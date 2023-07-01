from pydantic import BaseModel


class Player(BaseModel):
    health: int = 100
    magic: int = 100
    magic_limit: int = 100
    character: dict
    fight_result: list = []
