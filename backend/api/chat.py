from fastapi import APIRouter, WebSocket, WebSocketDisconnect

from .models import ChatRequest

router = APIRouter()


@router.post("/")
async def chat(request: ChatRequest) -> dict:
    """Simple REST endpoint that echoes back a combined message."""
    reply = " ".join(message.content for message in request.messages)
    return {"reply": reply}


@router.websocket("/ws")
async def chat_ws(websocket: WebSocket) -> None:
    """Echo back incoming text as tokenized JSON messages."""
    await websocket.accept()
    try:
        while True:
            data = await websocket.receive_text()
            for token in data.split():
                await websocket.send_json({"token": token})
    except WebSocketDisconnect:
        pass
