import asyncio
from websockets.exceptions import ConnectionClosed
import json

from client.async_ import async_readline
from client.user_data import UserData
from types_nt import NtTypes, NtPlayTypes
from ws_request_model import *
from ws_notify_model import *
import send_cmd

COMMAND_LINE = True
SLEEP_INTERVAL = 1.0
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def _message_parser(string: str):
    try:
        json_ = json.loads(string)
        if json_["nt_type"] == "play":
            return NtPlayTypes[json_["pl_type"]](json_)
        return NtTypes[json_["nt_type"]](json_)
    except ValueError as err:
        logger.error(err)
        logger.error(string)
        return None


class WebSocketClient:
    def __init__(self, ws):
        self.data = UserData()
        self.send_que = asyncio.Queue()
        self.recv_que = asyncio.Queue()
        loop = asyncio.get_running_loop()
        self._task_send = loop.create_task(self._send_que())
        self._task_recv = loop.create_task(self._recv_que())
        self.ws = ws

    def send_nowait(self, message: str):
        self.send_que.put_nowait(message)

    async def send(self, message: str):
        await self.send_que.put(message)

    def pull_card(self):
        logger.info("pull_card is called.")
        selected_cards = self.data.choice_one_card()
        logger.info("selected_cards: {}".format(",".join([str(card) for card in selected_cards])))
        self.send_nowait(RqOpePullCards(cards=selected_cards).json())

    async def _send_que(self, is_readline=False):
        """
        この関数は、キューから取り出したmessage文字列を送信する。
        """
        while True:
            if is_readline:
                message = await async_readline()
            else:
                message = await self.send_que.get()
            logger.info("send: message: {}".format(message))
            if message.startswith("\n"):
                await self.ws.close()
                break
            await asyncio.sleep(SLEEP_INTERVAL)
            await self.ws.send(message)
        self._task_send.set_result(None)

    async def _recv_que(self, is_model=True):
        while True:
            try:
                message = await self.ws.recv()
            except ConnectionClosed:
                break
            logger.info(f"received message: {message}")
            nt_cls = _message_parser(message)
            if not is_model or nt_cls is None:
                # 例外処理は_message_parser()でされているため何もしない。
                continue
            if not hasattr(nt_cls, "reflect"):
                logger.error(f"{nt_cls} doesn't have attribute 'reflect'")
                pass
            nt_cls.reflect(self.data)

        self._task_recv.set_result(None)
