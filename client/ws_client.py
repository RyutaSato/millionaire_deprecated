import asyncio
import contextlib
from asyncio import Event
import websockets
from websockets.exceptions import ConnectionClosed
import json

from types_both import *
from types_nt import *
from ws_request_model import *
from ws_notify_model import *
from client.async_ import async_readline
from client.user_data import UserData
import send_cmd

SLEEP_INTERVAL = 1.0
MAX_QUE_SIZE = 3
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def conn_watcher(func):
    async def _conn_watcher(*args, **kwargs):
        try:
            await func(*args, **kwargs)
        except ConnectionClosed:
            logger.debug("Connection was closed.")
        except asyncio.CancelledError:
            logger.debug("task was cancelled.")

    return _conn_watcher


def _parse_message(string: str):
    json_ = json.loads(string)
    match json_.get("nt_type"):
        case "play":
            mdl_cls = NtPlayTypes.get([json_["pl_type"]])
        case _:
            mdl_cls = NtTypes.get(json_["nt_type"])
    if mdl_cls is None:
        return None
    return mdl_cls(json_)


class ClientConnectionManager:
    # Before initialized
    future = asyncio.Future()

    def __init__(self, token: str):
        loop = asyncio.get_running_loop()
        self.send_que = asyncio.Queue(maxsize=MAX_QUE_SIZE)
        self.recv_que = asyncio.Queue(maxsize=MAX_QUE_SIZE)
        self._ws = websockets.connect(f"ws://127.0.0.1:8000/ws?token={token}")
        self._task_send = loop.create_task(self._send())
        self._task_recv = loop.create_task(self._recv())

    @conn_watcher
    async def _send(self):
        """
        この関数は、キューから取り出したmessage文字列を送信する。
        """
        while True:
            message = await self.send_que.get()
            logger.info("send: message: {}".format(message))
            if message.startswith("\n"):
                await self._ws.close()
            await asyncio.sleep(SLEEP_INTERVAL)
            await self._ws.send(message)

    @conn_watcher
    async def _recv(self):
        while True:
            message = await self._ws.recv()
            await self.recv_que.put(message)

    @conn_watcher
    async def _parse_recv_que(self):
        while True:
            message = await self.recv_que.get()
            logger.info(f"_parse_recv_que got this:{message}")
            nt_cls = _parse_message(message)

    def send(self, func):
        """
        async method
        このメソッドはdecoratorとして呼び出され、呼び出し元の関数の返り値は、そのまま、送信キューに追加される。
        """

        async def _create_msg_from_model(*args, **kwargs):
            mdl = func(*args, **kwargs)
            await self.send_que.put(mdl.json())

        return _create_msg_from_model


class WebSocketClient:
    def __init__(self, token: str):
        self._conn = ClientConnectionManager(token)
        self.data: UserData | None = None
        self._name: str = "loading..."
        self._status: UserStatusType = UserStatusType.Lobby
        loop = asyncio.get_running_loop()
        self._task_play = loop.create_task(self._play())
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

    async def rq_change_status(self, new_status: UserStatusType):
        logger.info("rq_change_status is called")
        match new_status:
            case UserStatusType.Lobby:
                self.data = UserData()
            case UserStatusType.QueueIn:
                self.flag_matched = asyncio.Event()
            case UserStatusType.InGame:
                self.flag_matched.set()
                self.flag_loaded = asyncio.Event()
            case _:
                logger.error("exception: rq_change_status got no match type {}".format(new_status))

        return RqChangeStatusUser(status_type=new_status)

    async def matched(self):
        await self.flag_matched.wait()
        self.flag_matched.clear()
        logger.info("matched waiting for game data...")
        await self.flag_loaded.wait()

    async def play_my_turn(self):
        await self.data.flag_my_turn.wait()
        self.data.flag_my_turn.clear()  # Eventのlockをクリアする

        selected_cards = self.data.choice_one_card()
        await self.rq_pull_card(selected_cards)

    async def play(self):
        task_play = asyncio.create_task(self._play())
        await task_play

    @conn_watcher
    async def _play(self):
        # play前処理
        await self.flag_loaded.wait()
        while True:
            await self.play_my_turn()

    # :TODO クライアントの動作を書く(high priority)
    async def rq_pull_card(self, selected_cards):
        logger.info("pull_card is called.")
        logger.info("selected_cards: {}".format(",".join([str(card) for card in selected_cards])))
        return RqOpePullCards(cards=selected_cards)

    @conn_watcher
    async def _send_que(self):
        """
        この関数は、キューから取り出したmessage文字列を送信する。
        """
        while True:
            message = await self.send_que.get()
            logger.info("send: message: {}".format(message))
            if message.startswith("\n"):
                await self.ws.close()
            await asyncio.sleep(SLEEP_INTERVAL)
            await self.ws.send(message)

    @conn_watcher
    async def _recv_que(self):
        while True:
            message = await self.ws.recv()
            logger.info(f"received message: {message}")
            nt_cls = _parse_message(message)
            if nt_cls is None:
                # 例外処理は_message_parser()でされているため何もしない。
                return
            if not hasattr(nt_cls, "reflect"):
                logger.error(f"{nt_cls} doesn't have attribute 'reflect'")
                return
            nt_cls.reflect(self.data)

    async def _end_process(self):
        self._task_play.cancel()
        self._task_send.cancel()
        self._task_recv.cancel()
        self.flag_matched = None
        self.flag_loaded = None
        self.data = None
