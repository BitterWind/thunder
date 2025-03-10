from pydantic import BaseModel
from dataclasses import dataclass
from typing import Dict, Any

#for player data storage , 
@dataclass
class game_state:
    players: Dict[str, Any] 

#cache data 
class player_data(BaseModel):
    id: int 
    position: dict
    size: int
    active: bool
    speed: int
    key_mouse: dict
    mouse: dict
    shootercnt: int

#memory data
class other_player_data(BaseModel):
    id : int 
    name : str
    color : str
    score : int 

class score_submit(BaseModel):
    user_id: str
    score: float

class leaderboard_entry(BaseModel):
    user_id: str
    score: float
    rank: int
