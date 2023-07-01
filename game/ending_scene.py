from ui import *


def show_ending_scene(result: str, events, start_new_game):
    for event in events:
        if event.type == pygame.KEYUP and event.key == pygame.K_RETURN:
            start_new_game()

    if result == 'win':
        draw_center_text('Hooray, you won the game! Press enter to restart the game...')
    elif result == 'lose':
        draw_center_text('Damn it, you lost! Press enter to restart the game...')
