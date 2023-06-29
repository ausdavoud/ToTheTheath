import pygame
import pygame.freetype
import os

pygame.init()
font_path = os.path.join('game', 'lexend.ttf')
text_font = pygame.freetype.Font(font_path, 18)
header_font = pygame.freetype.Font(font_path, 22)

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GRAY = (230, 230, 230)


def window(): return pygame.display.get_surface()


def draw_text(text, x, y, text_color=BLACK, font=text_font):
    font.render_to(window(), (x, y), text, text_color)


def draw_center_text(text, font=header_font, color=BLACK):
    text_rect = font.get_rect(text)
    x = (window().get_width() - text_rect.width) / 2
    y = (window().get_height() - text_rect.height) / 2
    destination = (x, y)
    font.render_to(window(), destination, text, color)


def draw_fill_rect(width, height, x, y, bg=GRAY):
    rect = pygame.Rect(x, y, width, height)
    pygame.draw.rect(window(), bg, rect, 0)
