from datetime import datetime
from uuid import UUID

import ulid

from command import Command, OperationEnum
from player import Player
from card import Card, CardSuite
from random import shuffle
import logging
from pydantic import BaseModel
from config import Config
from queue import Queue

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
        self.input_command(que)
        self.do_command(que)
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
                self.print_specific_status()
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

    def do_command(self, que: Queue):
        while True:
            cmd: Command | None = que.get()
            if cmd is None:
                break
            if cmd.operation == OperationEnum.pull:
                cmd.player.cards.pop(cmd.player.cards.index(*cmd.cards))
                self.discards.append(*cmd.cards)
            elif cmd.operation == OperationEnum.skip:
                pass
            else:
                raise InvalidInputException(
                    cmd.player.ulid,
                    is_skipped=True,
                    reason="command format is invalid")

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

    def create_cards(self) -> None:
        for suite in range(1, 5):
            for number in range(1, 14):
                self.discards.append(Card(suite=suite, number=number, strength=(number + 10) % 13))

    def shuffle_cards(self) -> None:
        shuffle(self.discards)

    def print_specific_status(self):
        print("****** board_id: {0} ******".format(self.id))
        print("created time: {0} ".format(self.created_at))
        print("******* discards status *******")
        cnt = 0
        if self.discards:
            for card in self.discards:
                print(card, end=", ")
                cnt += 1
                if cnt % 11 == 0:
                    print()
            print()
        else:
            print("No cards")
        print("****** EACH PLAYER STATUS *****")
        for player in self.players:
            if player.cards:
                player.print_status()
            else:
                print("player: {} No cards".format(player.ulid))
        print()
        print()

    # TEST METHODS
    @staticmethod
    def test_create_board():
        return Board(players=[Player.test_create_player() for _ in range(4)])

    @staticmethod
    def test_init_board_all():
        board = Board.test_create_board()
        print("Board instance is created.")
        board.print_specific_status()
        board.create_cards()
        print("ran Board.create_cards")
        board.print_specific_status()
        board.shuffle_cards()
        print("ran Board.shuffle_cards")
        board.print_specific_status()
        board.distribute_cards()
        print("ran Board.distribute_cards")
        board.print_specific_status()
        return board


if __name__ == '__main__':
    board = Board.test_init_board_all()
    board.play()
