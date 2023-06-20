from pydantic import BaseModel
from typing import Any

class Player(BaseModel):
    health: int = 100
    magic: int = 100
    magic_limit: int = 100
    character: Any

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
