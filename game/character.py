import pydantic


class Character(pydantic.BaseModel):
    name: str
    power: int
    magic_rate: int
    strike_rate: int
    defence_rate: int
    magic_reset_rate: int

    def get_stats(self):
        return {
            "Name": self.name,
            "Power": self.power,
            "Magic Rate": self.magic_rate,
            "Strike Rate": self.strike_rate,
            "Defence Rate": self.defence_rate,
            "Magic Reset Rate": self.magic_reset_rate
        }


harry_potter_info = {
    "name": "Harry Potter",
    "power": 14,
    "magic_rate": 12,
    "strike_rate": 45,
    "defence_rate": 60,
    "magic_reset_rate": 3,
}

someone_info = {
    "name": "Someone Else",
    "power": 15,
    "magic_rate": 12,
    "strike_rate": 70,
    "defence_rate": 40,
    "magic_reset_rate": 5,
}

harry_potter = Character(**harry_potter_info)
someone = Character(**someone_info)
characters = [harry_potter, someone]


def find_character(name):
    for character in characters:
        if character.name == name: return character
