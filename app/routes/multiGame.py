from collections import defaultdict

from fastapi import APIRouter, Query, WebSocket, WebSocketDisconnect
from fastapi.templating import Jinja2Templates
from numpy.random import random
from sqlalchemy import select
from fastapi import APIRouter, Request, Depends, Form, status, HTTPException
from fastapi.responses import HTMLResponse, RedirectResponse
from sqlalchemy.orm import Session

from typing import Dict, List
from fastapi.staticfiles import StaticFiles
import uuid
import json

from .auth import get_db
from models.user import User
from models.room import Room
from database import SessionLocal


router = APIRouter()
templates = Jinja2Templates(directory="./templates")



class GameManager:
    def __init__(self):
        self.active_connections = {}
        self.players = {}
        self.bullets = []

    async def broadcast(self, message: dict):
        for connection in self.active_connections.values():
            await connection.send_text(json.dumps(message))


game_manager = GameManager()


@router.get("/multiGame")
async def game_page(
    request: Request,
    room: int = Query(...),
    game: str = Query(...),
    db: Session = Depends(get_db)
):
    username = request.session.get("username")

    if not username:
        return RedirectResponse(url="/")
    """游戏主页面"""
    user = db.query(User).filter(User.username == username).first()
    return templates.TemplateResponse(
        "teamGame.html",
        {"request": request, "room_id": room, "game_id": game}
    )

@router.websocket("/game/{room_id}/ws")
async def websocket_endpoint(websocket: WebSocket, room_id: str):
    await websocket.accept()
    player_id = str(uuid.uuid4())

    try:
        # 初始化玩家
        game_manager.active_connections[player_id] = websocket
        game_manager.players[player_id] = {
            "x": 400,
            "y": 500,
            "color": f"hsl({hash(player_id) % 360}, 100%, 50%)",
            "score": 0
        }

        # 发送初始数据
        await websocket.send_text(json.dumps({
            "type": "init",
            "playerId": player_id,
            "players": game_manager.players,
            "bullets": game_manager.bullets
        }))

        # 持续监听消息
        while True:
            data = await websocket.receive_json()

            if data["type"] == "move":
                # 更新玩家位置
                game_manager.players[player_id]["x"] += data.get("dx", 0)
                game_manager.players[player_id]["y"] += data.get("dy", 0)

                # 边界限制
                game_manager.players[player_id]["x"] = max(0, min(760, game_manager.players[player_id]["x"]))
                game_manager.players[player_id]["y"] = max(0, min(560, game_manager.players[player_id]["y"]))

                await game_manager.broadcast({
                    "type": "playerUpdate",
                    "playerId": player_id,
                    "x": game_manager.players[player_id]["x"],
                    "y": game_manager.players[player_id]["y"]
                })

            elif data["type"] == "fire":
                # 生成子弹
                new_bullet = {
                    "id": str(uuid.uuid4()),
                    "x": data["x"] + 20,
                    "y": data["y"] - 10,
                    "dx": data["direction"]["x"] * 0.1,
                    "dy": data["direction"]["y"] * 0.1,
                    "owner": player_id
                }
                game_manager.bullets.append(new_bullet)

                await game_manager.broadcast({
                    "type": "bulletCreate",
                    "bullet": new_bullet
                })

    except WebSocketDisconnect:
        # 清理断开连接
        del game_manager.active_connections[player_id]
        del game_manager.players[player_id]
        await game_manager.broadcast({
            "type": "playerLeave",
            "playerId": player_id
        })

