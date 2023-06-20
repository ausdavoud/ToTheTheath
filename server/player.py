import socket
from pydantic import BaseModel
from typing import Any

class Player(BaseModel):
    socket: Any
    address: Any
    current_move: str = None
    match_id: int = None
    index: int = None
    character: Any
    name: str = None
    health: int = 100
    magic: int = 100
    magic_limit: int = 100
    
    def decrease_health(self, value):
        if self.health - value > 0:
            self.health -= value
        else:
            self.health = 0

    def increase_magic(self):
        reset_rate = self.character.magic_reset_rate
        if self.magic + reset_rate < self.magic_limit:
            self.magic += reset_rate
        else:
            self.magic = self.magic_limit

    def send(self, msg):
        try:
            self.socket.sendall(msg.encode('utf-8'))
        except socket.error as e:
            raise e

    def receive(self, data_length=1024):
        try:
            return self.socket.recv(data_length).decode('utf-8')
        except socket.error as e:
            raise e
