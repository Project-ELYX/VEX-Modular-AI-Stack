"""Chat endpoints for HTTP and WebSocket communication."""

from fastapi import APIRouter, Request, WebSocket, WebSocketDisconnect
from fastapi.responses import StreamingResponse

from ..agents.vex_router import VexRouter

router = APIRouter()


@router.post("/")
async def chat(request: Request):
    """Process messages via :class:`VexRouter`, optionally streaming.

    The endpoint expects a JSON payload of the form::

        {"message": "...", "mode": "local"|"remote", "stream": bool}

    """

    payload = await request.json()
    message = payload.get("message", "")
    mode = payload.get("mode", "local")
    stream = payload.get("stream", False)

    vex_router = VexRouter()
    vex_router.set_remote(mode == "remote")

    if stream:
        generator = await vex_router.handle_message(message, stream=True)

        async def _stream() -> list:
            async for token in generator:
                yield token
            # Signal end-of-stream so clients know when streaming is complete
            yield "[DONE]"

        return StreamingResponse(_stream(), media_type="text/plain")

    reply = await vex_router.handle_message(message, stream=False)
    if isinstance(reply, str):
        return {"reply": reply}
    return {"reply": ""}


@router.websocket("/ws")
async def chat_ws(websocket: WebSocket) -> None:
    """WebSocket interface backed by :class:`VexRouter`."""
    stream = websocket.query_params.get("stream", "true").lower() == "true"

    await websocket.accept()
    vex_router = VexRouter()
    try:
        while True:
            data = await websocket.receive_json()
            message = data.get("message", "")
            mode = data.get("mode", "local")
            vex_router.set_remote(mode == "remote")

            result = await vex_router.handle_message(message, stream=stream)
            if stream:
                accumulated = ""
                async for token in result:
                    accumulated += token
                    await websocket.send_json({"token": token})
                # Include a completion flag so clients can detect the end of the stream
                await websocket.send_json({"reply": accumulated, "done": True})
            else:
                if isinstance(result, str):
                    await websocket.send_json({"reply": result, "done": True})
                else:
                    await websocket.send_json({"reply": "", "done": True})
    except WebSocketDisconnect:
        pass
