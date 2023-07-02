from pydantic import BaseModel
from player import Player
from random import choices, choice
from _log import Log
import json


class Fight(BaseModel):
    player1: Player
    player2: Player
    logger: Log

    def send_stat(self) -> None:
        player1 = self.player1
        player2 = self.player2
        msg = {"health": player1.health,
               "magic": player1.magic,
               "fight_result": player1.fight_result,
               "enemy_health": player2.health,
               "enemy_magic": player2.magic,
               "header": 'change_stat'}
        player1.send(json.dumps(msg))

        msg = {"health": player2.health,
               "magic": player2.magic,
               "fight_result": player2.fight_result,
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
            
        return bool(success)

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
        
        return bool(success)

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

        if self.player1.current_move == 'defence' and self.player2.current_move == 'defence':
            self.player1.fight_result.append("Both defended")
            self.player2.fight_result.append("Both defended")
            self.logger.round_logging(player1_move_result=True, player2_move_result=True)
        elif self.player1.current_move == 'defence':
            if defence_success := Fight.is_defence_successful(self.player1):
                move_success = False
                self.player1.fight_result.append("You defended the enemy's attack")
                self.player2.fight_result.append("Enemy defended your attack")
                if self.player2.current_move  == 'magic':
                    self.player1.increase_magic()
                    self.player2.decrease_magic()
            else:
                move_success = moves[self.player2.current_move ](1)
            self.logger.round_logging(player1_move_result=defence_success, player2_move_result=move_success)

        elif self.player2.current_move  == 'defence':
            if defence_success := Fight.is_defence_successful(self.player2):
                move_success = False
                self.player2.fight_result.append("You defended enemy's attack")
                self.player1.fight_result.append("Enemy defended your attack")
                if self.player1.current_move == 'magic':
                    self.player2.increase_magic()
                    self.player1.decrease_magic()
            else:
                move_success = moves[self.player1.current_move](0)
            self.logger.round_logging(player1_move_result=move_success, player2_move_result=defence_success)

        else:
            player1_move_success = moves[self.player1.current_move](0)
            player2_move_success = moves[self.player2.current_move ](1)
            self.logger.round_logging(player1_move_result=player1_move_success, player2_move_result=player2_move_success,)

        winner: Player = None
        if self.player1.is_dead() and self.player2.is_dead():
            winner = choice([self.player1, self.player2])
        elif self.player1.is_dead():
            winner = self.player2
        elif self.player2.is_dead():
            winner = self.player1
        if winner is not None:
            self.logger.finish_logging(winner_IP=winner.address)
            return winner

        self.send_stat()
        self.player1.fight_result.clear()
        self.player2.fight_result.clear()
