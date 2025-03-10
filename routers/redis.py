#this file is someting about player data and the operation of data 
from fastapi import APIRouter, HTTPException
from models.schemas import score_submit, leaderboard_entry
from data_bases.redis import get_redis
from typing import List,Dict

#storage loong living data , like score , name , id ,etc : everything left after gaming 
r = get_redis()

# 尽量不适用get方法，
# 此处记录玩家的初始数据
router = APIRouter(prefix="/player_data_memory", tags=["玩家数据库管理"])

# POST /player_data_memory/scores HTTP/1.1"
@router.post("/get_id")
async def get_id(data: Dict):
    try:
        print(data)
        x = await game_service.get_id(data["name"])
        y = await game_service.get_room(data["mode"], x, data["obj"])
        return {"id":x, "room":y}
    except Exception as e:
        print(str(e))
        raise HTTPException(500, detail=str(e))
    
@router.post("/scores", 
            response_model=dict,
            status_code=201, 
            summary="提交分数并返回排名")
async def submit_score(data: dict): 
    try:
        print(data)
        # 更新/添加分数到排行榜
        r.zadd("leaderboard", {data["id"]: data["score"]}, nx=False)
        
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
    
@router.get("/leaderboard", response_model=List[leaderboard_entry], summary="获取排行榜")
async def get_leaderboard(top: int = 10):
    try:
        leaderboard = r.zrevrange("leaderboard", 0, top-1, withscores=True, score_cast_func=float)
        return [
            leaderboard_entry(user_id=uid, score=score, rank=idx+1)
            for idx, (uid, score) in enumerate(leaderboard)
        ]
    except Exception as e:
        raise HTTPException(500, f"Redis error: {str(e)}")

@router.get("/users/{user_id}/rank", summary="获取用户排名")
async def get_user_rank(user_id: str):
    try:
        score = r.zscore("leaderboard", user_id)
        if not score: raise HTTPException(404, "User not found")
        rank = r.zrevrank("leaderboard", user_id)
        return {
            "user_id": user_id,
            "score": float(score),
            "rank": rank + 1 if rank is not None else None
        }
    except Exception as e:
        raise HTTPException(500, f"Redis error: {str(e)}")
