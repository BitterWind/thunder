from typing import Dict
from models.schemas import GameState

class GameService:
    def __init__(self):
        self.player_log: Dict[str, dict] = {}
        # 初始化测试数据
        self.player_log["1"] = {
            'position': {'x': 500, 'y': 950},
            'size': 30,
            'color': '#00f',
            'active': True,
            'speed': 400,
            'key_mouse': {'KeyA': False, 'KeyS': False, 'KeyW': False, 'KeyD': False, 'Mouse': False},
            'mouse': {'x': 0, 'y': 0},
            'name': '1',
            'shootercnt': 0
        }

    async def update_player_log(self, data: dict) -> int:
        self.player_log[data["name"]] = data
        return 1

    async def get_player_log(self, name: str) -> dict:
        return self.player_log.get(name, {})

#这是一个类似gameState 的东西，但是是全局的，所有玩家共用的一个服务器存储对象
game_service = GameService() 