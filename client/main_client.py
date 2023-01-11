import asyncio

import websockets

from client.ws_client import WebSocketClient
from types_both import *


async def ws_client(token: str):
    async with websockets.connect(
            f"ws://127.0.0.1:8000/ws?token={token}") as ws:
        client = WebSocketClient(ws)
        await client.rq_change_status(UserStatusType.QueueIn)
        await client.matched()
        await client.play()


async def main():
    tokens = {"01835c3a-fb3d-b4e2-a43e-1682dc0be131",
              "01835c3a-fb3d-3520-3d79-6534542003b1",
              "01835c3a-fb3d-1c2e-8375-a475a429ca89",
              "01835c3a-fb3d-3520-3d79-6534542003b1"}
    tasks = set()
    for token in tokens:
        task = asyncio.create_task(ws_client(token))
        tasks.add(task)

    for task in tasks:
        await task


if __name__ == "__main__":
    asyncio.run(main())
