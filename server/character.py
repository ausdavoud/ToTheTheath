from pydantic import BaseModel


class Character(BaseModel):
    name: str
    strike_power: int
    magic_power: int
    magic_rate: int
    strike_rate: int
    defence_rate: int
    magic_reset_rate: int
    special_magic: int
    special_magic_success_rate: int
    light_theme: bool
    background_color: tuple

    def get_stats(self):
        return {
            "Name": self.name,
            "Strike Power": self.strike_power,
            "Magic Power": self.magic_power,
            "Magic Success Rate": self.magic_rate,
            "Strike Success Rate": self.strike_rate,
            "Defence Success Rate": self.defence_rate,
            "Magic Reset Rate": self.magic_reset_rate,
            "Special Magic Power": self.special_magic,
            "Special Magic Success Rate": self.special_magic_success_rate
        }


def find_character(name):
    for character in characters:
        if character.name == name: return character


harry_potter_dict = {
    "name": "Harry Potter",
    "strike_power": 9,
    "magic_power": 14,
    "magic_rate": 35,
    "strike_rate": 70,
    "defence_rate": 45,
    "magic_reset_rate": 13,
    "special_magic": 25,
    "special_magic_success_rate": 50,
    "light_theme": False,
    "background_color": (63, 0, 113) #(191, 249, 253)
}

dumbledore_dict = {
    "name": "Dumbledore",
    "strike_power": 13,
    "magic_power": 17,
    "magic_rate": 65,
    "strike_rate": 70,
    "defence_rate": 55,
    "magic_reset_rate": 7,
    "special_magic": 37,
    "special_magic_success_rate": 49,
    "light_theme": True,
    "background_color": (221, 230, 237) #(200, 253, 191)
}

voldemort_dict = {
    "name": "Voldemort",
    "strike_power": 10,
    "magic_power": 16,
    "magic_rate": 55,
    "strike_rate": 70,
    "defence_rate": 35,
    "magic_reset_rate": 12,
    "special_magic": 33,
    "special_magic_success_rate": 42,
    "light_theme": False,
    "background_color": (33, 53, 85)  #(12, 19, 79)
}

hermione_dict = {
    "name": "Hermione",
    "strike_power": 12,
    "magic_power": 15,
    "magic_rate": 60,
    "strike_rate": 50,
    "defence_rate": 50,
    "magic_reset_rate": 11,
    "special_magic": 30,
    "special_magic_success_rate": 50,
    "light_theme": True,
    "background_color": (255, 226, 226) #(255, 232, 249)
}

harry_potter = Character(**harry_potter_dict)
dumbledore = Character(**dumbledore_dict)
voldemort = Character(**voldemort_dict)
hermione = Character(**hermione_dict)
characters = [harry_potter, dumbledore, voldemort, hermione]
characters_dict = [harry_potter_dict, dumbledore_dict,
                   voldemort_dict, hermione_dict]
