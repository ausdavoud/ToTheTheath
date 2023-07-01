from pydantic import BaseModel
from player import Player
from random import choices, choice
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
               "result_str": player1.fight_result_str,
               "enemy_health": player2.health,
               "enemy_magic": player2.magic,
               "header": 'change_stat'}
        player1.send(json.dumps(msg))

        msg = {"health": player2.health,
               "magic": player2.magic,
               "result_str": player2.fight_result_str,
               "enemy_health": player1.health,
               "enemy_magic": player1.magic,
               "header": 'change_stat'}
        player2.send(json.dumps(msg))

    def strike(self, doer: int) -> None:
        players: list[Player] = [self.player1, self.player2]

        new_player1 = players[doer]
        new_player2 = players[int(not bool(doer))]

        strike_power = new_player1.character.strike_power
        success_rate = new_player1.character.strike_rate / 100
        success = choices([1, 0], weights=[success_rate, 1 - success_rate], k=1)[0]

        new_player2.decrease_health(success * strike_power)
        if success:
            new_player1.fight_result.append("You striked the enemy")
            new_player2.fight_result.append("Enemy striked You")
        else:
            new_player1.fight_result.append("You could not strike the enemy")
            new_player2.fight_result.append("Enemy could not strike you")

    def magic(self, doer: int) -> None:
        players: list[Player] = [self.player1, self.player2]

        new_player1 = players[doer]
        new_player2 = players[int(not bool(doer))]

        magic_power = new_player1.character.magic_power
        success_rate = new_player1.character.magic_rate / 100

        success = choices([1, 0], weights=[success_rate, 1 - success_rate], k=1)[0]

        if new_player1.decrease_magic():
            new_player2.decrease_health(success * magic_power)
        else:
            new_player1.fight_result.append('Your magic is not enough')

        if success:
            new_player1.fight_result.append("You spelled the enemy")
            new_player2.fight_result.append("Enemy spelled you")
        else:
            new_player1.fight_result.append("You could not spell the enemy")
            new_player2.fight_result.append("Enemy could not spell you")

    @staticmethod
    def is_defence_successful(player: Player) -> bool:
        success_rate = player.character.defence_rate / 100
        success = choices([1, 0], weights=[success_rate, 1 - success_rate], k=1)[0]
        return bool(success)
    
    def fight(self):
        moves = {
            'strike': self.strike,
            'magic': self.magic
        }

        if self.player1_move == 'defence' and self.player2_move == 'defence':
            self.player1.fight_result.append("Both defended")
            self.player2.fight_result.append("Both defended")

        elif self.player1_move == 'defence':
            if Fight.is_defence_successful(self.player1):
                self.player1.fight_result.append("You defended the enemy's attack")
                self.player2.fight_result.append("Enemy defended your attack")
                if self.player2_move == 'magic':
                    self.player1.increase_magic()
                    self.player2.decrease_magic()
            else:
                moves[self.player2_move](1)

        elif self.player2_move == 'defence':
            if Fight.is_defence_successful(self.player2):
                self.player2.fight_result.append("You defended enemy's attack")
                self.player1.fight_result.append("Enemy defended your attack")
                if self.player1_move == 'magic':
                    self.player2.increase_magic()
                    self.player1.decrease_magic()
            else:
                moves[self.player1_move](0)

        else:
            moves[self.player1_move](0)
            moves[self.player2_move](1)
        
        if self.player1.is_dead() and self.player2.is_dead():
            return choice([self.player1, self.player2])
        elif self.player1.is_dead():
            return self.player2
        elif self.player2.is_dead():
            return self.player1
            

        self.send_stat(self.player1, self.player2)
        self.player1.fight_result.clear()
        self.player2.fight_result.clear()
