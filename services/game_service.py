from typing import Dict
from models.schemas import game_state
# cache  storage fash and life short data , for example , position , moving direction ,etc 

class GameService:
    def __init__(self):
        self.player_log : Dict[int, dict]       =   {}
        self.id         : int                   =   1
        self.room_list  : Dict[int,dict]        =   {}
        self.room_ptr   : int                   =   1 # ptr
        self.room_cnt   : int                   =   0
        # 初始化测试数据
        self.player_log[1] = {
            'name': '1',
            'id':0,
            'position': {'x': 500, 'y': 950},
            'size': 30,
            'color': '#00f',
            'active': True,
            'speed': 400,
            'key_mouse': {'KeyA': False, 'KeyS': False, 'KeyW': False, 'KeyD': False, 'Mouse': False},
            'mouse': {'x': 0, 'y': 0},
            'shootercnt': 0 #血量
        }

    async def update_player_log(self, data: dict) -> int:
        self.player_log[data["name"]] = data
        return 1

    async def get_player_log(self, name: str) -> dict:
        return self.player_log.get(name, {})

    async def get_id(self, name: str) -> dict:
        print("get id ")
        self.player_log[self.id] = {#是的，这是默认初始数据
            'position': {'x': 500, 'y': 950},
            'id':self.id,
            'room':0,
            'size': 30,
            'color': '#00f',
            'active': True,
            'speed': 400,
            'key_mouse': {'KeyA': False, 'KeyS': False, 'KeyW': False, 'KeyD': False, 'Mouse': False},
            'mouse': {'x': 0, 'y': 0},
            'name': name,
            'shootercnt': 0 #血量
        }
        self.id += 1 
        return self.id -1 
    
    #分配房间 , 这里的逻辑是比较简单的那种，复杂情况暂时不考虑 ， 进阶的话，这里应该用两个队列？
    async def get_room(self, mode:int, id:int, obj:int) -> int:
        print("get room ")
        ans = 0
        match mode:
            case 2:
                #创建一个空房间
                self.room_list[self.room_cnt] = {"x":id, "y":0}
                ans = self.room_cnt
                self.room_cnt += 1 
            case 3:
                #随机加入房间?
                while(self.room_list[self.room_ptr]["y"]!=0):#遍历到下一个
                    self.room_ptr += 1  
                self.room_list[self.room_ptr]["y"] = id 
                ans = self.room_ptr
                self.room_ptr += 1
            case 4:
                if(self.room_list[obj]["y"]!=0):
                    ans = -1 #出错了，例外优先处理 
                else:
                    self.room_list[obj]["y"]=id 
                    ans = obj 
        return ans
#这是一个类似game_state 的东西，但是是全局的，所有玩家共用的一个服务器存储对象
# 该对象有不同的功能：玩家部分实时数据的存储，其余数据用redis来存储
game_service = GameService() 