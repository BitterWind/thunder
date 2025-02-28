#之后可以和server.py整合一下
from fastapi import FastAPI, Form, HTTPException, Request
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
import redis
import bcrypt
from datetime import datetime, timedelta

# 创建 Redis 客户端连接
r = redis.StrictRedis(host='localhost', port=6379, db=0, decode_responses=True)

# FastAPI 初始化
app = FastAPI()

# Jinja2模板
templates = Jinja2Templates(directory="templates")

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
def login_page(request: Request):
    return templates.TemplateResponse("login.html", {"request": request})

# 登录处理
@app.post("/login")
def login(username: str = Form(...), password: str = Form(...)):
    user_key = f"user:{username}"

    # 获取用户信息
    if not r.exists(user_key):
        raise HTTPException(status_code=401, detail="Invalid username or password")

    # 获取用户的详细信息
    user_data = r.hgetall(user_key)

    # 检查账户是否被锁定
    lock_until = user_data.get("lock_until")
    if lock_until:
        if lock_until != "":
            lock_until_time = datetime.strptime(lock_until, "%Y-%m-%d %H:%M:%S")
            if lock_until_time > datetime.now():
                lock_duration = (lock_until_time - datetime.now()).seconds // 60
                raise HTTPException(status_code=403, detail=f"Account locked. Try again after {lock_duration} minutes.")

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
            raise HTTPException(status_code=401, detail="Invalid username or password. Account locked for 30 minutes.")
        
        # 更新失败次数
        r.hset(user_key, "failed_attempts", failed_attempts)
        raise HTTPException(status_code=401, detail="Invalid username or password")

    # 如果密码正确，重置失败次数和锁定时间
    r.hset(user_key, mapping={
        "failed_attempts": 0,
        "lock_until": ""  # 重置 lock_until 为一个空字符串
    })

    return {"message": f"Welcome back, {username}!"}

# 首页
@app.get("/", response_class=HTMLResponse)
def home(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

# 启动时确认数据库连接
@app.get("/check_db")
def check_db():
    # 检查数据库是否存在用户键
    user_keys = r.keys("user:*")
    if user_keys:
        return {"message": "Users exist in Redis!"}
    else:
        return {"message": "No users found in Redis!"}

