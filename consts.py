import pygame
from tkinter import Tk
import os

pygame.init()  # Инициализация проекта

# Константы, используемые в программе:
SCALE = 5  # Коэффициент масштаба окна
HALF_SCALE = SCALE // 2
WINDOW_WIDTH = 100 * SCALE
HEIGHT = 100 * SCALE
FPS = 60
SETTINGS_WIDTH = 400
ALL_WIDTH = WINDOW_WIDTH + SETTINGS_WIDTH
ALLOWED_X = (0, WINDOW_WIDTH)
TEXT_X = 700
TEXT_Y = 385
DELAY = 10
LINES = 'LINES'
ERASER = 'ERASER'

# Цвета
BLUE = (1, 140, 240, 255)
RED = (255, 36, 1, 255)
GREEN = (167, 252, 1, 255)
LIGHT_GRAY = (70, 70, 70, 255)
ORANGE = (255, 79, 1, 255)
DARK_GRAY = (50, 51, 50, 255)
GRAY = (60, 60, 59, 255)
YELLOW = (255, 186, 1, 255)
WHITE = (255, 255, 254, 255)
BLACK = (0, 0, 1, 255)
DARK_WHITE = (210, 209, 210, 255)
WHITE_GRAY = (100, 101, 100, 255)

# Звуки, изображения и шрифты, используемые в программе
ICON_IMAGE = pygame.image.load('images/character.png')
DOTS_S = pygame.mixer.Sound('sounds/dots.ogg')
DOTS_LINES_S = pygame.mixer.Sound('sounds/dots.mp3')
LINES_S = pygame.mixer.Sound('sounds/line.mp3')
ERASER_S = pygame.mixer.Sound('sounds/eraser.ogg')
SUCCESS_S = pygame.mixer.Sound('sounds/success.ogg')
ERROR_S = pygame.mixer.Sound('sounds/sharp.mp3')
UPDATE_S = pygame.mixer.Sound('sounds/update.ogg')
BUTTON_S = pygame.mixer.Sound('sounds/button.mp3')
pygame.mixer.music.load('sounds/draw.mp3')
FONT = pygame.font.SysFont('collibri', 36)

# Глобальные переменные
start_pos = None
start_pos_flag = False
end_pos = None
end_pos_flag = False
moving_flag = False
ground_color = None
default_start_pos = (SCALE * 2, SCALE * 2)
default_end_pos = (WINDOW_WIDTH - SCALE * 2, HEIGHT - SCALE * 2)
dots = []
mode = LINES
phase_drawing = True
image_loaded = False
log_flag = False
objects = []
reversed = False
allowed_splits = ['.jpg', '.jpeg', '.png']
path = 'dist/main/logs'
logs = []
log_page_number = 0
log_page_counter = 1
page_flag = False
prev_page = False
saved = False
fil_len = 0
DEVIATION = 0.5

# Инициализация проекта
SCREEN = pygame.display.set_mode((ALL_WIDTH, HEIGHT))
Tk().withdraw()
pygame.display.set_caption('Best way searcher')
pygame.display.set_icon(ICON_IMAGE)
SETTINGS = pygame.Surface((SETTINGS_WIDTH, HEIGHT))
SETTINGS.fill(DARK_GRAY)
CLOCK = pygame.time.Clock()
START = pygame.Surface((SCALE * 2, SCALE * 2))
START.fill(GREEN)
END = pygame.Surface((SCALE * 2, SCALE * 2))
END.fill(RED)
YELLOW_BLANK = pygame.Surface((WINDOW_WIDTH, HEIGHT))
YELLOW_BLANK.fill(YELLOW)
BLANK = pygame.surface.Surface((350, 175))
BLANK.fill(GRAY)
if HALF_SCALE >= 0:
    HALF_SCALE = 1
LINES_SIZE = SCALE
COMPRESSION = 1
if COMPRESSION < 1:
    COMPRESSION = 1
LINES_SCALE = 1
if COMPRESSION > 1:
    LINES_SCALE = COMPRESSION // 2
