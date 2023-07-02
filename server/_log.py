from datetime import datetime
from pydantic import BaseModel
from typing import Any
from player import Player
FILE_NAME = 'ttt_log.txt'

class Log(BaseModel):
    player1: Player
    player2: Player
    round: int = 0
    players_IPs: dict = {}
    
    def start_logging(self) -> None:
        self.players_IPs = {self.player1.address: f'[0]{self.player1.name}',
                              self.player2.address: f'[1]{self.player2.name}'}
        with open(FILE_NAME, 'a', encoding='utf-8') as file:
            msg = f'''-------------------------------
MATCH START: {datetime.now()}
{self.player1.address}: {self.players_IPs[self.player1.address]}
{self.player2.address}: {self.players_IPs[self.player2.address]}\n\n'''
            file.write(msg)

        self.round+=1

    def round_logging(self, player1_move_result: bool, player2_move_result: bool) -> None:
        player1_move_result = 'Success' if player1_move_result==True else 'Fail'
        player2_move_result = 'Success' if player2_move_result==True else 'Fail'
        with open(FILE_NAME, 'a', encoding='utf-8') as file:
            msg = f'''>> ROUND {self.round}:
{self.players_IPs[self.player1.address]}: {self.player1.current_move} -> {player1_move_result}
{self.players_IPs[self.player2.address]}: {self.player2.current_move} -> {player2_move_result}
>>>> DESCRIPTION:
{self.players_IPs[self.player1.address]}: HEALTH = {self.player1.health}, MAGIC = {self.player1.magic}
{self.players_IPs[self.player2.address]}: HEALTH = {self.player2.health}, MAGIC = {self.player2.magic}\n\n'''
            file.write(msg)
        self.round += 1
    
    def finish_logging(self, winner_IP: tuple) -> None:
        loser_IP = self.player1.address if winner_IP == self.player2.address else self.player2.address
        with open(FILE_NAME, 'a', encoding='utf-8') as file:
            msg = f'''<< RESULT >>:
WINNER: {self.players_IPs[winner_IP]}
LOSER: {self.players_IPs[loser_IP]}
-------------------------------\n\n
'''
            file.write(msg)