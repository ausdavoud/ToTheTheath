class Character:
    def __init__(self, name, magic_rate, strike_rate, defence_rate, magic_reset_rate, power):
        self.name = name
        self.health = 100
        self.magic = 100
        self.magic_rate = magic_rate
        self.strike_rate = strike_rate
        self.defence_rate = defence_rate
        self.magic_reset_rate = magic_reset_rate
        self.power = power

    def reduce_health(self, value):
        if self.health > value:
            self.health -= value
        else:
            self.health = 0

    def increase_magic(self):
        self.magic += self.magic_reset_rate
