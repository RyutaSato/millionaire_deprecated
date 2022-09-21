import sys
from datetime import datetime
from multiprocessing import freeze_support
from uuid import UUID

import ulid

from fast_api_project.command import Command, OperationEnum
from fast_api_project.player import Player
from fast_api_project.card import Card, CardSuite
from random import shuffle
import logging
from pydantic import BaseModel
from fast_api_project.config import Config
from queue import Queue
from threading import Thread

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


def cards_from_str(player: Player, str_cards: str) -> list[Card]:
    li_cards = str_cards.split("&")
    cards = []
    for str_card in li_cards:
        num = str_card[1:]
        if not num.isnumeric():
            raise InvalidInputException(
                player.ulid, msg=str_cards, is_skipped=True, reason="card number format is wrong.")
        num = int(num)
        if str_card[0] == 's':
            suite = CardSuite.SPADE
        elif str_card[0] == 'c':
            suite = CardSuite.CLOVER
        elif str_card[0] == 'd':
            suite = CardSuite.DIAMOND
        elif str_card[0] == 'h':
            suite = CardSuite.HEART
        else:
            raise InvalidInputException(
                player.ulid, msg=str_cards, is_skipped=True, reason="card suite format is wrong.")
        card = Card(suite=suite, number=num, strength=Card.set_strength(num))
        logger.debug("{} are selected.".format(str(card)))
        # if not card in player.cards:
        #     raise InvalidInputException(
        #         player.ulid, msg=str_cards, is_skipped=True, reason="player don't have this card {}".format(card))
        # player.cards.pop(player.cards.index(card))
        cards.append(card)
    return cards


class Board(BaseModel):
    id: UUID = ulid.new().uuid
    created_at: datetime = datetime.now()
    config: Config = Config()
    players: list[Player]
    discards: list[Card] = []

    def play(self):
        logger.debug("this game is started.")
        que = Queue()
        input_thread = Thread(target=self.input_command, args=(que,))
        do_thread = Thread(target=self.do_command, args=(que,))
        input_thread.start()
        do_thread.start()
        logger.debug("this game is finished.")

    def input_command(self, que: Queue):
        """
        input example:
            exit
            pull s3&d3
            give d7&c7 target1&target2
        """
        while True:
            for player in self.players:
                logger.debug("{0} is turn".format(player.ulid))
                self.logging_specific_status()
                str_cmds: list[str] = list(input().split(","))
                for str_cmd in str_cmds:
                    list_cmd = str_cmd.split()
                    if list_cmd[0] == "exit":
                        que.put(None)
                        return
                    if len(list_cmd) == 2:
                        que.put(Command(
                            player=player,
                            cards=cards_from_str(player, list_cmd[1]),
                            operation=OperationEnum[list_cmd[0]]))
                    elif len(list_cmd) == 3:
                        targets = [self.player_from_uuid(UUID(target)) for target in list_cmd[2].split("&")]
                        que.put(Command(
                            player=player,
                            cards=cards_from_str(player, list_cmd[1]),
                            targets=targets,
                            operation=OperationEnum[list_cmd[0]]))
                    else:
                        raise InvalidInputException(player.ulid, is_skipped=True)
                logger.debug("que is {}".format(str(que.empty())))

    def do_command(self, que: Queue):
        logger.debug("do_command is started")
        while True:
            logger.debug("waiting queue in...")
            cmd: Command | None = que.get()
            logger.debug("{} command got.".format(cmd))
            if cmd is None:
                break
            if cmd.operation == OperationEnum.pull:
                logger.debug("pull is selected")
                for card in cmd.cards:
                    cmd.player.cards.pop(cmd.player.cards.index(card))
                    self.discards.append(card)
            elif cmd.operation == OperationEnum.skip:
                logger.debug("skip is selected")
            else:
                raise InvalidInputException(
                    cmd.player.ulid,
                    is_skipped=True,
                    reason="command format is invalid")
            logger.debug("command is done.")

    def player_from_uuid(self, ulid_: UUID) -> Player:
        for player in self.players:
            if ulid_ == player.ulid:
                return player
        raise InvalidInputException(ulid_, msg="Player with ulid {} does not exit.".format(ulid_))

    def distribute_cards(self) -> None:
        while self.discards:
            for player in self.players:
                if self.discards:
                    player.cards.append(self.discards.pop())

    def shuffle_cards(self) -> None:
        shuffle(self.discards)

    def logging_specific_status(self):
        logger.info("****** board_id: {0} ******".format(self.id))
        logger.info("created time: {0} ".format(self.created_at))
        logger.info("******* discards status *******")
        cnt = 0
        if self.discards:
            cards_str = []
            for card in self.discards:
                cards_str.append(str(card))
                cnt += 1
                if cnt % 11 == 0:
                    logger.info(", ".join(cards_str))
                    cards_str = []
        else:
            logger.info("No cards")
        logger.info("****** EACH PLAYER STATUS *****")
        for player in self.players:
            if player.cards:
                player.print_status()
            else:
                logger.info("player: {} No cards".format(player.ulid))


if __name__ == '__main__':
    pass
