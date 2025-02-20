from fastapi.websockets import WebSocket
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import time
from typing import Dict
import json

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
        data = await websocket.receive_text()
        msg = json.loads(data)
        
        # 更新玩家状态（示例：移动指令）
        if msg['type'] == 'move':
            state.players[msg['playerId']] = {
                'x': msg['x'],
                'y': msg['y']
            }
        
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



# 存储玩家位置数据（内存存储示例）
player_positions: Dict[str, dict] = {}

class PositionData(BaseModel):
    x: int
    y: int
    player_id: str

@app.post("/update-position")
async def update_position(data: PositionData):
    """更新玩家位置"""
    player_positions[data.player_id] = {
        "x": data.x,
        "y": data.y,
        "timestamp": time.time()
    }
    print("\t\t\t\t\t\t\t\t\t\tx: %d   y: %d  id : %s"%(data.x,data.y,data.player_id))
    return {"status": "success"}

@app.get("/get-positions")
async def get_positions():
    """获取所有玩家位置（用于后续扩展）"""
    return player_positions