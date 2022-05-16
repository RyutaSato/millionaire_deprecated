from fastapi import WebSocket


class User:
    def __init__(self, websocket: WebSocket, name):
        self.ws = websocket
        self.name = name
