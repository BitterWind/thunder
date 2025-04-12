#this file is someting about player data and the operation of data 
from fastapi import APIRouter, HTTPException
from services.game_service import game_service
from typing import List,Dict

# 此处记录玩家的初始数据
router = APIRouter(prefix="/room_data_cache", tags=["玩家数据管理"])

#用来给创建房间的player更新房间数据，随时加入新玩家
@router.post("/get_room_update")
async def get_room_update(data: Dict):
    try:
        print(data)
        ans = await game_service.get_room(data["id"], data["room"])    #这里需要返回队友的数据，
        return ans
    except Exception as e:
        print(str(e))
        raise HTTPException(500, detail=str(e))
