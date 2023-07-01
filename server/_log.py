from datetime import datetime
from pydantic import BaseModel
from typing import Any
from player import Player
FILE_NAME = 'ttt_log.txt'

class Log(BaseModel):
    player1_IP: tuple
    player2_IP: tuple
    player1_character: str
    player2_character: str
    round: int = 0
    players_IPs: dict = {}
    
    def start_logging(self) -> None:
        self.players_IPs = {self.player1_IP: f'[0]{self.player1_character}',
                              self.player2_IP: f'[1]{self.player2_character}'}
        with open(FILE_NAME, 'a', encoding='utf-8') as file:
            msg = f'''-------------------------------
MATCH START: {datetime.now()}
{self.player1_IP}: {self.players_IPs[self.player1_IP]}
{self.player2_IP}: {self.players_IPs[self.player2_IP]}\n\n'''
            file.write(msg)
            
        self.round+=1
            
    def round_logging(self, player1_IP: tuple, player2_IP: tuple, 
                      player1_move: str, player2_move: str,
                      player1_move_result: bool, player2_move_result:  bool,
                      player1_health, player2_health,
                      player1_magic, player2_magic) -> None:
        
        player1_move_result = str(player1_move_result).replace('True', 'Success').replace('False', 'Fail')
        player2_move_result = str(player2_move_result).replace('True', 'Success').replace('False', 'Fail')
        with open(FILE_NAME, 'a', encoding='utf-8') as file:
            msg = f'''>> ROUND {self.round}:
{self.players_IPs[player1_IP]}: {player1_move} -> {player1_move_result}
{self.players_IPs[player2_IP]}: {player2_move} -> {player2_move_result}
>>>> DESCRIPTION:
{self.players_IPs[player1_IP]}: HEALTH = {player1_health}, MAGIC = {player1_magic}
{self.players_IPs[player2_IP]}: HEALTH = {player2_health}, MAGIC = {player2_magic}\n\n'''
            file.write(msg)
        self.round += 1
    
    def finish_logging(self, winner_IP: tuple) -> None:
        loser_IP = self.player1_IP if winner_IP == self.player2_IP else self.player2_IP
        with open(FILE_NAME, 'a', encoding='utf-8') as file:
            msg = f'''<< RESULT >>:
WINNER: {self.players_IPs[winner_IP]}
LOSER: {self.players_IPs[loser_IP]}
-------------------------------\n\n
'''
            file.write(msg)