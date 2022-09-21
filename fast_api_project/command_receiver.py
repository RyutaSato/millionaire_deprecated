import sys
import asyncio
import websockets
import threading
import logging
from concurrent.futures import Future

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)


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


async def websocket_client():
    async with websockets.connect("ws://127.0.0.1:8000/ws?token=01835c3a-fb3d-b4e2-a43e-1682dc0be131") as ws:
        while True:
            message = await async_readline()
            logger.debug("received: " + message)
            if message == "exit":
                break
            await ws.send(message)

if __name__ == "__main__":
    asyncio.run(websocket_client())
