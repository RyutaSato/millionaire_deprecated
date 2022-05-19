import os
import sys
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from ws_manage import Manager, WebSocket
from user import User
from fastapi import FastAPI, WebSocketDisconnect, Depends
from fastapi.security import OAuth2PasswordBearer
from fastapi.responses import FileResponse
from db_config import db_config
import json
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
    try:
        while True:
            data = await websocket.receive_text()
            # data = await websocket.receive_json()
            reply_dict = {
                "client": websocket.headers.get('sec-websocket-key'),
                "status": "online",
                "message": data
            }
            # for key in websocket.headers.keys():
            #     print(key, websocket.headers.get(key))
            print(f"client:{websocket.headers.get('sec-websocket-key')} {websocket.client}")
            await manager.send_personal_message(f"You wrote: {data}", websocket)
            # await manager.broadcast(f"Client #{client_id} says: {data}")
            await manager.broadcast(json.dumps(reply_dict))
            await manager.send_personal_message(f"Matching cueue.. in {len(manager.active_connections)}", websocket)
    except WebSocketDisconnect:
        manager.disconnect(websocket)
        await manager.broadcast(f"Client #{client_id} left the chat")

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


@app.post("/items/")
async def read_items(token: str = Depends(oauth2_scheme)):
    return {"token": token}