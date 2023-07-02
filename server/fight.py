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

    @staticmethod
    def is_move_successful(success_rate: int) -> bool:
        success_rate /= 100
        success = choices([1, 0], weights=[success_rate, 1 - success_rate], k=1)[0]
        return bool(success)
    
    def strike(self, doer: Player) -> bool:
        enemy = self.player1 if doer.index == self.player2.index else self.player2
        strike_power = doer.character.strike_power
        success = Fight.is_move_successful(doer.character.strike_rate)

        enemy.decrease_health(int(success) * strike_power)
        if success:
            doer.fight_result.append("You striked the enemy")
            enemy.fight_result.append("Enemy striked You")
        else:
            doer.fight_result.append("You could not strike the enemy")
            enemy.fight_result.append("Enemy could not strike you")
            
        return success

    def magic(self, doer: Player) -> bool:
        enemy = self.player1 if doer.index == self.player2.index else self.player2
        magic_power = doer.character.magic_power
        success = Fight.is_move_successful(doer.character.magic_rate)

        if doer.decrease_magic():
            enemy.decrease_health(int(success) * magic_power)
        else:
            doer.fight_result.append('Your magic is not enough')

        if success:
            doer.fight_result.append("You spelled the enemy")
            enemy.fight_result.append("Enemy spelled you")
        else:
            doer.fight_result.append("You could not spell the enemy")
            enemy.fight_result.append("Enemy could not spell you")
        
        return success
    
    def fight(self):
        moves = {
            'strike': self.strike,
            'magic': self.magic
        }
        
        player1_move_result: bool
        player2_move_result: bool
        if self.player1.current_move == 'defence' and self.player2.current_move == 'defence':
            self.player1.fight_result.append("Both defended")
            self.player2.fight_result.append("Both defended")
            player1_move_result, player2_move_result = True, True

        elif self.player1.current_move == 'defence':
            if player1_move_result := Fight.is_move_successful(self.player1.character.defence_rate):
                player2_move_result = False
                self.player1.fight_result.append("You defended the enemy's attack")
                self.player2.fight_result.append("Enemy defended your attack")
                if self.player2.current_move  == 'magic':
                    self.player1.increase_magic()
                    self.player2.decrease_magic()
            else:
                player2_move_result = moves[self.player2.current_move](self.player2)

        elif self.player2.current_move  == 'defence':
            if player2_move_result := Fight.is_move_successful(self.player2.character.defence_rate):
                player1_move_result = False
                self.player2.fight_result.append("You defended enemy's attack")
                self.player1.fight_result.append("Enemy defended your attack")
                if self.player1.current_move == 'magic':
                    self.player2.increase_magic()
                    self.player1.decrease_magic()
            else:
                player1_move_result = moves[self.player1.current_move](self.player1)

        else:
            player1_move_result = moves[self.player1.current_move](self.player1)
            player2_move_result = moves[self.player2.current_move ](self.player2)
        self.logger.round_logging(player1_move_result=player1_move_result, player2_move_result=player2_move_result)

        winner: Player = None
        if self.player1.is_dead() and self.player2.is_dead():
            winner = choice([self.player1, self.player2])
        elif self.player1.is_dead() or self.player2.is_dead():
            winner = self.player1 if self.player1.is_dead else self.player2

        if winner is not None:
            self.logger.finish_logging(winner)
            return winner

        self.send_stat()
        self.player1.fight_result.clear()
        self.player2.fight_result.clear()
