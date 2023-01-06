import pygame
import sys
from buttons import Button
from shortestWaySearcher.BFS import *

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

# Цвета
BLUE = (0, 140, 240, 255)
RED = (255, 0, 0, 255)
GREEN = (0, 255, 0, 255)
GRAY = (70, 70, 70, 255)
ORANGE = (255, 79, 0, 255)

# Создание программы
pygame.init()
screen = pygame.display.set_mode((all_width, win_height))
clock = pygame.time.Clock()
START = pygame.Surface((SCALE * 2, SCALE * 2))
START.fill(BLUE)
END = pygame.Surface((SCALE * 2, SCALE * 2))
END.fill(RED)
objects = []
font = pygame.font.SysFont('Arial', 40)
char_image = pygame.image.load('character.png')
dots_s = pygame.mixer.Sound('sounds/dots.ogg')
lines_s = pygame.mixer.Sound('sounds/lines.ogg')

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


# Функция, создающая точку старта
def starting():
    global start_pos, start_pos_flag

    if event.type == pygame.MOUSEBUTTONDOWN:
        pos = event.pos
        color = screen.get_at(pos)

        if color == GREEN:  # Защита на дурака:
            start_pos = default_start_pos  # Нельзя создать точку на границе поля
        else:
            start_pos = pos

        dots_s.play()
        start_pos_flag = True


# Функция, создающая конечную точку
def ending():
    global end_pos, end_pos_flag, default_end_pos

    if event.type == pygame.MOUSEBUTTONDOWN:
        pos = event.pos
        color = screen.get_at(pos)

        if screen.get_at(default_end_pos) == BLUE:  # Защита от дурака:
            default_end_pos = default_start_pos  # Если в координатах конечной точки по умолчанию
            # Находится конечная точка, то координаты конечной
            # Точки равны координатам по умолчанию точки старта
        if color == GREEN or color == BLUE:
            end_pos = default_end_pos  # Нельзя создать точку на границе поля или на точке старта
        else:
            end_pos = pos

        dots_s.play()
        end_pos_flag = True
        pygame.display.set_caption('Now, draw the environment!')  # Забавная подсказка в названии окна программы


# Функция рисования:
def drawing(e):
    global lines

    pressed = pygame.mouse.get_pressed()  # Нажатые клавиши
    pos = pygame.mouse.get_pos()  # Позиция курсора мыши

    if e.type == pygame.KEYDOWN and (e.mod & pygame.KMOD_CTRL) \
            and not len(dots):  # Переключение режима:
        lines = not lines  # Нажатием на ctrl можно чередовать режим рисования линий режимом ластика

    if lines:  # Режим рисования линий
        drawing_lines(e, pos)
    else:  # Режим ластика
        if pressed[0]:  # Если нажата ЛКМ
            pygame.draw.circle(screen, GRAY, pos, SCALE * 2)


# Режим рисования линий:
def drawing_lines(e, p):
    if e.type == pygame.MOUSEBUTTONDOWN:  # Если нажать ЛКМ, то
        button = e.button  # В этом месте экрана будет нарисована точка
        if button == 1:  # Если нажать ПКМ, то по очереди будут соединены все точки на экране
            dots.append(p)  # Соединены все точки на экране
            pygame.draw.circle(screen, GREEN, p, HALF_SCALE)  # Рисование точек
            dots_s.play()
        elif button == 3 and len(dots) >= 2:  # Если точек больше 2 и нажата ПКМ, они
            pygame.draw.lines(screen, GREEN, False, dots, SCALE * LINES_SCALE)  # Соединяются по очереди
            dots.clear()  # Очистка массива точек
            lines_s.play()


# Класс персонажа
class Character(pygame.sprite.Sprite):
    def __init__(self):  # Инициализация персонажа
        pygame.sprite.Sprite.__init__(self)
        self.image = char_image
        self.rect = self.image.get_rect()
        self.rect.center = (start_pos[0], start_pos[1])


# Подготовка к запуску первой стадии программы
pygame.display.set_caption('Set start and end points')  # Забавная подсказка в названии окна программы
screen.fill(GRAY)  # Заполнение экрана серым
pygame.display.update()  # Заполнение экрана серым
phase_drawing = True  # Фаза рисования
pygame.draw.rect(screen, GREEN, (0, 0, win_width, win_height), SCALE)  # Рисование границ
update_Button = Button(screen, 600, 30, 150, 75, 'update')
objects.append(update_Button)

while phase_drawing:
    clock.tick(win_fps) # 1 цикл длятся 1/60 секунду
    for obj in objects:
        obj.process()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:  # Если нажать на крестик или использовать
            sys.exit()  # Сочетание горячих клавиш Alt + F4, то программа закроется
        if allow_x[0] < pygame.mouse.get_pos()[0] < allow_x[1]:
            if not start_pos_flag:  # Создание точки старта
                starting()
                pygame.draw.rect(screen, GREEN, (0, 0, SCALE, SCALE))
            elif not end_pos_flag:  # Создание конечной точки
                ending()
                pygame.draw.rect(screen, GREEN, (0, 0, SCALE, SCALE))
            elif end_pos_flag:  # Рисование
                drawing(event)
            if event.type == pygame.KEYDOWN and end_pos_flag:  # Завершение фазы рисования при
                if event.key == pygame.K_SPACE:  # Нажатии на пробел и создания конечной точки
                    phase_drawing = False  # И точки старты
    pygame.draw.rect(screen, GREEN, (0, 0, win_width, win_height), SCALE)  # Обновление границ
    if start_pos is not None:  # Обновление точки старта
        screen.blit(START, (start_pos[0] - SCALE, start_pos[1] - SCALE))
    if end_pos is not None:  # Обновление конечной точки
        screen.blit(END, (end_pos[0] - SCALE, end_pos[1] - SCALE))
    pygame.display.update()  # Обновление границ экрана

# Точка старта и конечная точка представляют объект типа Surface соответствующего цвета
# В конце итерации цикла while phase_drawing они перерисовываются на экран для
# Исключения вариации их закрашивания, из-за чего будет сбой в программе

# Парсинг всей доступной информации на экране приложения в строку для последующей обработки:
scheme = ''  # Массив строк
pygame.display.set_caption('Searching the shortest way...')  # Забавная подсказка в названии окна программы
for x in range(0, win_width, COMPRESSION):  # Построчный перебор каждого пикселя на экране по оси x
    for y in range(0, win_height, COMPRESSION):  # Построчный перебор каждого пикселя на экране по оси y
        pos = (x // COMPRESSION, y // COMPRESSION)  # Текущая позиция
        pix = screen.get_at((x, y))  # Получаем цвет в пикселе
        if pix == GREEN:  # Обработка для препятствий
            scheme += '#'
        else:  # Обработка для пустых (серых) точек на экране
            scheme += '.'
    scheme += '\n'  # Добавление строки в массив
# print(scheme)
scheme = scheme.split('\n')  # Преобразование получившейся строки в массив строк

# Создание спрайта персонажа
# all_sprites = pygame.sprite.Group()
# char = Character()
# all_sprites.add(char)
# all_sprites.draw(screen)

way = SWM(scheme, (start_pos[0] // COMPRESSION, start_pos[1] // COMPRESSION),
          (end_pos[0] // COMPRESSION,
           end_pos[1] // COMPRESSION))
# Получаем путь от точки старта до конечной точки и расстояние этого пути
rect_hero = pygame.Rect(start_pos[0], start_pos[1], SCALE, SCALE)
if COMPRESSION == 1:
    win_fps *= SCALE
else:
    win_fps *= LINES_SCALE

if way[1] < INF:
    pygame.display.set_caption('Drawing the shortest way...')
    rect_hero.x -= HALF_SCALE
    rect_hero.y -= HALF_SCALE
    for i in way[0]:
        pygame.draw.rect(screen, ORANGE, rect_hero, SCALE, SCALE)
        pygame.display.update(rect_hero)
        rect_hero.x += i[0] * COMPRESSION
        rect_hero.y += i[1] * COMPRESSION
        clock.tick(win_fps)
    pygame.display.set_caption('The shortest way fas drawn! Its length is: ' + str(way[1] * COMPRESSION))
else:
    pygame.display.set_caption('I am sorry, but I cannot find the shortest way :(')

phase_moving = True
while phase_moving:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
