import pygame


pygame.init()
# Основные параметры программы:
SCALE = 5  # Масштаб
HALF_SCALE = SCALE // 2
if HALF_SCALE >= 0:
    HALF_SCALE = 1
LINES_SIZE = SCALE
COMPRESSION = 1
if COMPRESSION < 1:
    COMPRESSION = 1
LINES_SCALE = 1
if COMPRESSION > 1:
    LINES_SCALE = COMPRESSION // 2
win_width = 100 * SCALE  # Ширина окна
win_height = 100 * SCALE  # Высота окна
win_fps = 60  # Частота кадров в секунду
set_width = 400
all_width = win_width + set_width
allow_x = (0, win_width)
delay = 10

# Цвета
BLUE = (0, 140, 240, 255)
RED = (255, 36, 0, 255)
GREEN = (167, 252, 0, 255)
GRAY = (70, 70, 70, 255)
ORANGE = (255, 79, 0, 255)
DARK_GRAY = (50, 50, 50, 255)
YELLOW = (255, 186, 0, 255)
WHITE = (255, 255, 255, 255)
BLACK = (0, 0, 0, 255)

# Позиции и переменные
start_pos = None
start_pos_flag = False
end_pos = None
end_pos_flag = False
moving_flag = False
default_start_pos = (SCALE * 2, SCALE * 2)
default_end_pos = (win_width - SCALE * 2, win_height - SCALE * 2)
dots = []
lines = True
objects = []
icon_image = pygame.image.load('character.png')
dots_s = pygame.mixer.Sound('sounds/dots (2).ogg')
lines_s = pygame.mixer.Sound('sounds/lines.ogg')
eraser_s = pygame.mixer.Sound('sounds/eraser.ogg')
success_s = pygame.mixer.Sound('sounds/success.ogg')
error_s = pygame.mixer.Sound('sounds/error.ogg')
update_s = pygame.mixer.Sound('sounds/update.ogg')
font = pygame.font.SysFont('collibri', 36)
