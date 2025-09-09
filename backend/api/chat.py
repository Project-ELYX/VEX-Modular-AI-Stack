from fastapi import APIRouter, WebSocket, WebSocketDisconnect
from fastapi.responses import StreamingResponse

from ..agents.vex_router import VexRouter
from .models import ChatRequest

router = APIRouter()


@router.post("/")
async def chat(request: ChatRequest):
    """Process messages via :class:`VexRouter`, optionally streaming."""
    user_message = request.messages[-1].content if request.messages else ""
    vex_router = VexRouter()
    vex_router.set_remote(request.remote)

    if request.stream:
        generator = await vex_router.handle_message(user_message, stream=True)
        return StreamingResponse(generator, media_type="text/plain")

    reply = await vex_router.handle_message(user_message, stream=False)
    if isinstance(reply, str):
        return {"reply": reply}
    return {"reply": ""}


@router.websocket("/ws")
async def chat_ws(websocket: WebSocket) -> None:
    """WebSocket interface backed by :class:`VexRouter`."""
    stream = websocket.query_params.get("stream", "true").lower() == "true"
    remote = websocket.query_params.get("remote", "false").lower() == "true"

    await websocket.accept()
    vex_router = VexRouter()
    vex_router.set_remote(remote)
    try:
        while True:
            data = await websocket.receive_text()
            result = await vex_router.handle_message(data, stream=stream)
            if stream:
                async for token in result:
                    await websocket.send_json({"token": token})
            else:
                if isinstance(result, str):
                    await websocket.send_json({"reply": result})
                else:
                    await websocket.send_json({"reply": ""})
    except WebSocketDisconnect:
        pass
