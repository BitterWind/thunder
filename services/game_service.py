from typing import Dict
from models.schemas import Player
# cache storage fash and life short data , for example , position , moving direction ,etc 

class GameService:
    def __init__(self):
        self.player_log                         =   {}
        self.id         : int                   =   1
        self.room_list                          =   {}
        self.empty_cnt  : int                   =   0 # cnt , 计数空房间数量, 从一号房间开始
        self.room_ptr   : int                   =   1 # ptr,用来指向一个空房间
        self.room_cnt   : int                   =   1 # 给最新的房间编号赋值
        # 初始化测试数据
        self.player_log[0] = Player()

    async def update_player_log(self, data: dict) -> int:
        self.player_log[int(data["id"])].update(
            position=dict(data["position"]), 
            key_mouse=dict(data["key_mouse"]),
            mouse=dict(data["mouse"]),
            shooter_cnt=int(data["shooter_cnt"]),
            )
        return 1

    async def get_player_log(self, id: int) -> dict:
        return self.player_log[id].data()

    #在这里初始化服务器的一个玩家
    async def get_id(self, name: str) -> dict:
        # print(f"get id {self.id} ")
        self.player_log[self.id] = Player(name=name, id=self.id)
        self.id += 1 
        return self.id -1 
    
    #分配房间 , 这里的逻辑是比较简单的那种，复杂情况暂时不考虑 ， 进阶的话，这里应该用两个队列？
    async def get_room(self, mode:int, id:int, room:int = -1) -> int:  #这里存在大量异步函数并行访问同一个变量，如何限制其串行访问，防止数据错乱？
        ans = 0   #默认 single 0号房间
        room = int(room)

        match mode:
            case 2:
                #创建一个空房间
                self.room_list[self.room_cnt] = {"x":id, "y":0, "start":0}
                ans = self.room_cnt
                self.room_cnt += 1 
                self.empty_cnt += 1
            case 3:
                #随机加入房间
                if(self.empty_cnt==0):#没有房间了，直接返回-1
                    ans = -1
                else:
                    while(True):#遍历到下一个，这一块和内存管理的位图有点像。
                        if self.room_ptr not in self.room_list:
                            self.room_ptr += 1
                            continue
                        if self.room_list[self.room_ptr]["y"]==0:
                            break
                        self.room_ptr += 1
                    self.room_list[self.room_ptr]["y"] = id 
                    ans = self.room_ptr
                    self.room_ptr += 1
                    self.empty_cnt -= 1
            case 4:
                #加入指定房间
                # print(f"指定房间号：{room}")
                # print(f"当前房间列表：{self.room_list}")
                # print(f"room 类型{type(room)}")
                # print(f"room_list[room]: {self.room_list[int(room)]}")
                if(self.room_list[room]["y"]!=0):
                    ans = -1 #出错了，例外优先处理 
                else:
                    self.room_list[room]["y"]=id 
                    ans = room 
                    self.room_ptr += 1
                    self.empty_cnt -= 1
        return ans
    
    #更新房间数据,  依据房间号来获取队友数据
    async def get_room_update(self, id:int, room:int) -> dict:
        room = int(room)
        ans = {}

        if room not in self.room_list:
            ans["team_member"] = {"name":"NULL", "id":0}
            ans["active"] = 0
            ans["ready"] = 0
            ans["start"] = 0
            return ans
        elif self.room_list[room]["y"] == 0: #房间里只有房主
            ans["team_member"] = {"name":"NULL", "id":0}
            ans["active"] = 1
            ans["ready"] = 0
        elif self.room_list[room]["x"] == id: #房主问队友
            ans["team_member"] = {"name":self.player_log[self.room_list[room]["y"]].data()['name'], "id":self.room_list[room]["y"]}
            ans["ready"] = 1
            ans["active"] = 1
        elif self.room_list[room]["y"] == id: #队友问房主
            ans["team_member"] = {"name":self.player_log[self.room_list[room]["x"]].data()['name'], "id":self.room_list[room]["x"]}
            ans["ready"] = 1
            ans["active"] = 1
        else:
            ans["team_member"] = {"name":"NULL", "id":0}
            ans["active"] = 1
            ans["ready"] = 0
            
        ans["start"] = self.room_list[room]["start"]
        print(f"get_room_update: {id} {room} {ans} {self.player_log[self.room_list[room]["x"]].data()}")
        print(f"room_list now: {self.room_list}\n")
        return ans
    
    async def is_empty(self, room:int) -> bool:
        if room not in self.room_list:
            return False
        # 判断房间是否为空
        if(self.room_list[room]["y"]==0):
            return True
        else:
            return False
    
    async def leave_room(self, id: int, room: int) -> bool:
        print(f"\n\nleave_room: player_id={id} left room_id={room}")
        print(f"room_list before leave: {self.room_list}")
        # 验证房间存在
        if room not in self.room_list: #考虑到异步函数的并发访问问题，直接用特例来处理
            return True
        
        # 移除玩家并更新房间状态
        if self.room_list[room]["x"] == id:
            self.room_list[room]["x"] = 0
            if(self.room_list[room]["y"] == 0):#没有成员
                self.empty_cnt -= 1
                if self.room_ptr > room:
                    self.room_ptr = room
            # 如果是房主离开，直接解散
            del self.room_list[room]

        elif self.room_list[room]["y"] == id:
            self.room_list[room]["y"] = 0
            self.empty_cnt += 1
            if self.room_ptr > room:
                self.room_ptr = room
        else:
            return False  # 玩家不在该房间
        
        # 清理玩家数据
        if id in self.player_log:
            del self.player_log[id]
        print(f"room_list after leave: {self.room_list}")
        print(f"当前指针指向：{self.room_ptr}\n\n")
        return True
    
    async def start_room(self, id:int, room:int ) -> bool:
        if(self.room_list[room]["x"]==id):
            self.room_list[room]["start"] = 1
            return True
        else:
            return False

#这是一个类似game_data 的东西，但是是全局的，所有玩家共用的一个服务器存储对象
# 该对象有不同的功能：玩家部分实时数据的存储，其余数据用redis来存储
game_service = GameService() 