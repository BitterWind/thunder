from fastapi import APIRouter
from sse_starlette.sse import EventSourceResponse
import asyncio

router = APIRouter()


class SSEManager:
    def __init__(self):
        self.connections = {}

    def add_connection(self, room_id: int):
        queue = asyncio.Queue()
        if room_id not in self.connections:
            self.connections[room_id] = set()
        self.connections[room_id].add(queue)
        return queue

    def remove_connection(self, room_id: int, queue):
        self.connections[room_id].remove(queue)
        if not self.connections[room_id]:
            del self.connections[room_id]

    async def broadcast(self, room_id: int, message: str):
        if room_id in self.connections:
            for queue in self.connections[room_id]:
                await queue.put(message)


sse_manager = SSEManager()


@router.get("/room/{room_id}/stream")
async def room_stream(room_id: int):
    """SSE事件流"""

    async def event_generator():
        queue = sse_manager.add_connection(room_id)
        try:
            while True:
                data = await queue.get()
                yield {"event": "update", "data": data}
                queue.task_done()
        finally:
            sse_manager.remove_connection(room_id, queue)

    return EventSourceResponse(event_generator())