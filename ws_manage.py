from fastapi import WebSocket
import asyncio


class ConnectionManager:
    # :TODO active_connectionsをuserクラスで置き換える。
    def __init__(self):
        # :TODO distribute lobby and each game room
        self.active_connections: list[WebSocket] = []
        self.tmp_lobby: list[WebSocket] = []
        self.queue = asyncio.Queue(maxsize=4)
        self.event = asyncio.Event()
        self._iter_cnt = -1

    def __aiter__(self):
        return self

    async def __anext__(self):
        self._iter_cnt += 1
        if self._iter_cnt >= len(self.active_connections):
            self._iter_cnt = -1
            raise StopAsyncIteration
        return self.active_connections[self._iter_cnt]

    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        self.active_connections.append(websocket)
        self.tmp_lobby.append(websocket)

    async def queue_wait(self):
        if self.queue.full():
            self.event.set()
        await self.event.wait()

    def disconnect(self, websocket: WebSocket):
        self.active_connections.remove(websocket)
        self.tmp_lobby.remove(websocket)

    async def broadcast(self, message: str):
        for connection in self.active_connections:
            await connection.send_text(message)


if __name__ == "__main__":
    manager = ConnectionManager()
