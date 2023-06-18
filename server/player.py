import socket


class Player:
    def __init__(self, player_socket, addr):
        self.__name = None
        self.health = 100
        self.magic = 100
        self.magic_limit = 100
        self.socket = player_socket
        self.current_move = None
        self.address = addr
        self.match_id = None
        self.index = None
        self.character = None

    @property
    def name(self):
        return self.__name

    @name.setter
    def name(self, character_name):
        self.__name = character_name
        # self.character = find_character(character_name)

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
