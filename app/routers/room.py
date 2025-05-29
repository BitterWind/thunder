#this file is someting about player data and the operation of data 
from fastapi import APIRouter, HTTPException
from services.game_service import game_service
from typing import List,Dict

# 此处记录玩家的初始数据
router = APIRouter(prefix="/room_data_cache", tags=["玩家数据管理"])

#用来给创建房间的player更新房间数据，随时加入新玩家
@router.post("/get_room_update")
async def get_room_update(data: Dict):
    print("receive data for updating ",data)
    ans = await game_service.get_room_update(data["id"], data["room"])    #这里需要返回队友的数据，
    
    return ans

# 用来处理玩家离开房间的逻辑
@router.post("/leave_room")
async def leave_room(data: Dict):
    print("leave room received: ",data)
    result = await game_service.leave_room(data["id"], data["room"])
    return {"success": result}

# 用来处理玩家开始的逻辑
@router.post("/start_room")
async def start_room(data: Dict):
    print("start room received: ",data)
    result = await game_service.start_room(data["id"], data["room"])
    return {"success": result}
