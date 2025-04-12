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
# 原始字典数据
player_data = {
    'name': '1',
    'id': 0,
    'position': {'x': 500, 'y': 950},
    'size': 30,
    'color': '#00f',
    'active': True,
    'speed': 400,
    'key_mouse': {'KeyA': False, 'KeyS': False, 'KeyW': False, 'KeyD': False, 'Mouse': False},
    'mouse': {'x': 0, 'y': 0},
    'shooter_cnt': 0
}

# 转换为结构体
player = PlayerStruct(player_data)

# 访问属性
print(player.name)  # 输出: "1"
print(player.position.x)  # 输出: 500
print(player.key_mouse.KeyA)  # 输出: False