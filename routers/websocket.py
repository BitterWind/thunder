from fastapi import APIRouter, WebSocket
from services.game_service import game_service

router = APIRouter()

@router.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    try:
        while True:
            data = await websocket.receive_text()
            await websocket.send_json({
                "players": game_service.player_log
            })
    except Exception as e:
        print(f"连接异常: {str(e)}")
    finally:
        await websocket.close()
        