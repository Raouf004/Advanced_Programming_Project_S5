from fastapi import WebSocket
from typing import Dict, List


class ConnectionManager:
    def __init__(self):
        self.rooms: Dict[str, List[WebSocket]] = {}

    async def connect(self, room_id: str, websocket: WebSocket):
        await websocket.accept()
        self.rooms.setdefault(room_id, []).append(websocket)

    def disconnect(self, room_id: str, websocket: WebSocket):
        self.rooms[room_id].remove(websocket)
        if not self.rooms[room_id]:
            del self.rooms[room_id]

    async def broadcast(self, room_id: str, message: dict, sender: WebSocket):
        for ws in self.rooms.get(room_id, []):
            if ws != sender:
                await ws.send_json(message)
