import asyncio
import sys
import threading
import logging
from concurrent.futures import Future


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
