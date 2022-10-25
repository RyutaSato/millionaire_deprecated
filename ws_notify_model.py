"""
クラスルール：
    ・全てのモデルクラスはWebSocketNtクラスを継承する。
    ・全てのモデルクラスはNtTypeのプロパティに追加する。
    ・全てのモデルクラスはNtTypes辞書のvalueに追加する。
    ・ユーザーの情報に変更があった場合はサーバー側から一方的に通知する。
命名ルール：
    ・"Nt" + "対象(外)" + "対象(内)"
    ・対象
        Status: アクセスしているクライアントの状態(queue中、ゲーム中など)
            status: lobby, queue_in, matched, in_game
        Profile: 要求されたユーザーの情報

        Play:
            player: players[?]
            cards: [card1, card2, ...]
            operation: ("pull", "give", ...)
            target: 0 or players[?] or [player[?], player[?]]

        StatusGame: ゲームの全体の状態（ゲーム開始時、再接続時、デバッグ時使用）
            players:    [player1, player2, ...]
            discards:   [card1, card2, ...]
            cards:      [card1, card2, ...]

"""
import logging
from datetime import datetime, timedelta
from abc import abstractmethod, ABCMeta
from pydantic import BaseModel

from client.user_data import UserData
from fast_api_project.card import Card
from fast_api_project.player import Player
from user import UserOut
from types_nt import NtType
from types_both import GameOperationType

logger = logging.getLogger(__name__)


class _WebSocketNotify(BaseModel, metaclass=ABCMeta):
    """
    このクラスは、サーバーからクライアントへ送る文字列を構成するためのベースモデルです。
    このクラスは抽象クラスであり、インスタンス化しません。
    """
    sent_at: datetime = datetime.now()
    nt_type: NtType
    error: bool = False

    @abstractmethod
    def reflect(self, data: UserData):
        pass

    def ping(self) -> timedelta:
        return datetime.now() - self.sent_at

    class Config:
        use_enum_values = True


class NtStatus(_WebSocketNotify):
    """
    このクラスは、接続時、ユーザー情報に変更があった場合に送信されるモデルです。
    このクラスには、ユーザーが所有できる全ての情報を含んでいる必要があります。

    """

    def reflect(self, data: UserData):
        data.name = self.user.name

    nt_type = NtType.Status
    user: UserOut


class NtStatusGame(_WebSocketNotify):
    """
    ゲーム全体の状態通知
    プロパティはゲーム盤面を完全に再現できる必要十分な情報がそろっている必要があります。
    このクラスは、ゲーム開始時、再接続時、デバッグ時に使用されます。
    """

    def reflect(self, data: UserData):
        data.discards = self.discards
        data.field = self.field
        data.players = self.players

    nt_type = NtType.Game
    discards: list[Card]
    field: list[Card]
    players: list[int]


class _WebSocketNotifyPlay(_WebSocketNotify, metaclass=ABCMeta):
    """
    このクラスはWebSocketNotifyを継承した、ゲーム中の操作通知のみに特化したクラスです。
    このクラスは抽象クラスであり、インスタンス化しません。
    """

    nt_type = NtType.Play
    pl_type: GameOperationType
    player: int
    targets: list[int]
    cards: list[Card]


class NtProfile(_WebSocketNotify):
    # :TODO 未完成
    nt_type = NtType.Profile

    def reflect(self, data: UserData):
        pass


class NtPlayPullCards(_WebSocketNotifyPlay):
    pl_type = GameOperationType.pull
    targets = []

    def reflect(self, data: UserData):
        if data.number == self.player:
            data.pull_cards(self.cards, True)
        else:
            data.pull_cards(self.cards, False)

# class ErrorHandleModelNotify(_WebSocketNotify):
#     @validator("error")
#     def check_error_flag(cls):
#         if not cls.error:
#             logger.error("An instance of ErrorHandleModel class was created even though no error flag was set")
#             ValueError()

# class AdmittedModelsIn:
#     def __init__(self):
#         self.err_handle = ErrorHandleModelNotify
#         self.admitted_models: list = [WebSocketNotifyPlaySelectedCards, SelectedLobbyCommandNotify]
#
#     def convert_from_str(self, msg: str):
#         for admitted_model in self.admitted_models:
#             try:
#                 return admitted_model.parse_raw(msg)
#             except TypeError:
#                 logger.debug(f"{admitted_model} is invalid and skipped")
#         return None
#
#     def convert_from_dict(self, dct: dict):
#         for admitted_model in self.admitted_models:
#             try:
#                 return admitted_model(**dct)
#             except TypeError:
#                 logger.debug(f"{admitted_model} is invalid and skipped")
#         return None
