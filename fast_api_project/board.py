from multiprocessing import freeze_support
from uuid import UUID

from fast_api_project.cards import Cards
from fast_api_project.player import Player
import logging

DEBUG = True
if DEBUG:
    logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)


class InvalidInputException(Exception):
    def __init__(self, ulid_: UUID, msg: str = "", is_skipped: bool = False, reason: str = "Invalid Input"):
        self.ulid = ulid_
        self.msg = msg
        self.is_skipped = is_skipped
        self.reason = reason
        logger.error("{} {}".format(self.reason, self.msg))

    def __str__(self):
        if self.is_skipped:
            return "{} {}".format(self.reason, self.msg), "player {} is skipped.".format(self.ulid)
        return "{} {}".format(self.reason, self.msg)


class Board:
    def __init__(self, players: list[Player], is_shuffle=True, joker_num=2):
        self.discard = Cards.create_cards(is_shuffle=is_shuffle, joker_num=joker_num)
        self.on_board = Cards()
        self.players = players
        self._turn = 0
        self._passed_flag_total = 0
        for i in range(len(self.discard)):  # self.players[].connection_status 実装後はオンラインのみ
            self.players[i % len(self.players)].cards.add(self.discard.pop())

    def __len__(self):
        return len([pl for pl in self.players if len(pl) > 0])

    def _reset_passed_flag(self):
        self._passed_flag_total = 0
        next_player = 0
        for i in range(len(self.players)):
            if self.players[i].passed:
                self.players[i].passed = False
            else:
                next_player = i
        return next_player

    @classmethod
    def test_init(cls):
        players = [Player(uuid=UUID("01835c3a-fb3d-b4e2-a43e-1682dc0be131"), name="test1"),
                   Player(uuid=UUID("01835c3a-fb3d-832f-27eb-0126cee681e9"), name="test2"),
                   Player(uuid=UUID("01835c3a-fb3d-1c2e-8375-a475a429ca89"), name="test3"),
                   Player(uuid=UUID("01835c3a-fb3d-3520-3d79-6534542003b1"), name="test4")]
        return cls(players, is_shuffle=True, joker_num=0)

    def test_run(self):
        while len(self) > 1:
            self._turn += 1
            if self._passed_flag_total >= 3:
                self._turn = self._reset_passed_flag()
                self.discard.add(self.on_board.clear())
            pl = self.players[self._turn % 4]
            logger.info(f"{pl.name}: is turn, cards: {pl.cards()}")
            if pl.passed:
                logger.info(f"{pl.name}: already passed")
                continue
            selected_cards = pl.play_cards(self.on_board())
            logger.info(f"{pl.name}: selected: {selected_cards}")
            if not selected_cards:
                pl.passed = True
                self._passed_flag_total += 1
                logger.info(f"{pl.name} is selected passed")
                continue
            if self.on_board:
                self.discard.add(self.on_board.clear())
            for c in selected_cards:
                self.on_board.add(c)
            logger.info(f"on_board: {self.on_board()}")
            del pl.cards[selected_cards]
            self._turn += 1
            # sleep(1)


# import sys
# from datetime import datetime
# from multiprocessing import freeze_support
# from uuid import UUID
#
# import ulid
# from fastapi.websockets import WebSocket
#
# from fast_api_project.cards import Cards
# from fast_api_project.playeroperation import PlayerOperation, PlayerOperationEnum
# from fast_api_project.player import Player
# from fast_api_project.card import Card, SUITE_LIST
# import logging
# from fast_api_project.config import Config
# from queue import Queue
# from asyncio.queues import Queue
# import asyncio
#
# from fast_api_project.user_management import UserManager
# class Board:
#     id: UUID = ulid.new().uuid
#     created_at: datetime = datetime.now()
#     config: Config = Config()
#     players: list[Player]
#     users: list[UserManager] = []
#     discards: list[Card] = []
#     que = Queue()
#
#     @classmethod
#     async def ws_init(cls, users: list[UserManager]):
#         logger.debug("this game is started.")
#         cls.users = users
#         cls.players = [user.player for user in users]
#         cls.discards = Card.create_cards(is_shuffle=False)
#         return cls
#
#     async def ws_play(self):
#         # :TODO WebSocket用のPlay関数を作成
#         self.distribute_cards()
#         play_loop = asyncio.new_event_loop()
#         do_task = play_loop.create_task(self.do_command(self.que))
#         ws_accept_task = play_loop.create_task(self.ws_accept_command(self.que))
#         await do_task
#         await ws_accept_task
#
#     async def ws_accept_command(self, que):
#         while True:
#             for user in self.users:
#                 await que.join()
#                 logger.debug("{} is turn".format(user.player.ulid_))
#                 await self.ws_broadcast("{} is turn".format(user.player.ulid_))
#                 await user.ws.send_json(user.player.dict())
#                 str_cmds = await user.ws.receive_text()
#                 for str_cmd in str_cmds:
#                     list_cmd = str_cmd.split()
#                     if list_cmd[0] == "exit":
#                         await que.put(None)
#                         return
#                     if len(list_cmd) == 2:
#                         await que.put(PlayerOperation(
#                             player=user.player,
#                             cards=Card.retrieve_from_str(list_cmd[1]),
#                             operation=PlayerOperationEnum[list_cmd[0]]))
#                     elif len(list_cmd) == 3:
#                         targets = [self.player_from_uuid(UUID(target)) for target in list_cmd[2].split("&")]
#                         await que.put(PlayerOperation(
#                             player=user.player,
#                             cards=Card.retrieve_from_str(list_cmd[1]),
#                             targets=targets,
#                             operation=PlayerOperationEnum[list_cmd[0]]))
#                     else:
#                         raise InvalidInputException(user.player.ulid_, is_skipped=True)
#
#     async def ws_broadcast(self, msg: str):
#         for user in self.users:
#             await user.ws.send_text(msg)
#
#     async def play(self):
#         logger.debug("this game is started.")
#         que = Queue()
#         # input_thread = Thread(target=self.input_command, args=(que,))
#         # do_thread = Thread(target=self.do_command, args=(que,))
#         # input_thread.start()
#         # do_thread.start()
#         loop = asyncio.get_running_loop()
#         input_task = loop.create_task(self.input_command(que))
#         do_task = loop.create_task(self.do_command(que))
#         await input_task
#         await do_task
#         logger.debug("this game is finished.")
#
#     async def input_command(self, que: Queue):
#         test_message_cnt = 0
#         """
#         :TODO move to command_receiver.py
#         input example:
#             exit
#             pull sp3&d3
#             give di7&cl7 target1&target2
#         """
#         self.logging_specific_status()
#         while True:
#             for player in self.players:
#                 await que.join()
#                 logger.debug("{0} is turn".format(player.ulid_))
#                 if DEBUG:
#                     message = await test_replies(test_message_cnt)
#                     test_message_cnt += 1
#                 else:
#                     message = await async_readline()
#                 str_cmds: list[str] = message.split(",")
#                 for str_cmd in str_cmds:
#                     list_cmd = str_cmd.split()
#                     if list_cmd[0] == "exit":
#                         await que.put(None)
#                         return
#                     if len(list_cmd) == 2:
#                         await que.put(PlayerOperation(
#                             player=player,
#                             cards=Card.retrieve_from_str(list_cmd[1]),
#                             operation=PlayerOperationEnum[list_cmd[0]]))
#                     elif len(list_cmd) == 3:
#                         targets = [self.player_from_uuid(UUID(target)) for target in list_cmd[2].split("&")]
#                         await que.put(PlayerOperation(
#                             player=player,
#                             cards=Card.retrieve_from_str(list_cmd[1]),
#                             targets=targets,
#                             operation=PlayerOperationEnum[list_cmd[0]]))
#                     else:
#                         raise InvalidInputException(player.ulid_, is_skipped=True)
#                 logger.debug("que is {}".format(str(que.empty())))
#
#     async def do_command(self, que: Queue):
#         logger.debug("do_command is started")
#         while True:
#             logger.debug("waiting queue in...")
#             cmd: PlayerOperation | None = await que.get()
#             logger.debug("{} command got.".format(cmd))
#             if cmd is None:
#                 break
#             if cmd.operation == "pull":
#                 logger.debug("pull is selected")
#                 for card in cmd.cards:
#                     cmd.player.cards.pop(cmd.player.cards.index(card))
#                     self.discards.append(card)
#             elif cmd.operation == PlayerOperationEnum.skip:
#                 logger.debug("skip is selected")
#             else:
#                 logger.error("ValueError: operation command is invalid {}".format(cmd.operation))
#                 raise InvalidInputException(
#                     cmd.player.ulid_,
#                     is_skipped=True,
#                     reason="command format is invalid")
#             logger.debug("command is done.")
#             que.task_done()
#             self.logging_specific_status()
#
#     def player_from_uuid(self, ulid_: UUID) -> Player:
#         for player in self.players:
#             if ulid_ == player.ulid_:
#                 return player
#         raise InvalidInputException(ulid_, msg="Player with ulid_ {} does not exit.".format(ulid_))
#
#     def distribute_cards(self) -> None:
#         for i in range(len(self.discards)):
#             self.players[i % len(self.players)].cards.append(self.discards.pop())
#
#     def logging_specific_status(self):
#         logger.info("****** board_id: {0} ******".format(self.id))
#         logger.info("created time: {0} ".format(self.created_at))
#         logger.info("******* discards status *******")
#         cnt = 0
#         if self.discards:
#             cards_str = []
#             for card in self.discards:
#                 cards_str.append(str(card))
#                 cnt += 1
#                 if cnt % 11 == 0:
#                     logger.info("discards: ", ", ".join(cards_str))
#                     cards_str = []
#             logger.info("discards: " + ", ".join(cards_str))
#         else:
#             logger.info("No cards")
#         logger.info("****** EACH PLAYER STATUS *****")
#         for player in self.players:
#             if player.cards:
#                 player.print_status()
#             else:
#                 logger.info("player: {} No cards".format(player.ulid_))


if __name__ == '__main__':
    freeze_support()
    # players = [Player(uuid=UUID("01835c3a-fb3d-b4e2-a43e-1682dc0be131"), name="test1"),
    #            Player(uuid=UUID("01835c3a-fb3d-832f-27eb-0126cee681e9"), name="test2"),
    #            Player(uuid=UUID("01835c3a-fb3d-1c2e-8375-a475a429ca89"), name="test3"),
    #            Player(uuid=UUID("01835c3a-fb3d-3520-3d79-6534542003b1"), name="test4")]
    # discards = Cards.create_cards(is_shuffle=False)
    # board = Board(
    #     players=players,
    #     discards=discards
    # )
    # board.distribute_cards()
    # loop = asyncio.get_event_loop()
    # loop.run_until_complete(board.play())
