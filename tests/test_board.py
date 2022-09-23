import os
import sys

from uuid import UUID
from fast_api_project import board
from fast_api_project.player import Player
import pytest

"""
test command is this:
>>> pytest test_board.py --cov=fast_api_project --cov-report term-missing
"""
print(os.path.dirname(__file__))


class TestBoard:
    @classmethod
    def setup_class(cls) -> None:
        sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
        players = [Player(ulid=UUID("01835c3a-fb3d-b4e2-a43e-1682dc0be131"), name="test1"),
                   Player(ulid=UUID("01835c3a-fb3d-832f-27eb-0126cee681e9"), name="test2"),
                   Player(ulid=UUID("01835c3a-fb3d-1c2e-8375-a475a429ca89"), name="test3"),
                   Player(ulid=UUID("01835c3a-fb3d-3520-3d79-6534542003b1"), name="test4")]
        discards = board.create_cards()
        cls.board = board.Board(
            players=players,
            discards=discards
        )

    @classmethod
    def teardown_class(cls):
        pass

    def test_play(self):
        pass

    def test_input_command(self):
        pass

    def test_distribute_cards(self):
        pass
