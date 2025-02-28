from fastapi import FastAPI, Form, HTTPException, Request, WebSocket
from fastapi.responses import HTMLResponse, RedirectResponse, FileResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from dataclasses import dataclass
import redis
import bcrypt
from datetime import datetime, timedelta
import json
from typing import Dict
import uvicorn

# 创建 Redis 客户端连接
r = redis.StrictRedis(host='localhost', port=6379, db=0, decode_responses=True)

# FastAPI 初始化
app = FastAPI()

# 允许跨域
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# 挂载静态文件目录
app.mount("/static", StaticFiles(directory="static"), name="static")

# Jinja2模板
templates = Jinja2Templates(directory="templates")

# 游戏状态类
class GameState:
    def __init__(self):
        self.players = {}

# 注册页面
@app.get("/register", response_class=HTMLResponse)
def register_page(request: Request):
    return templates.TemplateResponse("register.html", {"request": request})

# 注册处理
@app.post("/register")
def register(username: str = Form(...), password: str = Form(...)):
    user_key = f"user:{username}"

    # 检查用户名是否已经存在
    if r.exists(user_key):
        raise HTTPException(status_code=400, detail="Username already taken")

    # 密码加密
    hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
    
    # 存储用户信息到 Redis
    r.hset(user_key, mapping={
        "hashed_password": hashed_password.decode('utf-8'),
        "failed_attempts": 0,
        "lock_until": ""  # 使用空字符串代替 None
    })

    return RedirectResponse(url="/login", status_code=303)

# 登录页面
@app.get("/login", response_class=HTMLResponse)
def login_page(request: Request, error: str = None):
    # 获取 URL 查询参数中的 error 信息
    return templates.TemplateResponse("login.html", {"request": request, "error": error})

# 登录处理
@app.post("/login")
def login(username: str = Form(...), password: str = Form(...)):
    user_key = f"user:{username}"

    if not r.exists(user_key):
        # 用户名错误，跳转并显示错误信息
        return RedirectResponse(url="/login?error=Invalid%20username%20or%20password", status_code=303)

    user_data = r.hgetall(user_key)

    # 检查账户是否被锁定
    lock_until = user_data.get("lock_until")
    if lock_until:
        if lock_until != "":
            lock_until_time = datetime.strptime(lock_until, "%Y-%m-%d %H:%M:%S")
            if lock_until_time > datetime.now():
                lock_duration = (lock_until_time - datetime.now()).seconds // 60
                return RedirectResponse(url=f"/login?error=Account%20locked.%20Try%20again%20after%20{lock_duration}%20minutes", status_code=303)

    # 验证密码
    if not bcrypt.checkpw(password.encode('utf-8'), user_data["hashed_password"].encode('utf-8')):
        # 密码错误，增加失败次数
        failed_attempts = int(user_data["failed_attempts"]) + 1

        if failed_attempts >= 5:
            # 如果失败次数达到 5 次，锁定账户 30 分钟
            lock_until_time = (datetime.now() + timedelta(minutes=30)).strftime("%Y-%m-%d %H:%M:%S")
            r.hset(user_key, mapping={
                "failed_attempts": 0,
                "lock_until": lock_until_time
            })
            return RedirectResponse(url="/login?error=Invalid%20username%20or%20password.%20Account%20locked%20for%2030%20minutes", status_code=303)
        
        # 更新失败次数
        r.hset(user_key, "failed_attempts", failed_attempts)
        return RedirectResponse(url="/login?error=Invalid%20username%20or%20password", status_code=303)

    # 如果密码正确，重置失败次数和锁定时间
    r.hset(user_key, mapping={
        "failed_attempts": 0,
        "lock_until": ""  # 重置 lock_until 为一个空字符串
    })

    # 登录成功，重定向到主页或其他页面
    return RedirectResponse(url="/home", status_code=303)

# 首页路由，返回 home.html
@app.get("/home", response_class=HTMLResponse)
def home(request: Request):
    return templates.TemplateResponse("home.html", {"request": request})


# WebSocket 游戏逻辑
class Player:
    def __init__(self, name: str):
        self.name = name
        self.position = {"x": 0, "y": 0}
        self.size = 30
        self.color = "#00f"
        self.speed = 400
        self.keys = {"KeyW": False, "KeyA": False, "KeyS": False, "KeyD": False}
        self.mouse = {"x": 0, "y": 0}
        self.active = True
        self.id = 0

# 存储玩家位置数据（内存存储示例）
player_log: Dict[str, dict] = {}

async def game_loop(websocket: WebSocket):
    state = GameState()
    while True:
        data = await websocket.receive_text()  # 接收客户端数据
        # 此处可以根据游戏规则更新玩家位置等状态
        await websocket.send_json({"players": state.players})

@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    try:
        await game_loop(websocket)
    except Exception as e:
        print(f"连接异常: {str(e)}")
    finally:
        await websocket.close()

# 直接访问HTML文件的路由
@app.get("/client.html")
async def client():
    return FileResponse('static/client.html')  # 路径相对于项目根目录

@app.get("/game.html")
async def client():
    return FileResponse('static/game.html')  # 路径相对于项目根目录

# 存储玩家鼠标数据并返回处理结果
@app.post("/send-log-player")
async def send_log_player(data: dict):
    try:
        player_log[data["name"]] = data
        return data
    except Exception as e:
        return {"status": "error", "detail": str(e)}

# 获取玩家的数据
@app.post("/get-log-player")
async def get_log_player(data: dict):
    try:
        return player_log[data["name"]]
    except Exception as e:
        return {"status": "error", "detail": str(e)}

# 首页
@app.get("/", response_class=HTMLResponse)
def home(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

# 启动时确认数据库连接
@app.get("/check_db")
def check_db():
    user_keys = r.keys("user:*")
    if user_keys:
        return {"message": "Users exist in Redis!"}
    else:
        return {"message": "No users found in Redis!"}

# 运行服务器
if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)



