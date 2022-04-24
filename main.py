import os
from typing import List
from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.responses import HTMLResponse
from fastapi.responses import FileResponse
from time import sleep
with open("index.html", 'r', encoding='utf-8') as f:
    html: str = f.read()


class User:
    def __init__(self, websocket: WebSocket):
        self.ws = websocket


class Manager:
    def __init__(self):
        self.active_connections: List[WebSocket] = []

    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        self.active_connections.append(websocket)

    def disconnect(self, websocket: WebSocket):
        self.active_connections.remove(websocket)

    async def send_personal_message(self, message: str, websocket: WebSocket):
        await websocket.send_text(message)

    async def broadcast(self, message: str):
        for connection in self.active_connections:
            await connection.send_text(message)


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
