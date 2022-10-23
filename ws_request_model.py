"""
基本方針：

    将来追加予定の機能:
        Rqでは、errorフラグが立っているときのみ受け付けるModelを、
        ErrorHandleModelに切り替え、それ以外の場合は
        期待したModelでのみ受け付ける。
クラスルール：
    ・全てのモデルクラスはWebSocketRqクラスを継承する。
    ・全てのモデルクラスはRqTypeのプロパティに追加する。
    ・全てのモデルクラスはRqType辞書のvalueに追加する。
    ・"Command"は、標準ライブラリのcmdと混在するため使用しない。

命名ルール：
    ・"Rq" + "動詞" + "対象"
    ・操作系モデル     Ope
        ゲーム中のあらゆる操作については、このクラスを用います。
        このクラスモデルをサーバーが受け付けるのは、ゲーム中のみです。
    ・データ取得モデル  Get
        クライアントが保持していない情報をサーバーに要求するために用います。
        このモデルは"ユーザーが「特定の操作」をした場合にのみ"使えます。
        「特定の操作」は以下を含みます。
        接続・再接続、プロフィールの表示、履歴の表示、フレンドの詳細表示など
        ユーザーが接続中に何らかの状態変更、通知がある場合は、
        一方的にサーバーから送信されるため、クライアント自ら一度取得したデータを再度
        要求する必要はありません。
    ・変更モデル     Change
        ゲーム以外のデータに関する変更・操作を行う場合に使用されます。
        サーバーはユーザーごとのクライアントの状態(読み込み中、処理中など)を
        保持しているため、状態が変更になる時には必ず、このモデルを使用して通知します。
        その他、名前の変更、queueの状態変更、ルームの作成などに使用します。

"""
from enum import Enum

from pydantic import BaseModel, validator
from datetime import datetime, timedelta
from fast_api_project.card import Card
import logging

from fast_api_project.player import Player
from ws_types import RqType, RqTypes, UserDataType, GameOperationType

logger = logging.getLogger(__name__)
DEBUG = True


class _WebSocketRequest(BaseModel):
    """
    このクラスは、サーバーからクライアントへ送る文字列を構成するためのベースモデルです。
    このクラスは抽象クラスであり、インスタンス化しません。
    """
    sent_at: datetime = datetime.now()
    rq_type: RqType

    class Config:
        use_enum_values = True


class RqGetStatusUser(_WebSocketRequest):
    rq_type = RqType.GetStatusUser


class RqGetStatusGame(_WebSocketRequest):
    rq_type = RqType.GetStatusGame


class RqChangeStatusUser(_WebSocketRequest):
    """
    ユーザーデータの変更リクエストに使用されます。
    変更タイプを予めしておき、その値を決められた書式で送信します。
    """

    rq_type = RqType.ChangeStatusUser
    status_type: UserDataType


class RqOpePullCards(_WebSocketRequest):
    """
    cardsが空リストの場合、skipを指す。
    """
    rq_type = RqType.Operation
    operation = GameOperationType.pull
    cards: list[Card]


if DEBUG:
    for tmp in RqTypes.keys():
        try:
            RqType(tmp)
        except ValueError as e:
            logger.error(e)
            raise ImportError("RqType lacks keys")
    for tmp in RqType.__dict__.keys():
        if not str(tmp).startswith("_"):
            try:
                tmp_ = RqTypes[tmp]
            except KeyError as e:
                logger.error(e)
                raise ImportError("OutTypes lacks keys")
