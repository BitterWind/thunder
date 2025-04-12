from pydantic import BaseModel
from dataclasses import dataclass
from typing import Dict, Any

#for player data storage , 
@dataclass
class PositionStruct:
    def __init__(self, data):
        self.x = data['x']
        self.y = data['y']

class KeyMouseStruct:
    def __init__(self, data):
        self.KeyA = data['KeyA']
        self.KeyS = data['KeyS']
        self.KeyW = data['KeyW']
        self.KeyD = data['KeyD']
        self.Mouse = data['Mouse']

class MouseStruct:
    def __init__(self, data):
        self.x = data['x']
        self.y = data['y']
        
# ”类“一类的东西就用驼峰好了
class PlayerStruct:
    def __init__(self, data):
        self.name = data['name']
        self.id = data['id']
        self.position = PositionStruct(data['position'])  # 嵌套结构体
        self.size = data['size']
        self.color = data['color']
        self.active = data['active']
        self.speed = data['speed']
        self.key_mouse = KeyMouseStruct(data['key_mouse'])  # 嵌套结构体
        self.mouse = MouseStruct(data['mouse'])  # 嵌套结构体
        self.shooter_cnt = data['shooter_cnt']

    def __repr__(self):
        return f"PlayerStruct(name={self.name}, id={self.id}, position=({self.position.x}, {self.position.y}))"
