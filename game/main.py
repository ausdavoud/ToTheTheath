import socket
import time
from _thread import start_new_thread
from choose_character_scene import show_choosing_character_screen, change_current_character_index
from playing_scene import show_playing_screen, change_playing_status, activate_move, disable_move, disabled_moves
from ending_scene import show_ending_scene
from player import Player
from ui import *
import json

sc = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

WIDTH, HEIGHT = 900, 600
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
BACKGROUND = colors.WHITE
pygame.display.set_caption('To The Theath')

server_address = ('127.0.0.1', 4000)
FPS = 60
SCENE = "connecting"
MATCH_RESULT = ''

you: Player = None
enemy: Player = None
characters: list[dict] = []


def change_scene(scene):
    global SCENE
    time.sleep(0.2)
    SCENE = scene


def change_background(background, light_theme=True):
    global BACKGROUND
    BACKGROUND = background
    change_light_theme(light_theme)


def connect_to_server():
    global sc
    global characters
    while True:
        try:
            sc.connect(server_address)
            characters = extract_characters(sc.recv(1024).decode('utf-8'))
            change_scene("choosing_character")
            change_current_character_index(0, characters, change_background)
            start_new_thread(game_stat_receiver, ())
            break
        except ConnectionRefusedError:
            print('[conn refused] -- retrying in 1 second')
            sc = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            time.sleep(1)
        except Exception as e:
            change_scene('connection_error')
            print(e)
            break


def game_stat_receiver():
    while True:
        try:
            msg = sc.recv(1024)
            if not msg:
                break
            else:
                msg = msg.decode('utf-8')
                handle_server_msg(msg)
        except socket.error as e:
            print(e)
            break
    print(">> DISCONNECTED")


def handle_server_msg(msg: str) -> None:
    global enemy
    print(msg)
    msg = json.loads(msg)
    if msg['header'] == 'namechosed':
        enemy = find_character(msg['enemyname'])
        if enemy:
            enemy = Player(character=enemy)
            change_scene('playing')
    elif msg['header'] == 'change_stat':
        you.health = msg['health']
        you.magic = msg['magic']

        magic_power = you.character['magic_power']
        if you.magic < magic_power and 'magic' not in disabled_moves:
            disable_move('magic')
        elif you.magic > magic_power and 'magic' in disabled_moves:
            activate_move('magic')

        enemy.health = msg['enemy_health']
        enemy.magic = msg['enemy_magic']
        you.fight_result = msg['fight_result']
        change_playing_status("showing_result")
        time.sleep(1.5)
        change_playing_status('choosing_move')
    elif msg['header'] == 'end':
        global MATCH_RESULT
        MATCH_RESULT = msg['result']
        change_scene('ending')


def find_character(name):
    for character in characters:
        if character['name'] == name: return character


def extract_characters(text: str) -> list[dict]:
    characters = json.loads(text)
    return characters


def start_game(character):
    global you
    change_scene('waiting')
    you = Player(character=character)
    try:
        sc.sendall(json.dumps({"header": "start_game", "character_name": character['name']}).encode('utf-8'))
    except socket.error as e:
        print(e)


def start_new_game():
    global you, enemy, MATCH_RESULT, sc
    you = None
    enemy = None
    characters.clear()
    change_scene('connecting')
    MATCH_RESULT = ''
    change_playing_status('choosing_move')
    sc = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    main()


def handle_scenes(events):
    match SCENE:
        case 'choosing_character':
            show_choosing_character_screen(events, start_game, characters, change_background)
        case 'waiting':
            draw_center_text('Waiting for other player ...', colors.BLACK)
        case 'connecting':
            draw_center_text('Connecting ...', colors.BLACK)
        case 'playing':
            show_playing_screen(events, sc, you, enemy)
        case 'connection_error':
            draw_center_text("Connection Error !!", colors.BLACK)
        case 'ending':
            show_ending_scene(MATCH_RESULT, events, start_new_game)


def main():
    clock = pygame.time.Clock()
    running = True
    start_new_thread(connect_to_server, ())
    while running:
        clock.tick(FPS)
        events = pygame.event.get()
        for event in events:
            if event.type == pygame.QUIT:
                running = False
        WIN.fill(BACKGROUND)
        handle_scenes(events)
        pygame.display.update()
    pygame.quit()


if __name__ == "__main__":
    main()
