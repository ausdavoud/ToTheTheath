from ui import *

moves = ['strike', 'defence', 'magic']

status = 'choosing_move'
move_index = 0


def change_playing_status(value):
    global status
    status = value


def draw_move_option(move, x, y, selected=False):
    rect = pygame.Rect(x, y, 240, 40)
    pygame.draw.rect(window(), BLACK, rect, 0 if selected else 2)
    move = str(move)
    move = move[0].upper() + move[1:]
    draw_text(move, x + 8, y + 12, WHITE if selected else BLACK)


def draw_bars(health, magic, x, y, character_name):
    bar_width, bar_height = 240, 14
    draw_text(character_name, x, y, font=header_font)
    # Health bar
    draw_text('Health:', x, y + 40)
    draw_fill_rect(bar_width, bar_height, x, y + 65)
    health_bar_width = (health * bar_width) // 100
    draw_fill_rect(health_bar_width, bar_height, x, y + 65, BLACK)
    # Magic bar
    draw_text('Magic:', x, y + 100)
    draw_fill_rect(bar_width, bar_height, x, y + 125)
    health_bar_width = (magic * bar_width) // 100
    draw_fill_rect(health_bar_width, bar_height, x, y + 125, BLACK)


def show_playing_screen(events, socket, you, enemy):
    global move_index

    for event in events:
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP and move_index > 0:
                move_index -= 1
            elif event.key == pygame.K_DOWN and move_index < len(moves) - 1:
                move_index += 1
            elif event.key == pygame.K_RETURN:
                socket.sendall(f'move::{moves[move_index]}'.encode('utf-8'))
                change_playing_status('waiting')

    draw_bars(you.health, you.magic, 100, 40, you.character['name'])
    draw_bars(enemy.health, enemy.magic, 560, 40, enemy.character['name'])
    if status == 'choosing_move':
        draw_text("Choose Your Move :", 330, 275, BLACK, header_font)
        for i, move in enumerate(moves):
            draw_move_option(move, 330, 325 + (i * 52), i == move_index)
    elif status == 'waiting':
        draw_text("Waiting for enemy's move ...", 327, 340)
