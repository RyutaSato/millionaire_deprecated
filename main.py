import os
import sys
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from ws_manage import Manager, WebSocket
from user import User
from fastapi import FastAPI, WebSocketDisconnect
from fastapi.responses import FileResponse
from db_config import db_config
db_config()
app = FastAPI(version="0.75.1")
manager = Manager()


@app.get("/")
async def get():
    return FileResponse("index.html")
    # return HTMLResponse(html)


@app.get("/style.css")
async def get():
    return FileResponse("style.css")


@app.get("/main.js")
async def get():
    return FileResponse("main.js")


@app.websocket("/ws/{client_id}")
async def websocket_endpoint(websocket: WebSocket, client_id: int):
    await manager.connect(websocket)
    print(manager.active_connections)
    try:
        while True:
            data = await websocket.receive_text()
            print(f"client:{websocket.headers.get('sec-websocket-key')} {websocket.client}")
            await manager.send_personal_message(f"You wrote: {data}", websocket)
            await manager.broadcast(f"Client #{client_id} says: {data}")
            await manager.send_personal_message(f"Matching cueue.. in {len(manager.active_connections)}", websocket)
    except WebSocketDisconnect:
        manager.disconnect(websocket)
        await manager.broadcast(f"Client #{client_id} left the chat")
