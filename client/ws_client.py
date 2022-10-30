import asyncio
import contextlib
from asyncio import Event

from websockets.exceptions import ConnectionClosed
import json

from client.async_ import async_readline
from client.user_data import UserData
from types_both import *
from types_nt import *
from ws_request_model import *
from ws_notify_model import *
import send_cmd

COMMAND_LINE = True
SLEEP_INTERVAL = 1.0
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


@contextlib.asynccontextmanager
async def conn_watcher():
    while True:
        try:
            yield
        except ConnectionClosed:
            logger.debug("Connection was closed.")
            break
        except asyncio.exceptions.CancelledError:
            logger.debug("task was cancelled.")


def _message_parser(string: str):
    json_ = json.loads(string)
    match json_.get("nt_type"):
        case "play":
            mdl_cls = NtPlayTypes.get([json_["pl_type"]])
        case _:
            mdl_cls = NtTypes.get(json_["nt_type"])
    if mdl_cls is None:
        return None
    return mdl_cls(json_)


class WebSocketClient:
    def __init__(self, ws):
        self._name: str = "loading..."
        self._status: UserStatusType = UserStatusType.Lobby
        self.data: UserData | None = None
        self.send_que = asyncio.Queue()
        self.recv_que = asyncio.Queue()
        loop = asyncio.get_running_loop()
        self._task_send = loop.create_task(self._send_que())
        self._task_recv = loop.create_task(self._recv_que())
        self.ws = ws
        self.flag_matched: Event | None = None
        self.flag_loaded: Event | None = None

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, new_name: str):
        logger.info(f"name was changed from'{self._name}' to '{new_name}'")
        self._name = new_name

    @property
    def status(self):
        return self._status

    @status.setter
    def status(self, new_status: UserStatusType):
        """
        statusの変更はサーバーからの通知からのみ変更できる。
        """
        logger.info(f"requested: status was changed from'{self._status}' to '{new_status}'")
        self._status = new_status
        if new_status == UserStatusType.InGame:
            self.flag_matched.set()

    def send_nowait(self, model):
        self.send_que.put_nowait(model.json())

    async def send(self, model):
        await self.send_que.put(model.json())

    async def rq_change_status(self, new_status: UserStatusType):
        logger.info("rq_change_status is called")
        match new_status:
            case UserStatusType.Lobby:
                self.data.play_reset()
            case UserStatusType.QueueIn:
                self.flag_matched = asyncio.Event()
            case UserStatusType.InGame:
                self.flag_matched.set()
                self.flag_loaded = asyncio.Event()
            case _:
                logger.error("exception: rq_change_status got no match type {}".format(new_status))

        await self.send(RqChangeStatusUser(status_type=new_status))

    async def matched(self):
        await self.flag_matched.wait()
        self.flag_matched.clear()
        logger.info("matched waiting for game data...")
        await self.flag_loaded.wait()

    async def play_my_turn(self):
        await self.data.flag_my_turn.wait()
        self.data.flag_my_turn.clear()
        await self.rq_pull_card()

    async def play(self):
        task_play = asyncio.create_task(self._play())
        asyncio.get_running_loop().run_until_complete(task_play)

    async def _play(self):
        while True:
            await self.play_my_turn()

    async def rq_pull_card(self):
        logger.info("pull_card is called.")
        selected_cards = self.data.choice_one_card()
        logger.info("selected_cards: {}".format(",".join([str(card) for card in selected_cards])))
        await self.send(RqOpePullCards(cards=selected_cards))

    @conn_watcher()
    async def _send_que(self):
        """
        この関数は、キューから取り出したmessage文字列を送信する。
        """
        message = await self.send_que.get()
        logger.info("send: message: {}".format(message))
        if message.startswith("\n"):
            await self.ws.close()
        await asyncio.sleep(SLEEP_INTERVAL)
        await self.ws.send(message)

    @conn_watcher()
    async def _recv_que(self):
        message = await self.ws.recv()
        logger.info(f"received message: {message}")
        nt_cls = _message_parser(message)
        if nt_cls is None:
            # 例外処理は_message_parser()でされているため何もしない。
            return
        if not hasattr(nt_cls, "reflect"):
            logger.error(f"{nt_cls} doesn't have attribute 'reflect'")
            return
        nt_cls.reflect(self.data)

    async def _end_process(self):
        pass
