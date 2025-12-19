from fastapi import WebSocket, status
from jose import JWTError, jwt
from app.utils.auth import SECRET_KEY, ALGORITHM


async def get_current_user_ws(websocket: WebSocket) -> str | None:
    token = websocket.query_params.get("token")

    if not token:
        await websocket.close(code=status.WS_1008_POLICY_VIOLATION)
        return None

    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")

        if username is None:
            raise JWTError()

        return username

    except JWTError:
        await websocket.close(code=status.WS_1008_POLICY_VIOLATION)
        return None
