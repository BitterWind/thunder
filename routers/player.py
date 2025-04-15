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
    # print("get_id receive:",data)
    print(f"当前房间情况:{game_service.room_list}")
    if(data["mode"]==3):
        if(game_service.empty_cnt<=0):
            ans = {"id":-1, "room":-1}
            return ans
        # 这里需要返回队友的数据，
    x = await game_service.get_id(data["name"])
    y = await game_service.get_room(data["mode"], x, data["room"])
    print(f"\n分配的id和房间号：{x,y}")
    ans["id"] = x
    ans["room"] = y
    return ans  #单出口

@router.post("/send_log_player")
async def send_log(data: Dict):
    await game_service.update_player_log(data)
    print(f"\n服务器端存储的玩家数据：{game_service.player_log}")
    return True

@router.post("/get_log_player")
async def get_log(data: Dict):
    print(f"\n收到请求数据：{data}")
    ans = await game_service.get_player_log(data.get("name"))
    print(f"返回数据{ans}")
    return ans
