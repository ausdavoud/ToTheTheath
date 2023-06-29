from pydantic import BaseModel
from player import Player
from random import choice
from socket import socket

class Fight(BaseModel):
    player1: Player
    player2: Player
    player1_move: str
    player2_move: str 
    
    def strike(self, doer: int) -> list[Player]:
        players: list[Player] = [self.player1, self.player2]

        new_player1 = players[doer]
        new_player2 = players[not doer]
        
        strike_power = new_player1.character.strike_power
        success_rate = new_player1.character.strike_rate/100
        success = choice([1, 0], p=[success_rate, 1 - success_rate])
        messages = {0: 'could not hit the enemy.', 1: f'hit the enemy by {strike_power}!'}
        
        new_player2.decrease_health(success * strike_power)
        new_player1.send(f'You {messages[success]}')
        
        return new_player1, new_player2
        
    def magic(self, doer: int) -> list[Player]:
        players: list[Player] = [self.player1, self.player2]
        new_player1 = players[doer]
        new_player2 = players[not doer]
        
        magic_power  = new_player1.character.magic_power
        success_rate = new_player1.character.magic_rate / 100
        
        success = choice([1, 0], p=[success_rate, 1 - success_rate])
        messages = {0: 'could not hit the enemy.', 1: f'hit the enemy by {magic_power}!'}
        
        new_player2.decrease_health(success * magic_power)
        new_player1.send(f'You {messages[success]}')
        
        return new_player1, new_player2
        
    @staticmethod
    def is_defence_successful(player: Player) -> bool:
        success_rate = player.character.defence_rate / 100
        success = choice([1, 0], p=[success_rate, 1 - success_rate])
        return bool(success)
    
    def fight(self) -> list[Player]:
        moves = {
                'strike': self.strike,
                'magic': self.magic
                }

        if self.player1_move == 'defence' and self.player2_move == 'defence':
            msg = 'Both players defended!'
            self.player1.send(msg)
            self.player2.send(msg)
            
        elif self.player1_move == 'defence':
            if Fight.is_defence_successful(self.player1):
                print('Player 1 defended!')
                if self.player2_move == 'magic':
                    magic_reset_rate = self.player1.character.magic_reset_rate
                    self.player1.increase_magic(magic_reset_rate)
                    print(f'{magic_reset_rate} added to your magic!')
            else:
                self.player2, self.player1 = moves[self.player2_move](1)      
        elif self.player2_move == 'defence':
            if Fight.is_defence_successful(self.player2):
                print('Player 2 defended!')
                if self.player1_move == 'magic':
                    magic_reset_rate = self.player2.character.magic_reset_rate
                    self.player2.increase_magic(magic_reset_rate)
                    print(f'{magic_reset_rate} added to your magic!')
            else:
                self.player1, self.player2 = moves[self.player1_move](0)
                
        return self.player1, self.player2