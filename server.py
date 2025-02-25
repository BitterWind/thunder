# 后端 FastAPI 服务 (main.py)
from fastapi.websockets import WebSocket
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from dataclasses import dataclass
import time
from typing import Dict
import json
import uvicorn

#使用的服务器
app = FastAPI()

# 允许跨域
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# 挂载静态文件目录（必须放在路由定义前）[2]
app.mount("/static", StaticFiles(directory="static"), name="static")

# 定义根路由[1]
@app.get("/")
async def main():
    return {"message": "访问/client.html 或者/game.html 开始游戏"}

# 直接访问HTML文件的路由[2]
@app.get("/client.html")
async def client():
    return FileResponse('static/client.html')  # 路径相对于项目根目录[3]

@app.get("/game.html")
async def client():
    return FileResponse('static/game.html')  # 路径相对于项目根目录[3]

class GameState:
    def __init__(self):
        self.players = {}

async def game_loop(websocket: WebSocket):
    state = GameState()
    while True:
        # 接收客户端消息（非阻塞方式）
        data = await websocket.receive_text()#实际上，只有在双人模式的时候需要收集游戏数据
        
        # 发送当前游戏状态
        await websocket.send_json({
            "players": state.players
        })

@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    try:
        await game_loop(websocket)
    except Exception as e:
        print(f"连接异常: {str(e)}")
    finally:
        await websocket.close()

@app.post("/send-log-player")
async def send_log_player(data: dict):
    print(f"\n\n服务器端的名单：",player_log)
    """存储鼠标数据并返回处理结果"""
    try:
        # 此处可添加数据库存储逻辑  
        player_log[data["name"]]=data
        return data
    except Exception as e:
        return {"status": "error", "detail": str(e)}

@app.post("/get-log-player")
async def get_log_player(data:dict):
    print(f"\n\n服务器端的收到了：",data)
    """使得请求方获取另一个玩家的数据"""
    try:
        # 此处可添加数据库存储逻辑  
        print(f"\n\n发送了：Send: ",data)
        return player_log[data["name"]]  #一个dict， 包括id
    except Exception as e:
        return {"status": "error", "detail": str(e)}


# 存储玩家位置数据（内存存储示例）
player_log: Dict[str, dict] = {}
player_log["guy"]={'position': {'x': 713.32, 'y': 656.6800000000001}, 'size': 30, 'color': '#00f', 'active': True, 'speed': 400, 'keys': {'KeyW': False, 'KeyA': False, 'KeyS': False, 'KeyD': False, 'Mouse': False}, 'id': 259.054763912734, 'mouse': {'x': 316, 'y': 607}, 'name': 'guy'}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
