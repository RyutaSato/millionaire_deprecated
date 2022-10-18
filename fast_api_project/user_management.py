import asyncio
from uuid import UUID

from fastapi import WebSocket, status
from starlette.websockets import WebSocketDisconnect

from db_config import SessionLocal
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

    def __init__(self, ulid_: UUID, websocket: WebSocket):
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

    async def __aenter__(self):
        await self._ws.accept()
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        if exc_type is not WebSocketDisconnect:
            await self._disconnected()

    @property
    def ulid(self):
        return self._ulid

    async def user_event_loop(self):
        await asyncio.gather(self._get_queue_loop(),
                             self._get_queue_loop())

    async def send(self, msg):
        await self._send_que.put(msg)

    async def _receive_message_loop(self):
        try:
            while True:
                # :TODO Replace _ws.receive_text() with _ws.receive_json()
                message = await self._ws.receive_text()
                logger.debug("ulid: {} message: {}".format(self.ulid, message))
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
                        logger.error(e)
                        await self._ws.send_text(str(data))
        except WebSocketDisconnect:
            await self._disconnected()

    async def _disconnected(self, reason: str = ""):
        """
        この関数は切断処理を行います。切断要因がクライアント側、サーバー側かは問いません。
        通常、WebSocketDisconnectのexceptionの中で呼ばれます。
        """
        logger.debug("WebSocket disconnected ulid_:{} reason:{}".format(self._ulid, reason))
        await self._ws.close()
        manager.disconnect(self._ws)
