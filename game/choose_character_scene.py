# import sys
# sys.path.insert(0, '.')
# from server.character import characters
from ui import *

current_index = 0

def draw_character_option(character, x, y, selected=False):
    rect = pygame.Rect(x, y, 300, 48)
    pygame.draw.rect(pygame.display.get_surface(), BLACK, rect, 0 if selected else 2)
    draw_text(character['name'], x + 16, y + 16, WHITE if selected else BLACK)

def show_stats(character: dict):
    draw_text("Stats -------------", 520, 100, BLACK, header_font)
    # stats = character.get_stats()
    stats = character
    for i, stat in enumerate(stats.keys()):
        draw_text(f"{' '.join(stat.split('_')).capitalize()} : {stats[stat]}", 520, 100 + 48 + (25 + 8) * i)


def show_choosing_character_screen(events, enter_function, characters: list[dict]):
    global current_index

    for event in events:
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP and current_index > 0:
                current_index -= 1
            elif event.key == pygame.K_DOWN and current_index < len(characters) - 1:
                current_index += 1
            elif event.key == pygame.K_RETURN:
                enter_function(characters[current_index])

    draw_text("Choose your character:", 100, 100, BLACK, header_font)
    for i in range(len(characters)):
        c = characters[i]
        draw_character_option(c, 100, 166 + i * (48 + 24), i == current_index)
    show_stats(characters[current_index])
