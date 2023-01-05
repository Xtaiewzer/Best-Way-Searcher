import pygame
import sys
from shortestWaySearcher.BFS import *

# Основные параметры программы:
SCALE = 5  # Масштаб
HALF_SCALE = SCALE // 2
if HALF_SCALE >= 0:
    HALF_SCALE = 1
win_width = 100 * SCALE  # Ширина окна
win_height = 100 * SCALE  # Высота окна
win_fps = 60  # Частота кадров в секунду

# Цвета
BLUE = (0, 140, 240, 255)
RED = (255, 0, 0, 255)
GREEN = (0, 255, 0, 255)
GRAY = (70, 70, 70, 255)
ORANGE = (255, 104, 0, 255)

# Создание программы
pygame.init()
screen = pygame.display.set_mode((win_width, win_height))
clock = pygame.time.Clock()
START = pygame.Surface((SCALE, SCALE))
START.fill(BLUE)
END = pygame.Surface((SCALE, SCALE))
END.fill(RED)
char_image = pygame.image.load('character.png')

# Позиции и переменные
start_pos = None
start_pos_flag = False
end_pos = None
end_pos_flag = False
moving_flag = False
default_start_pos = (SCALE, SCALE)
default_end_pos = (win_width - SCALE * 2, win_height - SCALE * 2)
pods = []
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

        end_pos_flag = True
        pygame.display.set_caption('Now, draw the environment!')  # Забавная подсказка в названии окна программы


# Функция рисования:
def drawing(e):
    global lines

    pressed = pygame.mouse.get_pressed()  # Нажатые клавиши
    pos = pygame.mouse.get_pos()  # Позиция курсора мыши

    if e.type == pygame.KEYDOWN and (e.mod & pygame.KMOD_CTRL):  # Переключение режима:
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
            pods.append(p)  # Соединены все точки на экране
            pygame.draw.circle(screen, GREEN, p, HALF_SCALE)  # Рисование точек
        elif button == 3 and len(pods) >= 2:  # Если точек больше 2 и нажата ПКМ, они
            pygame.draw.lines(screen, GREEN, False, pods, SCALE * 2)  # Соединяются по очереди
            pods.clear()  # Очистка массива точек


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

while phase_drawing:
    clock.tick(win_fps)  # 1 цикл длятся 1/60 секунду
    for event in pygame.event.get():
        if event.type == pygame.QUIT:  # Если нажать на крестик или использовать
            sys.exit()  # Сочетание горячих клавиш Alt + F4, то программа закроется
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
        screen.blit(START, start_pos)
    if end_pos is not None:  # Обновление конечной точки
        screen.blit(END, end_pos)
    pygame.display.flip()  # Обновление границ экрана

# Точка старта и конечная точка представляют объект типа Surface соответствующего цвета
# В конце итерации цикла while phase_drawing они перерисовываются на экран для
# Исключения вариации их закрашивания, из-за чего будет сбой в программе

# Парсинг всей доступной информации на экране приложения в строку для последующей обработки:
scheme = ''  # Массив строк
s = None  # Координата точки старта
t = None  # Координата конечной точки
pygame.display.set_caption('Searching the shortest way...')  # Забавная подсказка в названии окна программы
for x in range(0, win_width, SCALE):  # Построчный перебор каждого пикселя на экране по оси x
    for y in range(0, win_height, SCALE):  # Построчный перебор каждого пикселя на экране по оси y
        pos = (x // 5, y // 5)  # Текущая позиция
        pix = screen.get_at((x, y))  # Получаем цвет в пикселе
        if pix == GREEN:  # Обработка для препятствий
            scheme += '#'
        elif pix == BLUE:  # Обработка для точки старта
            scheme += 'S'
            s = pos
        elif pix == RED:  # Обработка для конечной точки
            scheme += 'T'
            t = pos
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

way = SWM(scheme, s, t)  # Получаем путь от точки старта до конечной точки и расстояние этого пути
rect_hero = pygame.Rect(start_pos[0], start_pos[1], SCALE, SCALE)
win_fps *= 2
pygame.display.set_caption('Drawing the shortest way...')
if way[1] == INF:
    pass
else:
    for i in way[0]:
        pygame.draw.rect(screen, ORANGE, rect_hero, SCALE, SCALE)
        pygame.display.update(rect_hero)
        rect_hero.x += i[0] * SCALE
        rect_hero.y += i[1] * SCALE
        clock.tick(win_fps)

phase_moving = True
pygame.display.set_caption('The shortest way was drawn! Its length is: ' + str(way[1]))
while phase_moving:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
