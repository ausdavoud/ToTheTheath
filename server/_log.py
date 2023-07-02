from player import Player
from datetime import datetime
from pydantic import BaseModel

FILE_NAME = './server/ttt_log.txt'

class Log(BaseModel):
    player1: Player
    player2: Player
    round: int = 0
        
    def start_logging(self) -> None:
        with open(FILE_NAME, 'a', encoding='utf-8') as file:
            msg = f'''^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
MATCH START: {datetime.now()}
{self.player1.address}: [{self.player1.index}]{self.player1.name}
{self.player2.address}: [{self.player2.index}]{self.player2.name}
\n'''
            file.write(msg)

        self.round+=1

    def round_logging(self, player1_move_result: bool, player2_move_result: bool) -> None:
        player1_move_result = 'Success' if player1_move_result==True else 'Fail'
        player2_move_result = 'Success' if player2_move_result==True else 'Fail'
        with open(FILE_NAME, 'a', encoding='utf-8') as file:
            
            msg = f'''>> ROUND {self.round}:
[{self.player1.index}]{self.player1.name}: {self.player1.current_move} -> {player1_move_result} | HEALTH = {self.player1.health} | MAGIC = {self.player1.magic}
[{self.player2.index}]{self.player2.name}: {self.player2.current_move} -> {player2_move_result} | HEALTH = {self.player2.health} | MAGIC = {self.player2.magic}
\n'''
    
            file.write(msg)
        self.round += 1
    
    def finish_logging(self, winner: Player) -> None:
        loser = self.player1 if winner.index == self.player2.index else self.player2
        with open(FILE_NAME, 'a', encoding='utf-8') as file:
            
            msg = f'''<v><v><v> RESULT <v><v><v>:
WINNER: [{winner.index}]{winner.name}
LOSER: [{loser.index}]{loser.name}
vvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvv
\n'''

            file.write(msg)