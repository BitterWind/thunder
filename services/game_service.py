from typing import Dict
from models.schemas import PlayerStruct
# cache storage fash and life short data , for example , position , moving direction ,etc 

class GameService:
    def __init__(self):
        self.player_log : Dict[int, dict]       =   {}
        self.id         : int                   =   1
        self.room_list  : Dict[int,dict]        =   {}
        self.empty_cnt  : int                   =   0 # cnt , 计数空房间数量, 从一号房间开始
        self.room_ptr   : int                   =   1 # ptr,用来指向一个空房间
        self.room_cnt   : int                   =   1 # room count，用来计数当前房间数量
        # 初始化测试数据
        self.player_log[0] = PlayerStruct({
            'name': '1',
            'id':0,
            'position': {'x': 500, 'y': 950},
            'size': 30,
            'color': '#00f',
            'active': True,
            'speed': 400,
            'key_mouse': {'KeyA': False, 'KeyS': False, 'KeyW': False, 'KeyD': False, 'Mouse': False},
            'mouse': {'x': 0, 'y': 0},
            'shooter_cnt': 0 #血量
        })

    async def update_player_log(self, data: dict) -> int:
        self.player_log[data["id"]] = data
        return 1

    async def get_player_log(self, id: int) -> dict:
        return self.player_log.get(id, {})

    #在这里初始化服务器的一个玩家
    async def get_id(self, name: str) -> dict:
        # print(f"get id {self.id} ")
        self.player_log[self.id] = PlayerStruct({#是的，这是默认初始数据
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
            'shooter_cnt': 0 #血量
        })
        self.id += 1 
        return self.id -1 
    
    #分配房间 , 这里的逻辑是比较简单的那种，复杂情况暂时不考虑 ， 进阶的话，这里应该用两个队列？
    async def get_room(self, mode:int, id:int, obj:int = -1) -> int:  #这里存在大量异步函数并行访问同一个变量，如何限制其串行访问，防止数据错乱？
        ans = 0   #默认0号房间
        match mode:
            case 2:
                #创建一个空房间
                self.room_list[self.room_cnt] = {"x":id, "y":0}
                ans = self.room_cnt
                self.room_cnt += 1 
                self.empty_cnt += 1
            case 3:
                #随机加入房间
                if(self.empty_cnt==0):#没有房间了，直接返回-1
                    ans = -1
                else:
                    while(self.room_list[self.room_ptr]["y"]!=0):#遍历到下一个，这一块和内存管理的位图有点像。
                        self.room_ptr += 1  
                    self.room_list[self.room_ptr]["y"] = id 
                    ans = self.room_ptr
                    self.room_ptr += 1
            case 4:
                #加入指定房间
                if(self.room_list[obj]["y"]!=0):
                    ans = -1 #出错了，例外优先处理 
                else:
                    self.room_list[obj]["y"]=id 
                    ans = obj 
        return ans
    
    #更新房间数据,  依据房间号来获取队友数据
    async def get_room_update(self, id:int, room:int) -> dict:
        ans = {}
        if(self.room_list[room]["y"]!=0):
            ans["team_member_name"] = self.player_log[self.room_list[room]["y"]]["name"]
            ans["team_member_id"] = self.room_list[room]["y"]
            ans["ready"] = 1
        else:
            ans["team_member_name"] = "NULL"
            ans["team_member_id"] = 0
            ans["ready"] = 0
        return ans
    
    async def any_room(self) -> bool:
        if(self.empty_cnt>0):
            return True
        else:
            return False
        
    async def is_empty(self, room:int) -> bool:
        if(self.room_list[room]["y"]==0):
            return True
        else:
            return False

#这是一个类似game_data 的东西，但是是全局的，所有玩家共用的一个服务器存储对象
# 该对象有不同的功能：玩家部分实时数据的存储，其余数据用redis来存储
game_service = GameService() 