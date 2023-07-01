import socket
from _thread import start_new_thread
from player import Player
from fight import Fight
from character import characters_dict, find_character
import json

ADDR, PORT = "", 4000
soc = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

soc.bind((ADDR, PORT))
soc.listen()
print(">> Server is running on port", PORT)

players = []
waiting_player = None
running_matches = []


def process_move(player: Player, move: str):
    enemy_index = int(not bool(player.index))
    enemy: Player = running_matches[player.match_id][enemy_index]
    if not player.current_move and not enemy.current_move:
        player.current_move = move
    elif not player.current_move and enemy.current_move:
        player.current_move = move

        _fight = Fight(player1=player, player2=enemy,
                       player1_move=player.current_move,
                       player2_move=enemy.current_move)
        if (winner := _fight.fight()) != None:
            msg = {'result': 'win',
                   'header': 'end'}
            winner.send(json.dumps(msg))
            
            loser_index = int(not bool(winner.index))
            loser: Player = running_matches[winner.match_id][loser_index]
            msg = {'result': 'lose',
                   'header': 'end'}
            loser.send(json.dumps(msg))

        player.current_move = None
        enemy.current_move = None


def start_match(player1, player2):
    player1.match_id = len(running_matches)
    player1.index = 0
    player2.match_id = len(running_matches)
    player2.index = 1
    running_matches.append((player1, player2))
    player1.send(json.dumps({"name": player2.name,
                             "header": "namechosed"}))
    player2.send(json.dumps({"name": player1.name,
                             "header": "namechosed"}))


def handle_player_msg(msg, player: Player):
    global waiting_player
    msg = json.loads(msg)
    if msg['header'] == 'start_game':
        player.name = msg['character_name']
        player.character = find_character(msg['character_name'])

        if waiting_player is None:
            waiting_player = player
        else:
            start_match(waiting_player, player)
            waiting_player = None
    elif msg['header'] == 'move':
        process_move(player, msg['move'])
    else:
        print(msg)


def handle_player_connection(player):
    while True:
        try:
            msg = player.socket.recv(1024)
            if not msg:
                break
            else:
                msg = msg.decode('utf-8')
                handle_player_msg(msg, player)
        except socket.error as e:
            print(e)
            break
    print(">> DISCONNECTED:", player.address)


def start_server():
    while True:
        player, addr = soc.accept()
        player = Player(socket=player, address=addr)
        print(">> NEW CONNECTION:", addr)
        player.send("Hello from server")
        player.send(json.dumps(characters_dict))
        start_new_thread(handle_player_connection, (player,))


start_server()
