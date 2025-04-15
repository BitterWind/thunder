from pydantic import BaseModel
from dataclasses import dataclass

class Player:
    def __init__(
            self,
            name: str = "NULL",
            id: int = 0,
            position: dict = {'x': 500, 'y': 950},
            room: int = 0,
            size: int = 30,
            color: str = "#00f",
            active: bool = True,
            speed: int = 400,
            key_mouse: dict = {"KeyW": False, "KeyA": False, "KeyS": False, "KeyD": False, "Mouse": False},
            mouse: dict = {"x": 0, "y": 0},
            shooter_cnt: int = 0,
            start:int = 0):
        
        self.name = name
        self.id = id
        self.position = position
        self.room = room
        self.size = size
        self.color = color
        self.active = active
        self.speed = speed
        self.key_mouse = key_mouse
        self.mouse = mouse
        self.shooter_cnt = shooter_cnt
        self.start = start


    def __repr__(self):
        return f"PlayerStruct(name={self.name}, id={self.id}, position=({self.position['x']}, {self.position['y']}))"
    def data(self):
        return dict({
            "name": self.name,
            "id": self.id,
            "position": self.position,
            "room": self.room,
            "size": self.size,
            "color": self.color,
            "active": self.active,
            "speed": self.speed,
            "key_mouse": self.key_mouse,
            "mouse": self.mouse,
            "shooter_cnt": self.shooter_cnt,
            "start": self.start
        })
    
    def update(
            self,
            name: str = None,
            id: int = None,
            position: dict = None,
            room: int = None,
            size: int = None,
            color: str = None,
            active: bool = None,
            speed: int = None,
            key_mouse: dict = None,
            mouse: dict = None,
            shooter_cnt: int = None,
            start:int = None
        ):
        self.name = name if name is not None else self.name
        self.id = id if id is not None else self.id
        self.position = position if position is not None else self.position
        self.room = room if room is not None else self.room
        self.size = size if size is not None else self.size
        self.color = color if color is not None else self.color
        self.active = active if active is not None else self.active
        self.speed = speed if speed is not None else self.speed
        self.key_mouse = key_mouse if key_mouse is not None else self.key_mouse
        self.mouse = mouse if mouse is not None else self.mouse
        self.shooter_cnt = shooter_cnt if shooter_cnt is not None else self.shooter_cnt
        self.start = start if start is not None else self.start
        