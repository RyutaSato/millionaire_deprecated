from typing import List
from player import Player
from card import Card
from random import shuffle
import logging

logger = logging.getLogger(__name__)


class Board:
    MAX_STRENGTH = 100
    DEFAULT_JOKER_NUM = 2
    DEFAULT_PLAYER_NUM = 4
    SUIT_SET = ['Spade', 'Clover', 'Diamond', 'Heart']
    MARK_SET = ['♠', '☘', '♦', '♥']
    STRENGTH = [12, 13, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11]
    DEFAULT_MARK_NUM = len(SUIT_SET)
    DEFAULT_NUMBER_NUM = len(STRENGTH)
    DEFAULT_CARD_NUM = DEFAULT_NUMBER_NUM * DEFAULT_MARK_NUM + DEFAULT_JOKER_NUM
    FUNCTION_333SANDSTORM = False
    FUNCTION_44STOP = False
    FUNCTION_5SKIP = False
    FUNCTION_66NECK = False
    FUNCTION_7GIFT = True
    FUNCTION_8CUT = True
    FUNCTION_99RESQUE = False
    FUNCTION_10THROW = True
    FUNCTION_11BACK = False
    FUNCTION_12BOMBER = False
    FUNCTION_13SKIP = False
    FUNCTION_REVOLUTION = True
    FUNCTION_LOW_LIMIT = True
    FUNCTION_HIGH_LIMIT = True
    FUNCTION_EMPEROR = False

    def __init__(self, ulids: List[str], player_num=DEFAULT_PLAYER_NUM):
        self.player_num = player_num
        self.players = [Player(ulid) for ulid in ulids]
        cards: List[Card] = self._init_cards()
        self._init_players(cards)
        self.card_on_board: List[Card] = []
        self.status = 0
        for i in range(self.player_num):
            self.status |= 1 << i

    def __str__(self) -> str:
        s = ''
        s += f"{'-' * 10} Status {'-' * 10}"
        for player in self.players:
            s += f"cards : {player.cards}"
        s += f"{'-' * 25}"
        return s

    def play_game(self):
        turn_count = 0
        while self.status:
            self._command(turn_count % self.player_num)
            turn_count += 1
            # self.status の処理
            self._broadcast()
        del self

    def _broadcast(self):
        """
        全プレイヤーに盤面と，各プレイヤーの手札の枚数，ステータスを配信する
        json形式
        {
            "status": "normal"
            "board": self.card_on_board[-1].suite + self.card_on_board[-1].order
            "p1":
        }
        :return:
        """
        # broadcast

    def _command(self, current_player_num):
        card = self.players[current_player_num].get_card_from_client_to_board()
        if card is None:
            return
        if not self.card_on_board or card <= self.card_on_board[-1]:
            logger.exception(f"an invalid card was put out from Player {self.players[current_player_num]}"
                             f"the card is {card}")
            self.players[current_player_num].returned_invalid_card_from_board_to_player(card)
        self._add_card_on_board(card)
        # cardを盤面に出す処理
        for func in card.functions:
            func()
            self._broadcast()

    def is_valid_cards(self, current_player_num, index_list) -> bool:
        # not bool but status 連続かつ同じスートあるいは同じ強さであり、盤面より強くなければならない
        num_list = []
        for num in index_list:
            num_list.append(self.players[current_player_num].cards[num].order)

    def is_same_suit(self, current_player_num, index_list) -> bool:
        suit: str = self.players[current_player_num].cards[index_list[0]].suit
        for index in index_list:
            if suit != self.players[current_player_num].cards[index].suit:
                return False
        return True

    def is_same_num(self, current_player_num, index_list) -> bool:
        num: int = self.players[current_player_num].cards[index_list[0]].strength
        for index in index_list:
            if num != self.players[current_player_num].cards[index].strength:
                return False
        return True

    def is_consecutive_num(self, current_player_num, index_list) -> bool:
        num_list = []
        for index in index_list:
            num_list.append(self.players[current_player_num].cards[index].strength)
        num_list.sort()
        for i in range(len(num_list)):
            if num_list[0] + i != num_list[i]:
                return False
        return True

    def _add_joker(self) -> List[Card]:
        return [Card('Joker', '🃏', 0, self.MAX_STRENGTH)] * self.DEFAULT_JOKER_NUM

    def _init_cards(self) -> List[Card]:
        cards = self._add_joker()
        for num in range(self.DEFAULT_NUMBER_NUM):
            for mark in range(self.DEFAULT_MARK_NUM):
                cards.append(Card(self.SUIT_SET[mark], self.MARK_SET[mark], num * 10 + mark + 1, self.STRENGTH[num]))
        shuffle(cards)
        return cards

    def _init_players(self, cards):
        """
        {cards}を各プレイヤー{self.players}に分配する．
        """
        self._broadcast()
        for i in range(self.player_num):
            self.players[i].cards = cards[self.DEFAULT_CARD_NUM * i // self.player_num: \
                                          self.DEFAULT_CARD_NUM * (i + 1) // self.player_num]

    def _add_card_on_board(self, card):
        """
        {card} を {self.card_on_board} Listに追加する -> completed
        各プレイヤーに盤面データをブロードキャストする(async)
        """
        self.card_on_board.append(card)
        self._broadcast()

if __name__ == '__main__':
    import doctest
    doctest.testmod()