from fastapi import APIRouter, HTTPException
from services.game_service import game_service
from typing import Dict

router = APIRouter(prefix="/player", tags=["玩家管理"])

@router.post("/send-log")
async def send_log(data: Dict):
    try:
        result = await game_service.update_player_log(data)
        print(f"\n服务器端存储的玩家数据：{game_service.player_log}")
        return result
    except Exception as e:
        raise HTTPException(500, detail=str(e))

@router.post("/get-log")
async def get_log(data: Dict):
    try:
        print(f"\n收到请求数据：{data}")
        return await game_service.get_player_log(data.get("name"))
    except Exception as e:
        raise HTTPException(500, detail=str(e))