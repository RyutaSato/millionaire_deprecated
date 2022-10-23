import asyncio
from websockets.exceptions import ConnectionClosed
import json

from client.async_ import async_readline
from client.user_data import UserData
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
        return RqTypes[json_["command"]](json_)
    except ValueError as err:
        logger.error(err)
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

    def add_que(self, message: str):
        self.send_que.put_nowait(message)

    def pull_card(self):
        logger.info("pull_card is called.")
        selected_cards = self.data.choice_one_card()
        logger.info("selected_cards: {}".format(",".join([str(card) for card in selected_cards])))
        self.add_que(RqOpePullCards(cards=selected_cards).json())

    async def _send_que(self, is_readline=False):
        self.add_que(RqGetStatusUser().json())
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
            cmd_cls = _message_parser(message)
            if not is_model or cmd_cls is None:
                # 例外処理は_message_parser()でされているため何もしない。
                continue

        self._task_recv.set_result(None)
