from fastapi import WebSocket, WebSocketDisconnect
from app.websockets.manager import ConnectionManager
from app.websockets.auth import get_current_user_ws

manager = ConnectionManager()


async def chat_socket(websocket: WebSocket, room_id: str):
    user = await get_current_user_ws(websocket)
    if not user:
        return  # connection already closed

    await manager.connect(room_id, websocket)

    try:
        while True:
            data = await websocket.receive_json()

            await manager.broadcast(
                room_id,
                {
                    "type": "chat",
                    "sender": user,   # 🔐 trusted identity
                    "message": data.get("message"),
                },
                websocket,
            )

    except WebSocketDisconnect:
        manager.disconnect(room_id, websocket)
