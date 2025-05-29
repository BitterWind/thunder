# routers/ws.py (WebSocket适配)
from fastapi import APIRouter, WebSocket, WebSocketDisconnect
from services.game_service import game_service
import json

router = APIRouter()

# 连接管理
active_connections = {}  # {player_id: WebSocket}

async def broadcast_room_state(room_id: int, exclude_id: int = None):
    """向房间内所有玩家广播状态"""
    room = game_service.room_list.get(room_id)
    if not room:
        return
    
    # 获取房间内所有玩家ID
    player_ids = []
    if room["x"] != 0:
        player_ids.append(room["x"])
    if room["y"] != 0:
        player_ids.append(room["y"])
    
    # 向每个玩家发送队友信息
    for pid in player_ids:
        if pid == exclude_id or pid not in active_connections:
            continue
        
        # 获取该玩家的视角数据
        room_data = await game_service.get_room_update(pid, room_id)
        await active_connections[pid].send_json({
            "type": "room_update",
            "data": room_data
        })

@router.websocket("/ws/{client_id}")
async def websocket_endpoint(websocket: WebSocket, client_id: int):
    await websocket.accept()
    active_connections[client_id] = websocket
    current_room = None  # 跟踪玩家所在房间

    try:
        while True:
            data = await websocket.receive_text()
            
            # 处理消息类型
            message = json.loads(data)
            msg_type = message.get("type")
            
            if msg_type == "update_player":
                # 更新玩家状态
                await game_service.update_player_log(message)
                
                # 广播给同房间玩家（排除自己）
                if current_room is not None:
                    await broadcast_room_state(current_room, exclude_id=client_id)
                    
            elif msg_type == "join_room":
                # 加入房间逻辑
                mode = message.get("mode")
                room = message.get("room", -1)
                assigned_room = await game_service.get_room(mode, client_id, room)
                
                if assigned_room == -1:
                    await websocket.send_json({"error": "加入房间失败"})
                else:
                    current_room = assigned_room
                    # 通知房间内所有玩家更新状态
                    await broadcast_room_state(current_room)
                    
            elif msg_type == "leave_room":
                # 离开房间
                if current_room is not None:
                    success = await game_service.leave_room(client_id, current_room)
                    if success:
                        await broadcast_room_state(current_room)
                        current_room = None
                        
    except WebSocketDisconnect:
        # 断开连接时清理
        if client_id in active_connections:
            del active_connections[client_id]
        if current_room is not None:
            await game_service.leave_room(client_id, current_room)
            await broadcast_room_state(current_room)
