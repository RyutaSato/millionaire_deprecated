from fast_api_project.card import Card
import pytest


class TestCard:

    def test_create_cards(self):
        assert len(Card.create_cards(is_shuffle=True)) == 54
        cards = Card.create_cards(is_shuffle=False, joker_num=3)
        cards.sort()
        cnt = 0
        for i in [3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 1, 2]:
            for _ in range(4):
                assert cards[cnt].number == i
                cnt += 1

    def test_create_from_str(self):
        # case1: 全てValueError
        case1 = ["jo", "jo1", "sp0", "sp14"]

        # case2: 各Cardクラスのstrengthは，result2に一致
        case2 = ["jo0", "sp3", "he13", "di6", "cl1", "cl2", "cl3"]
        result2 = [100, 0, 10, 3, 11, 12, 0]
        sorted_cards = ["sp3", "cl3", "di6", "he13", "cl1", "cl2", "jo0"]
        cards = []

        for string in case1:
            with pytest.raises(ValueError):
                Card.create_from_str(string)

        for ca, res in zip(case2, result2):
            card = Card.create_from_str(ca)
            cards.append(card)
            assert ca == str(card)
            assert res == card.strength

        for card in cards[1:]:
            assert cards[0] > card
        for card, sorted_card in zip(sorted(cards), sorted_cards):
            assert sorted_card == str(card)
        with pytest.raises(NotImplementedError):
            if cards[0] >= case2[0]:
                print("success")
        with pytest.raises(NotImplementedError):
            if cards[0] != case2[0]:
                print("success")
