import asyncio
from uuid import UUID

from fastapi import WebSocket, status
from starlette.websockets import WebSocketDisconnect, WebSocketState

from fast_api_project.player import Player
from ws_manage import ConnectionManager
from ws_model_in import *
from asyncio import Queue

manager = ConnectionManager()


class UserManager:
    """
    インスタンスは、websocketのコネクションごとに作成される必要があります。
    このクラスでは、websocketでアクセス,認証後の全ての送信・受信処理を管理します。
    1ユーザーから複数のwebsocketアクセスがあった場合は、古いアクセスを削除します。（未実装）

    """

    def __init__(self, ulid_: UUID, websocket: WebSocket, debug: bool = False):
        self._ulid = ulid_
        self._ws = websocket
        self._send_que = Queue()
        self._receive_que = Queue()
        self._msg_cnt = 0
        self.is_turn = False
        self.player = Player(
            ulid_=ulid_,
            name="test"
        )
        self._debug = debug

    async def __aenter__(self):
        if not self.is_connected:
            await self._ws.accept()
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        await self._disconnected("async with statement called exit")

    @property
    def ulid(self):
        return self._ulid

    @property
    def is_connected(self) -> bool:
        return self._ws.client_state is WebSocketState.CONNECTED

    async def user_event_loop(self):
        await self._connect()
        await asyncio.gather(self._get_queue_loop(),
                             self._receive_message_loop())

    async def send(self, msg):
        """
        messageの型は文字列ではない場合、JSON型にして送信を試みます。
        それが不可能な場合は、str型にキャストして送信します。
        エラーにより接続が閉じられることはありません。
        """
        await self._send_que.put(msg)

    async def _receive_message_loop(self):
        try:
            while True:
                # :TODO Replace _ws.receive_text() with _ws.receive_json()
                message = await self._ws.receive_text()
                if self._debug:
                    logger.debug("ulid: {} message: {}".format(self.ulid, message))
                    await self._send_que.put(message)
        except WebSocketDisconnect:
            await self._disconnected()

    async def _get_queue_loop(self):
        try:
            while True:
                data = await self._send_que.get()
                if data is None:
                    await self._disconnected("WebSocket is disconnected because server message queue got None object.")
                    raise WebSocketDisconnect
                if type(data) is str:
                    await self._ws.send_text(data)
                else:
                    try:
                        await self._ws.send_json(data)
                    except Exception as e:
                        logger.error(f"{e} json decode is failure")
                        logger.error(str(data))
                        await self._ws.send_text(str(data))
        except WebSocketDisconnect:
            await self._disconnected()

    async def _connect(self):
        if not self.is_connected:
            await self._ws.accept()

    async def _disconnected(self, reason: str = "disconnected by client"):
        """
        この関数は切断処理を行います。切断要因がクライアント側、サーバー側かは問いません。
        通常、WebSocketDisconnectのexceptionの中で呼ばれます。
        """
        logger.debug("WebSocket disconnected ulid_:{} reason:{}".format(self._ulid, reason))
        if self.is_connected:
            await self._ws.close()
        # manager.disconnect(self._ws)
