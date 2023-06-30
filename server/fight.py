from pydantic import BaseModel
from player import Player
from random import choices
import json


class Fight(BaseModel):
    player1: Player
    player2: Player
    player1_move: str
    player2_move: str

    @staticmethod
    def send_stat(player1, player2) -> None:
        msg = {"health": player1.health,
               "magic": player1.magic,
               "enemy_health": player2.health,
               "enemy_magic": player2.magic,
               "header": 'change_stat'}
        player1.send(json.dumps(msg))

        msg = {"health": player2.health,
               "magic": player2.magic,
               "enemy_health": player1.health,
               "enemy_magic": player1.magic,
               "header": 'change_stat'}
        player2.send(json.dumps(msg))

    def strike(self, doer: int) -> tuple:
        players: list[Player] = [self.player1, self.player2]

        new_player1 = players[doer]
        new_player2 = players[not doer]

        strike_power = new_player1.character.strike_power
        success_rate = new_player1.character.strike_rate / 100
        success = choices([1, 0], weights=[success_rate, 1 - success_rate], k=1)[0]

        new_player2.decrease_health(success * strike_power)

        return new_player1, new_player2

    def magic(self, doer: int) -> tuple:
        players: list[Player] = [self.player1, self.player2]
        doer = bool(doer)
        new_player1 = players[doer]
        new_player2 = players[not doer]

        magic_power = new_player1.character.magic_power
        success_rate = new_player1.character.magic_rate / 100

        success = choices([1, 0], weights=[success_rate, 1 - success_rate], k=1)[0]

        new_player1.decrease_magic(magic_power)
        new_player2.decrease_health(success * magic_power)

        return new_player1, new_player2

    @staticmethod
    def is_defence_successful(player: Player) -> bool:
        success_rate = player.character.defence_rate / 100
        success = choices([1, 0], weights=[success_rate, 1 - success_rate], k=1)[0]
        return bool(success)

    def fight(self) -> tuple:
        moves = {
            'strike': self.strike,
            'magic': self.magic
        }

        if self.player1_move == 'defence' and self.player2_move == 'defence':
            print('Both defended!')
            ...

        elif self.player1_move == 'defence':
            if Fight.is_defence_successful(self.player1):
                print('Player 1 defended!')
                if self.player2_move == 'magic':
                    magic_reset_rate = self.player1.character.magic_reset_rate
                    self.player1.increase_magic()
                    print(f'{magic_reset_rate} added to your magic!')
            else:
                self.player2, self.player1 = moves[self.player2_move](1)

        elif self.player2_move == 'defence':
            if Fight.is_defence_successful(self.player2):
                print('Player 2 defended!')
                if self.player1_move == 'magic':
                    magic_reset_rate = self.player2.character.magic_reset_rate
                    self.player2.increase_magic()
                    print(f'{magic_reset_rate} added to your magic!')
            else:
                self.player1, self.player2 = moves[self.player1_move](0)

        else:
            self.player1, self.player2 = moves[self.player1_move](0)
            self.player2, self.player1 = moves[self.player2_move](1)

        self.send_stat(self.player1, self.player2)
        return self.player1, self.player2
