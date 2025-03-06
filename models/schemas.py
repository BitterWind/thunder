from pydantic import BaseModel
from dataclasses import dataclass
from typing import Dict, Any

@dataclass
class GameState:
    players: Dict[str, Any]

class PlayerData(BaseModel):
    name: str
    position: dict
    size: int
    color: str
    active: bool
    speed: int
    key_mouse: dict
    id: float
    mouse: dict
    shootercnt: int

class ScoreSubmit(BaseModel):
    user_id: str
    score: float

class LeaderboardEntry(BaseModel):
    user_id: str
    score: float
    rank: int
