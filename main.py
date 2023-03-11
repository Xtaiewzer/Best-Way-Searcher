#import PIL
import sys
import random
import pygame.event
from Wave_algorythm import *
from consts import *


# С помощью этой функции создается стартовая точка
def starting(event):
    global start_pos, start_pos_flag

    if event.type == pygame.MOUSEBUTTONDOWN:
        pos = event.pos
        color = SCREEN.get_at(pos)

        if color == YELLOW:
            start_pos = default_start_pos
        else:
            start_pos = pos

        DOTS_S.play()
        start_pos_flag = True


# С помощью этой функции создается конечная точка
def ending(event):
    global end_pos, end_pos_flag, default_end_pos

    if event.type == pygame.MOUSEBUTTONDOWN:
        pos = event.pos
        color = SCREEN.get_at(pos)

        if SCREEN.get_at(default_end_pos) == GREEN:
            default_end_pos = default_start_pos

        if color == YELLOW or color == GREEN:
            end_pos = default_end_pos
        else:
            end_pos = pos

        DOTS_S.play()
        end_pos_flag = True


# С помощью этой функции происходит рисование линий на экране
def drawing(e):
    global mode, DELAY
    pressed = pygame.mouse.get_pressed()
    pos = pygame.mouse.get_pos()
    if mode == LINES:
        drawing_lines(e, pos)
    else:  # Eraser mode
        if pressed[0]:
            pygame.draw.circle(SCREEN, LIGHT_GRAY, pos, SCALE * 2)
            DELAY += 1
            if DELAY % 10 == 0:
                ERASER_S.play()
                DELAY = 0


# Функция для смены режима:
# Eraser mode <-> Lines mode
def change_mode():
    global mode
    if mode == LINES:
        mode = ERASER
    else:
        mode = LINES


# С помощью этой функции ставятся и соединяются точки на графе
def drawing_lines(e, p):
    if e.type == pygame.MOUSEBUTTONDOWN:
        button = e.button
        if button == 1:
            dots.append(p)
            pygame.draw.circle(SCREEN, YELLOW, p, HALF_SCALE)
            DOTS_LINES_S.play()
        elif button == 3 and len(dots) >= 2:
            link_dots()


# Функция, соединяющая точки на графе
def link_dots():
    pygame.draw.lines(SCREEN, YELLOW, False, dots, SCALE * LINES_SCALE)
    dots.clear()
    LINES_S.play()


# Функция для обработки кнопок и обновления экрана
def funcs():
    for e in pygame.event.get():
        buttons(e)
        pygame.display.update()


# Функция для обновления поля
def restart():
    global start_pos_flag, start_pos, end_pos, end_pos_flag, \
        default_end_pos, default_start_pos, dots, mode, objects, \
        phase_drawing

    pygame.mixer.music.stop()
    UPDATE_S.play()
    start_pos = None
    phase_drawing = True
    start_pos_flag = False
    end_pos = None
    end_pos_flag = False
    default_start_pos = (SCALE * 2, SCALE * 2)
    default_end_pos = (WINDOW_WIDTH - SCALE * 2, HEIGHT - SCALE * 2)
    dots = []
    mode = LINES
    objects = []
    run()


# Функция для завершения работы приложения
def close(e):
    if e.type == pygame.QUIT:
        sys.exit()


# Кнопка для перезапуска программы
def rst_button(event):
    button_surf = pygame.Surface((55, 55))
    text = FONT.render('R', True, BLACK)
    center = (700, 550)
    text_rect = text.get_rect(center=center)
    button = button_surf.get_rect(center=center)
    button_surf.fill(WHITE)
    mouse_pos = pygame.mouse.get_pos()
    if button.collidepoint(mouse_pos):
        button_surf.fill(LIGHT_GRAY)
        if event.type == pygame.MOUSEBUTTONDOWN:
            restart()
            BUTTON_S.play()
    SCREEN.blit(button_surf, button)
    SCREEN.blit(text, text_rect)


# Функция для случайного заполнения поля
def randomizer_pos():
    global start_pos, start_pos_flag, end_pos, end_pos_flag
    start_pos = (random.randint(SCALE * 2, WINDOW_WIDTH - SCALE * 2)
                 , random.randint(SCALE * 2, HEIGHT - SCALE * 2))
    end_pos = (random.randint(SCALE * 2, WINDOW_WIDTH - SCALE * 2)
               , random.randint(SCALE * 2, HEIGHT - SCALE * 2))
    start_pos_flag = True
    end_pos_flag = True


# Функция для случайного заполнения массива точек
def randomizer_dots():
    global dots
    for i in range(2, 4):
        for j in range(i):
            randx = random.randint(0, WINDOW_WIDTH - SCALE)
            randy = random.randint(0, HEIGHT - SCALE)
            dots.append((randx, randy))
        link_dots()
    for i in range(2, 8):
        for j in range(i):
            randx = random.randint(0, WINDOW_WIDTH - SCALE)
            randy = random.randint(0, HEIGHT - SCALE)
            pygame.draw.circle(SCREEN, YELLOW, (randx, randy), i)


#  Кнопка для случайного заполнения поля
def random_button(event):
    button_surf = pygame.Surface((150, 55))
    text = FONT.render('RANDOM', True, BLACK)
    center = (800, 50)
    text_rect = text.get_rect(center=center)
    button = button_surf.get_rect(center=center)
    if phase_drawing and end_pos_flag and not len(dots):
        button_surf.fill(WHITE)
        mouse_pos = pygame.mouse.get_pos()
        if button.collidepoint(mouse_pos):
            button_surf.fill(LIGHT_GRAY)
            if event.type == pygame.MOUSEBUTTONDOWN:
                randomizer_dots()
    elif not start_pos_flag and not len(dots):
        button_surf.fill(WHITE)
        mouse_pos = pygame.mouse.get_pos()
        if button.collidepoint(mouse_pos):
            button_surf.fill(LIGHT_GRAY)
            if event.type == pygame.MOUSEBUTTONDOWN:
                DOTS_S.play()
                randomizer_pos()
    else:
        button_surf.fill(LIGHT_GRAY)
    SCREEN.blit(button_surf, button)
    SCREEN.blit(text, text_rect)


# Кнопка для рисования
def draw_button(event):
    button_surf = pygame.Surface((150, 55))
    text = FONT.render('DRAW', True, BLACK)
    center = (600, 150)
    text_rect = text.get_rect(center=center)
    button = button_surf.get_rect(center=center)
    if phase_drawing and end_pos_flag and len(dots) > 1 \
            and mode == LINES:
        button_surf.fill(WHITE)
        mouse_pos = pygame.mouse.get_pos()
        if button.collidepoint(mouse_pos):
            button_surf.fill(LIGHT_GRAY)
            if event.type == pygame.MOUSEBUTTONDOWN:
                link_dots()
    else:
        button_surf.fill(LIGHT_GRAY)
    SCREEN.blit(button_surf, button)
    SCREEN.blit(text, text_rect)


# Кнопка для активации алгоритма поиска кратчайшего пути
def test_button(event):
    global phase_drawing
    button_surf = pygame.Surface((150, 55))
    text = FONT.render('TEST', True, BLACK)
    center = (600, 50)
    text_rect = text.get_rect(center=center)
    button = button_surf.get_rect(center=center)
    if phase_drawing and end_pos_flag and not len(dots):
        button_surf.fill(WHITE)
        mouse_pos = pygame.mouse.get_pos()
        if button.collidepoint(mouse_pos):
            button_surf.fill(LIGHT_GRAY)
            if event.type == pygame.MOUSEBUTTONDOWN:
                phase_drawing = False
                BUTTON_S.play()
    else:
        button_surf.fill(LIGHT_GRAY)
    SCREEN.blit(button_surf, button)
    SCREEN.blit(text, text_rect)


# Кнопка для смены режима:
# Eraser mode <-> Lines mode
def mode_button(event):
    button_surf = pygame.Surface((150, 55))
    text = FONT.render(mode, True, BLACK)
    center = (800, 150)
    text_rect = text.get_rect(center=center)
    button = button_surf.get_rect(center=center)
    if phase_drawing and end_pos_flag and not len(dots):
        button_surf.fill(WHITE)
        mouse_pos = pygame.mouse.get_pos()
        if button.collidepoint(mouse_pos):
            button_surf.fill(LIGHT_GRAY)
            if event.type == pygame.MOUSEBUTTONDOWN:
                change_mode()
                BUTTON_S.play()
    else:
        button_surf.fill(LIGHT_GRAY)
    SCREEN.blit(button_surf, button)
    SCREEN.blit(text, text_rect)


def image_button(event):
    button_surf = pygame.Surface((150, 55))
    text = FONT.render('IMAGE', True, BLACK)
    center = (600, 250)
    text_rect = text.get_rect(center=center)
    button = button_surf.get_rect(center=center)
    button_surf.fill(WHITE)
    mouse_pos = pygame.mouse.get_pos()
    if button.collidepoint(mouse_pos):
        button_surf.fill(LIGHT_GRAY)
        if event.type == pygame.MOUSEBUTTONDOWN:
            BUTTON_S.play()
            image_loading('images/lab.png')
    else:
        button_surf.fill(WHITE)
    SCREEN.blit(button_surf, button)
    SCREEN.blit(text, text_rect)


def image_loading(filename):
    image = pygame.image.load(filename)
    image = pygame.transform.scale(image, (WINDOW_WIDTH, HEIGHT))
    image_rect = image.get_rect(center=(250, 250))
    SCREEN.blit(image, image_rect)


# Функция для вывода текста в специальное окошко
def screen_text(text, c_x, c_y):
    scr_text = FONT.render(text, True, WHITE)
    scr_text_rect = scr_text.get_rect(center=(c_x, c_y))
    SCREEN.blit(scr_text, scr_text_rect)


# Функция для обновления текста на текстовом экране
def put_blank():
    SCREEN.blit(BLANK, (525, 300))
    pygame.draw.line(SCREEN, YELLOW, (525, 300), (875, 300), 5)
    pygame.draw.line(SCREEN, YELLOW, (525, 475), (875, 475), 5)


# Функция для обработки кнопок
def buttons(e):
    close(e)
    #rst_button(e)
    random_button(e)
    draw_button(e)
    test_button(e)
    mode_button(e)
    image_button(e)


# Функция для запуска программы
def run():
    global phase_drawing
    SCREEN.fill(LIGHT_GRAY)
    pygame.display.update()
    SCREEN.blit(SETTINGS, (WINDOW_WIDTH, 0))
    put_blank()
    screen_text('Set start position', TEXT_X, TEXT_Y)

    # Этап для установки начальной и конечной точек и рисования:
    while phase_drawing:
        CLOCK.tick(FPS)
        for e in pygame.event.get():
            buttons(e)
            if ALLOWED_X[0] < pygame.mouse.get_pos()[0] < ALLOWED_X[1]:
                # Отмечается стартовая точка и конечная точка;
                if not start_pos_flag:
                    starting(e)
                    pygame.draw.rect(SCREEN, YELLOW, (0, 0, SCALE, SCALE))
                elif not end_pos_flag:
                    ending(e)
                    pygame.draw.rect(SCREEN, YELLOW, (0, 0, SCALE, SCALE))
                    put_blank()
                    screen_text('Set finish position', TEXT_X, TEXT_Y)
                    # Создаются препятствия
                elif end_pos_flag:
                    put_blank()
                    screen_text('Now, draw the environment', TEXT_X, TEXT_Y)
                    drawing(e)
        pygame.draw.rect(SCREEN, YELLOW, (0, 0, WINDOW_WIDTH, HEIGHT), SCALE)
        if start_pos is not None:
            SCREEN.blit(START, (start_pos[0] - SCALE, start_pos[1] - SCALE))
        if end_pos is not None:
            SCREEN.blit(END, (end_pos[0] - SCALE, end_pos[1] - SCALE))
        pygame.display.update()

    # Этап обработки поля в схему для
    # последующей обработки алгоритмом
    scheme = [[None] * HEIGHT for _ in range(WINDOW_WIDTH)]
    put_blank()
    screen_text('Searching the shortest way...', TEXT_X, TEXT_Y)
    pygame.display.update()
    for x in range(0, WINDOW_WIDTH, COMPRESSION):
        for y in range(0, HEIGHT, COMPRESSION):
            funcs()
            pix = SCREEN.get_at((x, y))
            if pix == YELLOW:
                scheme[x][y] = False
            else:
                scheme[x][y] = True

    # Схема отправляется на обработку алгоритму
    way = Wave_algorythm(scheme, (start_pos[0] // COMPRESSION, start_pos[1] // COMPRESSION),
                         (end_pos[0] // COMPRESSION,
                          end_pos[1] // COMPRESSION))
    rect_hero = pygame.Rect(start_pos[0], start_pos[1], SCALE, SCALE)
    pygame.display.update()
    length = len(way)

    # Обработка схемы движение и вывод кратчайшего пути на экран
    if length:
        put_blank()
        screen_text('Drawing the shortest way...', TEXT_X, TEXT_Y)
        pygame.display.update()
        pygame.mixer.music.play(-1)
        for i in way:
            funcs()
            pygame.draw.rect(SCREEN, ORANGE, rect_hero, SCALE, SCALE)
            pygame.display.update(rect_hero)
            rect_hero.x += i[0] * COMPRESSION
            rect_hero.y += i[1] * COMPRESSION
            pygame.time.wait(SCALE)
        put_blank()
        screen_text('The shortest way is drawn', TEXT_X, TEXT_Y - 20)
        screen_text('Its length is ' + str(length * COMPRESSION) + ' pixels', TEXT_X, TEXT_Y + 30)
        pygame.mixer.music.stop()
        SUCCESS_S.play()
        pygame.display.update()
    else:  # Алгоритм не смог вычислить кратчайший путь
        put_blank()
        screen_text('Sorry, but the algorithm', TEXT_X, TEXT_Y - 25)
        screen_text('did not find the shortest way', TEXT_X, TEXT_Y + 25)
        ERROR_S.play()
        pygame.display.update()

    # Конец работы программы и ожидание последующих действий
    while 1:
        funcs()
        CLOCK.tick(FPS)


# Запуск программы
if __name__ == "__main__":
    run()
