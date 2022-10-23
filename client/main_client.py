import asyncio

import websockets

from client.ws_client import WebSocketClient


async def main():
    async with websockets.connect("ws://127.0.0.1:8000/ws?token=01835c3a-fb3d-b4e2-a43e-1682dc0be131") as ws:
        client = WebSocketClient(ws)
        # :TODO クライアントの動作を書く(high priority)


if __name__ == "__main__":
    asyncio.run(main())
