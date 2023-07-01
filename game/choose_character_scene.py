from ui import *

current_index = 0


def draw_character_option(character, x, y, selected=False):
    rect = pygame.Rect(x, y, 300, 48)
    pygame.draw.rect(pygame.display.get_surface(), colors.BLACK, rect, 0 if selected else 2)
    draw_text(character['name'], x + 16, y + 16, colors.WHITE if selected else colors.BLACK)


def show_stats(character: dict):
    draw_text("Stats -------------", 520, 100, colors.BLACK, header_font)
    stats = character
    for i, stat in enumerate(stats.keys()):
        if stat != 'light_theme' and stat != 'background_color':
            draw_text(f"{' '.join(stat.split('_')).capitalize()} : {stats[stat]}",
                      520, 100 + 48 + (25 + 8) * i, colors.BLACK)


def change_current_character_index(index: int, characters, change_background):
    global current_index
    current_index = index
    background = tuple(characters[current_index]['background_color'])
    light_theme = characters[current_index]['light_theme']
    change_background(background, light_theme)


def show_choosing_character_screen(events, enter_function, characters: list[dict], change_background):
    for event in events:
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP and current_index > 0:
                change_current_character_index(current_index - 1, characters, change_background)
            elif event.key == pygame.K_DOWN and current_index < len(characters) - 1:
                change_current_character_index(current_index + 1, characters, change_background)
            elif event.key == pygame.K_RETURN:
                enter_function(characters[current_index])

    draw_text("Choose your character:", 100, 100, colors.BLACK, header_font)
    for i in range(len(characters)):
        c = characters[i]
        draw_character_option(c, 100, 166 + i * (48 + 24), i == current_index)
    show_stats(characters[current_index])
