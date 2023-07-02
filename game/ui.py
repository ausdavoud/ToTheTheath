import pygame
import pygame.freetype
import os
from pydantic import BaseModel

pygame.init()
font_path = os.path.join(os.path.dirname(__file__), 'lexend.ttf')
text_font = pygame.freetype.Font(font_path, 18)
header_font = pygame.freetype.Font(font_path, 22)


class Colors(BaseModel):
    BLACK = (0, 0, 0)
    WHITE = (255, 255, 255)
    GRAY = (230, 230, 230)


LIGHT_THEME = True
colors = Colors()


def window(): return pygame.display.get_surface()


def change_light_theme(light_theme: bool):
    global LIGHT_THEME
    LIGHT_THEME = light_theme
    if LIGHT_THEME:
        colors.WHITE = (255, 255, 255)
        colors.BLACK = (0, 0, 0)
        colors.GRAY = (230, 230, 230)
    else:
        colors.WHITE = (0, 0, 0)
        colors.BLACK = (255, 255, 255)
        colors.GRAY = (150, 150, 150)


def draw_text(text, x, y, text_color, font=text_font):
    font.render_to(window(), (x, y), text, text_color)


def draw_center_text(text, color, font=header_font):
    text_rect = font.get_rect(text)
    x = (window().get_width() - text_rect.width) / 2
    y = (window().get_height() - text_rect.height) / 2
    destination = (x, y)
    font.render_to(window(), destination, text, color)


def draw_center_text_list(text_list: list, text_color, font=header_font):
    height = 0
    for i, text in enumerate(text_list):
        text_rect = font.get_rect(text)
        height += text_rect.height
    height += (len(text_list) - 1) * 24
    y = (window().get_height() - height) / 2
    for i in range(len(text_list)):
        text_rect = font.get_rect(text_list[i])
        x = (window().get_width() - text_rect.width) / 2
        draw_text(text_list[i], x, y + (text_rect.height + 24) * i, text_color, font)


def draw_fill_rect(width, height, x, y, bg):
    rect = pygame.Rect(x, y, width, height)
    pygame.draw.rect(window(), bg, rect, 0)