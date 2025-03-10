# 这个文件没有用，当其无，有器之用。
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from data_bases.redis import get_redis

# 修改后的数据模型
class ScoreSubmit(BaseModel):
    id: str     # 字段名改为id
    score: float

# 修改后的响应模型
class SubmitResponse(BaseModel):
    id: str
    score: float
    rank: int
    message: str

router = APIRouter(prefix="/player_data_memory", tags=["玩家数据库管理"])
r = get_redis()

@router.post("/scores", 
            response_model=SubmitResponse,  # 使用新的响应模型
            status_code=201, 
            summary="提交分数并返回排名")
async def submit_score(data: ScoreSubmit):  # 使用新的请求模型
    try:
        # 更新/添加分数到排行榜
        r.zadd("leaderboard", {data.id: data.score}, nx=False)
        
        # 获取当前排名（Redis返回的是从0开始的排名）
        raw_rank = r.zrevrank("leaderboard", data.id)
        
        if raw_rank is None:
            raise HTTPException(500, "Failed to get ranking")
        
        # 转换为从1开始的排名
        current_rank = raw_rank + 1
        
        return {
            "id": data.id,
            "rank": current_rank,
            "message": "Score updated successfully"
        }
        
    except Exception as e:
        raise HTTPException(500, f"Redis error: {str(e)}")