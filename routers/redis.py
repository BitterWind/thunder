#this file is someting about player data and the operation of data 
from fastapi import APIRouter, HTTPException
from models.schemas import score_submit, leaderboard_entry
from data_bases.redis import get_redis
from services.game_service import game_service
from typing import List,Dict

#storage loong living data , like score , name , id ,etc : everything left after gaming 
r = get_redis()

# 尽量不适用get方法，
# 此处记录玩家的初始数据
router = APIRouter(prefix="/player_data_memory", tags=["玩家数据库管理"])

@router.post("/scores", 
            response_model=dict,
            status_code=201, 
            summary="提交分数并返回排名")
async def submit_score(data: dict): 
    try:
        # print(data)
        # 更新/添加分数到排行榜
        r.zadd("leaderboard", {data["id"]: data["score"]}, nx=False)
        # print(r.zrange("leaderboard", 0, -1, withscores=True)) 后续可以根据user id去找到
        # 获取当前排名（Redis返回的是从0开始的排名）
        raw_rank = r.zrevrank("leaderboard", data["id"])

        if raw_rank is None:
            raise HTTPException(500, "Failed to get ranking")
        
        # 转换为从1开始的排名
        current_rank = raw_rank + 1
        
        return {
            "id": data["id"],
            "score": data["score"],
            "rank": current_rank,
            "message": "Score updated successfully"
        }
    
    except Exception as e:
        raise HTTPException(500, f"Redis error: {str(e)}")
    

@router.post("/leaderboard", 
           summary="查询排行榜（POST方法）",
           description="通过POST请求查询排行榜，支持分页和完整列表")
async def leaderboard(request: dict):
    try:
        # 计算分页范围
        # start = (request["page"] - 1) * request["page_size"] #从第几页开始吗。
        # end = start + request["page_size"]  - 1
        start = 0
        end   = 10
        # 处理完整列表请求
        leaderboard = r.zrevrange("leaderboard", start, end, withscores=True)

        print(leaderboard)
        ans = {}
        for rank,(id, score) in enumerate(leaderboard):
            ans[game_service.player_log[int(id)]["name"]] = (score, int(id)+1, rank)
        print(ans)
        return ans  
    except Exception as e:
        raise HTTPException(500, f"Redis error: {str(e)}")
