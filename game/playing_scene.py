import json

from ui import *

moves = ['strike', 'defence', 'magic']
disabled_moves = []

status = 'choosing_move'
move_index = 0


def change_playing_status(value):
    global status
    status = value


def disable_move(move: str):
    global move_index
    moves.remove(move)
    disabled_moves.append(move)
    move_index = 0


def activate_move(move: str):
    global move_index
    disabled_moves.remove(move)
    moves.append(move)
    move_index = 0


def draw_move_option(move, x, y, selected=False, disabled=False):
    color = colors.GRAY if disabled else colors.BLACK
    rect = pygame.Rect(x, y, 240, 40)
    pygame.draw.rect(window(), color, rect, 0 if selected else 2)
    move = str(move)
    move = move[0].upper() + move[1:]
    draw_text(move, x + 8, y + 12, colors.WHITE if selected else color)


def draw_bars(health, magic, x, y, character_name):
    bar_width, bar_height = 240, 14
    draw_text(character_name, x, y, colors.BLACK, header_font)
    # Health bar
    draw_text('Health:', x, y + 40, colors.BLACK)
    draw_fill_rect(bar_width, bar_height, x, y + 65, colors.GRAY)
    health_bar_width = (health * bar_width) // 100
    draw_fill_rect(health_bar_width, bar_height, x, y + 65, colors.BLACK)
    # Magic bar
    draw_text('Magic:', x, y + 100, colors.BLACK)
    draw_fill_rect(bar_width, bar_height, x, y + 125, colors.GRAY)
    health_bar_width = (magic * bar_width) // 100
    draw_fill_rect(health_bar_width, bar_height, x, y + 125, colors.BLACK)


def show_playing_screen(events, socket, you, enemy):
    global move_index

    for event in events:
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP and move_index > 0:
                move_index -= 1
            elif event.key == pygame.K_DOWN and move_index < len(moves) - 1:
                move_index += 1
            elif event.key == pygame.K_RETURN:
                socket.sendall(json.dumps({"header": "move", "move": moves[move_index]}).encode('utf-8'))
                change_playing_status('waiting')

    if status == "showing_result":
        draw_center_text_list(you.fight_result, colors.BLACK)
    else:
        draw_bars(you.health, you.magic, 100, 40, you.character['name'])
        draw_bars(enemy.health, enemy.magic, 560, 40, enemy.character['name'])
        if status == 'choosing_move':
            draw_text("Choose Your Move :", 330, 275, colors.BLACK, header_font)
            for i, move in enumerate(moves):
                draw_move_option(move, 330, 325 + (i * 52), i == move_index)
            for i, move in enumerate(disabled_moves):
                draw_move_option(move, 330, 325 + ((i + len(moves)) * 52), False, True)
        elif status == 'waiting':
            draw_text("Waiting for enemy's move ...", 327, 340, colors.BLACK)
