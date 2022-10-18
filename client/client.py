from queue import Queue
from datetime import datetime
import sys
import asyncio
import websockets
import threading
import logging
from concurrent.futures import Future
from ws_model_in import SelectedLobbyCommandIn, LobbyCommandEnum, PlayerSelectedCardsIn, PlayerCommandEnum
from ws_model_out import CommandOutEnum, UserStatusChangedOut, BoardAllStatusOut

COMMAND_LINE = True
logger = logging.getLogger(__name__)

messages = [
    SelectedLobbyCommandIn(command=LobbyCommandEnum.QUEUE_IN),
    SelectedLobbyCommandIn(command=LobbyCommandEnum.QUEUE_CANCEL),
    SelectedLobbyCommandIn(command=LobbyCommandEnum.QUEUE_IN),
    PlayerSelectedCardsIn(command=PlayerCommandEnum.pull, )

]


async def run_as_daemon(func, *args):
    """
    this func can use blocking function as non-blocking function.
    """
    future = Future()
    future.set_running_or_notify_cancel()

    def daemon():
        try:
            result = func(*args)
        except Exception as e:
            future.set_exception(e)
        else:
            future.set_result(result)

    threading.Thread(target=daemon, daemon=True).start()
    return await asyncio.wrap_future(future)


async def async_readline() -> str:
    return await run_as_daemon(sys.stdin.readline)


class WebSocketClient:
    def __init__(self):
        self._player_command = PlayerCommandEnum.pull
        self._lobby_command = LobbyCommandEnum.QUEUE_CANCEL
        self.queue = asyncio.Queue()

    @property
    def created_at(self):
        return datetime.now()

    @property
    def lobby_command(self):
        return self._lobby_command

    @lobby_command.setter
    def lobby_command(self, command: LobbyCommandEnum):
        # setterではクライアントの状態は変更されず、サーバーからのステータス通知により変更する。
        self.queue.put(SelectedLobbyCommandIn(command=command).json())
        self._lobby_command = LobbyCommandEnum.UPDATING


async def send(ws, client: WebSocketClient, is_readline=False):
    while True:
        if is_readline:
            message = await async_readline()
        else:
            message = await client.queue.get()
        print("message:", message)
        if message.startswith("\n"):
            await ws.close()
            return
        await ws.send(message)


async def recv(ws, client: WebSocketClient, is_model=True):
    while True:
        message = await ws.recv()
        print(str(message))
        if is_model:
            command = CommandOutEnum(dict(message)["command"])


async def main():
    client = WebSocketClient()
    async with websockets.connect("ws://127.0.0.1:8000/ws?token=01835c3a-fb3d-b4e2-a43e-1682dc0be131") as ws:
        await asyncio.gather(send(ws, client, True), recv(ws, client, False))


if __name__ == "__main__":
    asyncio.run(main())
