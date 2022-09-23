from fast_api_project.card import Card
import pytest


class TestCard:
    @classmethod
    def test_retrieve_from_str(cls):
        li = Card.retrieve_from_str("he13&sp8")
        assert li[0].json() == '{"suite": "he", "number": 13, "strength": 10}'
        assert li[1].json() == '{"suite": "sp", "number": 8, "strength": 5}'
