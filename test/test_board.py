import os
import sys
import unittest
import ulid


from fast_api_project.board import Board

class BoardTest(unittest.TestCase):
    def setUp(self) -> None:
        sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
        self.ULIDS = ['01G2VK93KPT13CAHPZQMCV2VNH', '01G2VKC3FYY2ZM2V1C3YAPETBT',
                      '01G2VKC68XDB5TM09G0T921G31', '01G2VKC7GNTAE57SA65BCP3V70']

        self.player = Board(self.ULIDS)
    def tearDown(self) -> None:
        del self.player
