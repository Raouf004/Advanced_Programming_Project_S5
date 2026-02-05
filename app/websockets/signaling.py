from fastapi import WebSocket, WebSocketDisconnect
from app.websockets.manager import ConnectionManager
from app.websockets.auth import get_current_user_ws

manager = ConnectionManager()


async def signaling_socket(websocket: WebSocket, room_id: str):
    user = await get_current_user_ws(websocket)
    if not user:
        return

    await manager.connect(room_id, websocket)

    try:
        while True:
            data = await websocket.receive_json()

            await manager.broadcast(
                room_id,
                {
                    "type": data["type"],      # offer / answer / ice-candidate
                    "sender": user,
                    "payload": data["payload"],
                },
                websocket,
            )

    except WebSocketDisconnect:
        manager.disconnect(room_id, websocket)
