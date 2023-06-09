import pydantic

class Character(pydantic.BaseModel):
    name: str
    power: int
    magic_rate: int
    strike_rate: int
    magic: int = 100
    health: int = 100
    defence_rate: int
    magic_reset_rate: int
        
    def reduce_health(self, value: int) -> None:
        if self.health > value:
            self.health -= value
        else:
            self.health = 0

    def increase_magic(self) -> None:
        self.magic += self.magic_reset_rate