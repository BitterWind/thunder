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
        return f"PlayerStruct(name={self.name}, id={self.id}, position=({self.position.x}, {self.position.y}))"
    def data(self):
        return {
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
        }
    
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

if __name__ == "__main__":
    # Create a new player instance
    players  =   {}
    players[0] = Player(name="JohnDoe", id=1)
    # Print the player's initial data
    # print(players[0].data())
    data = {'position': {'x': 583.3500000000001, 'y': 275.10000000000014},
             'size': 30, 'color': 'hsl(358.7054177857062, 70%, 60%)',
               'active': True, 'speed': 500,
                 'keyMouse': {'KeyA': False, 'KeyS': False, 'KeyW': False, 'KeyD': False, 'Mouse': False},
                   'mouse': {'x': 650, 'y': 770},
                   'id': 1, 'room': 1, 'name': 'default_name', 'shooter_cnt': 8}
    players[1] = Player(name=data['name'], id=data['id'], room=data['room'])
    players[1].update(
        position=data['position'],
        size=data['size'],
        color=data['color'],
        active=data['active'],
        speed=data['speed'],
        key_mouse=data['keyMouse'],
        mouse=data['mouse'],
        shooter_cnt=data['shooter_cnt'],
        start=0
    )
    # Print the updated player's data
    print(players[1].data())
#踏实一点，小朋友。

