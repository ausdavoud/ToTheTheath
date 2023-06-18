class Player:
    def __init__(self, character):
        self.health = 100
        self.magic = 100
        self.magic_limit = 100
        self.character = character

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
