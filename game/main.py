import socket
import time
from _thread import start_new_thread
from choose_character_scene import show_choosing_character_screen
from playing_scene import show_playing_screen
from player import Player
from character import find_character
from ui import *

sc = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

WIDTH, HEIGHT = 900, 600
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('To The Theath')

server_address = ('127.0.0.1', 4000)
FPS = 60
SCENE = "connecting"

you = None
enemy = None


def change_scene(scene):
    global SCENE
    SCENE = scene


def connect_to_server():
    global sc
    while True:
        try:
            sc.connect(server_address)
            print(sc.recv(1024).decode('utf-8'))
            change_scene("choosing_character")
            break
        except ConnectionRefusedError:
            print('[conn refused] -- retrying in 1 second')
            sc = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            time.sleep(1)
        except Exception as e:
            change_scene('connection_error')
            print(e)
            break


def start_game(character):
    global you
    change_scene('waiting')
    you = Player(character=character)

    def _start():
        global enemy
        try:
            sc.sendall(f'msg::start_game::{character.name}'.encode('utf-8'))
            enemy_character_name = sc.recv(1024).decode('utf-8')
            enemy = find_character(enemy_character_name)
            if enemy:
                enemy = Player(character=enemy)
                change_scene('playing')
            else:
                msg = enemy_character_name
                print(msg)
        except socket.error as e:
            print(e)

    start_new_thread(_start, ())


def handle_scenes(events):
    match SCENE:
        case 'choosing_character':
            show_choosing_character_screen(events, start_game)
        case 'waiting':
            draw_center_text('Waiting for other player ...')
        case 'connecting':
            draw_center_text('Connecting ...')
        case 'playing':
            show_playing_screen(events, sc, you, enemy)
        case 'connection_error':
            draw_center_text("Connection Error !!")


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
        WIN.fill(WHITE)
        handle_scenes(events)
        pygame.display.update()
    pygame.quit()


if __name__ == "__main__":
    main()
