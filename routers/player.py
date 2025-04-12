#this file is someting about player data and the operation of data 
from fastapi import APIRouter, HTTPException
from services.game_service import game_service
from typing import List,Dict

# 此处实现双人模式
# 此处记录玩家的初始数据
router = APIRouter(prefix="/player_data_cache", tags=["玩家数据管理"])

#id and room number 
@router.post("/get_id")
async def get_id(data: Dict):
    ans = {"id":0, "room":-1}
    try:
        print("get_id receive:",data)
        if(game_service.any_room()):
            x = await game_service.get_id(data["name"])
            y = await game_service.get_room(data["mode"], x, data["room"])
            print(f"\n分配的id和房间号：{x,y}")
            ans["id"] = x
            ans["room"] = y
        else:
            raise HTTPException(500, detail="没有房间了")
    except Exception as e:
        print(str(e))
        raise HTTPException(500, detail=str(e))
    return ans  #单出口

@router.post("/send_log")
async def send_log(data: Dict):
    try:
        result = await game_service.update_player_log(data)
        print(f"\n服务器端存储的玩家数据：{game_service.player_log}")
        return result
    except Exception as e:
        raise HTTPException(500, detail=str(e))

@router.post("/get_log")
async def get_log(data: Dict):
    try:
        print(f"\n收到请求数据：{data}")
        return await game_service.get_player_log(data.get("name"))
    except Exception as e:
        raise HTTPException(500, detail=str(e))
    