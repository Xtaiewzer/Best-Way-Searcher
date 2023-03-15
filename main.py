import shutil
import sys
import os
import random
import pygame.event
from Wave_algorythm import *
from consts import *
from History import Log, image_handling
from tkinter import filedialog


# С помощью этой функции создается стартовая точка
def starting(event):
    global start_pos, start_pos_flag

    if event.type == pygame.MOUSEBUTTONDOWN and ALLOWED_X[0] < pygame.mouse.get_pos()[0] < ALLOWED_X[1]:
        start_pos = event.pos

        DOTS_S.play()
        start_pos_flag = True


# С помощью этой функции создается конечная точка
def ending(event):
    global end_pos, end_pos_flag
    if event.type == pygame.MOUSEBUTTONDOWN and ALLOWED_X[0] < pygame.mouse.get_pos()[0] < ALLOWED_X[1]:
        end_pos = event.pos

        DOTS_S.play()
        end_pos_flag = True


# Проверка позоций стартовой и конечной точек на корректность
def check_pos_on_valid():
    global end_pos, start_pos

    if start_pos is not None:
        while SCREEN.get_at(start_pos) == YELLOW:
            start_pos = get_random_tuple()

    if end_pos is not None:
        color = SCREEN.get_at(end_pos)
        while color == YELLOW:
            end_pos = get_random_tuple()
            color = SCREEN.get_at(end_pos)


# С помощью этой функции происходит рисование линий на экране
def drawing(e):
    global mode, DELAY
    if ALLOWED_X[0] < pygame.mouse.get_pos()[0] < ALLOWED_X[1]:
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
    if len(dots) != 0:
        link_dots()
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
    if len(dots) == 0:
        return
    if len(dots) == 1:
        dots.append(get_random_tuple())
    pygame.draw.lines(SCREEN, YELLOW, False, dots, SCALE * LINES_SCALE)
    dots.clear()
    LINES_S.play()


# Функция для обработки кнопок и обновления экрана
def check_on_close():
    for e in pygame.event.get():
        buttons_and_events(e)
        pygame.display.update()


# Функция для обновления поля
def restart():
    global start_pos_flag, start_pos, end_pos, end_pos_flag, \
        default_end_pos, default_start_pos, dots, mode, objects, \
        phase_drawing, ground_color

    pygame.mixer.music.stop()
    UPDATE_S.play()
    start_pos = None
    phase_drawing = True
    start_pos_flag = False
    end_pos = None
    ground_color = None
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
def restart_button(event):
    button_surf = pygame.Surface((150, 55))
    text = FONT.render('RESTART', True, BLACK)
    center = (800, 50)
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

# Проверка на соответствие цвета поверхности
def check_deviation(pix):
    deviation = 0.5
    return pix != YELLOW and (ground_color[0] - deviation * ground_color[0] <= pix[0] <=
                              ground_color[0] + deviation * ground_color[0]) and \
        (ground_color[1] - deviation * ground_color[1] <= pix[1] <=
         ground_color[1] + deviation * ground_color[1]) and \
        (ground_color[2] - deviation * ground_color[2] <= pix[2] <=
         ground_color[2] + deviation * ground_color[2]) or pix == GREEN \
        or pix == RED or pix == LIGHT_GRAY


# Функция для случайного заполнения поля
def randomizer_pos():
    global start_pos, start_pos_flag, end_pos, end_pos_flag
    if not start_pos_flag:
        start_pos = (get_random_tuple())
        start_pos_flag = True
    if not end_pos_flag:
        end_pos = (get_random_tuple())
        end_pos_flag = True
    DOTS_S.play()
    check_pos_on_valid()


# Функция для случайного заполнения массива точек
def get_random_tuple():
    return (random.randint(0, WINDOW_WIDTH - SCALE),
            random.randint(0, HEIGHT - SCALE))


# Функция для случайного заполнения экрана
def randomizer_dots():
    for i in range(2, 4):
        for j in range(i):
            dots.append(get_random_tuple())
        link_dots()
    for i in range(2, 8):
        for j in range(i):
            pygame.draw.circle(SCREEN, YELLOW, get_random_tuple(), i)

# Кнопка для рисования
def draw_button(event):
    button_surf = pygame.Surface((150, 55))
    text = FONT.render('DRAW', True, BLACK)
    center = (600, 150)
    text_rect = text.get_rect(center=center)
    button = button_surf.get_rect(center=center)
    if phase_drawing and not end_pos_flag and len(dots) > 0 \
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


# Функция для активации алгоритма поиска кратчайшего пути
def next_function():
    global phase_drawing
    if phase_drawing:
        link_dots()
        phase_drawing = False
        BUTTON_S.play()


# Горячая клавиша для активации алгоритма поиска кратчайшего пути
def next_hotkey(event):
    if event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
        next_function()


# Кнопка для активации алгоритма поиска кратчайшего пути
def next_button(event):
    button_surf = pygame.Surface((150, 55))
    text = FONT.render('NEXT', True, BLACK)
    center = (600, 50)
    text_rect = text.get_rect(center=center)
    button = button_surf.get_rect(center=center)
    if phase_drawing:
        button_surf.fill(WHITE)
        mouse_pos = pygame.mouse.get_pos()
        if button.collidepoint(mouse_pos):
            button_surf.fill(LIGHT_GRAY)
            if event.type == pygame.MOUSEBUTTONDOWN:
                next_function()
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
    if phase_drawing and not end_pos_flag:
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

# Функция кнопки для загрузки изображений
def image_button(event):
    global image_loaded
    button_surf = pygame.Surface((150, 55))
    text = FONT.render('IMAGE', True, BLACK)
    center = (600, 250)
    text_rect = text.get_rect(center=center)
    button = button_surf.get_rect(center=center)
    button_surf.fill(WHITE)
    mouse_pos = pygame.mouse.get_pos()
    if phase_drawing:
        if button.collidepoint(mouse_pos):
            button_surf.fill(LIGHT_GRAY)
            if event.type == pygame.MOUSEBUTTONDOWN:
                BUTTON_S.play()
                try:
                    new_image = filedialog.askopenfilename(filetypes=[
                        ('image', '*.jpeg*'),
                        ('image', '*.jpg*'),
                        ('image', '*.png*')
                    ])
                    image_loading(new_image)
                    for dirs, folders, files in os.walk(path):
                        shutil.copy2(new_image, dirs)
                    image_loaded = True
                except:
                    put_blank()
                    screen_text('Cannot upload the image', TEXT_X, TEXT_Y)
                    image_loaded = False
    else:
        button_surf.fill(LIGHT_GRAY)
    SCREEN.blit(button_surf, button)
    SCREEN.blit(text, text_rect)


# Кнопка для просмотра последних макетов
def log_button(event):
    global log_flag

    button_surf = pygame.Surface((150, 55))
    text = FONT.render('LOG', True, BLACK)
    center = (800, 250)
    text_rect = text.get_rect(center=center)
    button = button_surf.get_rect(center=center)
    button_surf.fill(WHITE)
    mouse_pos = pygame.mouse.get_pos()
    if phase_drawing:
        if button.collidepoint(mouse_pos):
            button_surf.fill(LIGHT_GRAY)
            if event.type == pygame.MOUSEBUTTONDOWN:
                BUTTON_S.play()
                reversed = False
                for dirs, folders, files in os.walk(path):
                    if not reversed:
                        files.reverse()
                        reversed = True
                    for i in range(len(files)):
                        if os.path.splitext(files[i])[1] in allowed_splits:
                            obj = Log(dirs + '/' + files[i], i, files[i])
                            logs.append(obj)
                        if len(logs) == 6:
                            break
                log_flag = True
    else:
        button_surf.fill(LIGHT_GRAY)
    SCREEN.blit(button_surf, button)
    SCREEN.blit(text, text_rect)


# Функция кнопки журнала загрузок
def log_back_button(event):
    global log_flag

    button_surf = pygame.Surface((100, 35))
    text = FONT.render('BACK', True, BLACK)
    center = (850, 470)
    text_rect = text.get_rect(center=center)
    button = button_surf.get_rect(center=center)
    button_surf.fill(WHITE)
    mouse_pos = pygame.mouse.get_pos()
    surf = pygame.Surface((400, 500))
    surf.fill(GRAY)
    surf_rect = surf.get_rect(center=(WINDOW_WIDTH + SETTINGS_WIDTH / 2, HEIGHT / 2))
    if not end_pos_flag:
        if button.collidepoint(mouse_pos):
            button_surf.fill(LIGHT_GRAY)
            if event.type == pygame.MOUSEBUTTONDOWN:
                BUTTON_S.play()
                SCREEN.blit(surf, surf_rect)
                log_flag = False
    else:
        button_surf.fill(LIGHT_GRAY)
    SCREEN.blit(button_surf, button)
    SCREEN.blit(text, text_rect)


# Функция для случайного заполнения поля
def random_hotkey(event):
    if event.type == pygame.KEYDOWN and event.key == pygame.K_r:
        if phase_drawing:
            randomizer_dots()
        elif not phase_drawing:
            randomizer_pos()

# функция загрузки изображения
def image_loading(filename):
    SCREEN.blit(YELLOW_BLANK, (0, 0))
    image = image_handling(pygame.image.load(filename))
    SCREEN.blit(image, image.get_rect(center=(WINDOW_WIDTH // 2, HEIGHT // 2)))


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
def buttons_and_events(event):
    close(event)
    global log_flag
    if not log_flag:
        restart_button(event)
        log_button(event)
        random_hotkey(event)
        draw_button(event)
        next_button(event)
        mode_button(event)
        next_hotkey(event)
        image_button(event)
    else:
        surf = pygame.Surface((400, 500))
        surf.fill(DARK_GRAY)
        surf_rect = surf.get_rect(center=(WINDOW_WIDTH + SETTINGS_WIDTH / 2, HEIGHT / 2))
        SCREEN.blit(surf, surf_rect)
        log_back_button(event)
        if not log_flag:
            SCREEN.blit(surf, surf_rect)
            logs.clear()
            put_blank()
        for j in logs:
            if not log_flag:
                logs.clear()
                put_blank()
                break
            j.display(event)
            if j.clicked:
                log_flag = False
                SCREEN.blit(YELLOW_BLANK, (0, 0))
                SCREEN.blit(surf, surf_rect)
                SCREEN.blit(j.preview, j.preview_rect)
                j.clicked = False
                logs.clear()
                put_blank()
                screen_text('Draw the environment', TEXT_X, TEXT_Y)
                break
            if j.del_click:
                logs.remove(j)
                os.remove(j.filename)


def joke():
    pygame.display.set_caption('Пупс Хантер')
    pygame.display.set_icon(pygame.image.load('logs/photo_2023-01-23_21-51-53.jpg'))
    face = pygame.image.load('logs/photo_2023-01-23_21-51-53.jpg')
    face = pygame.transform.scale(face, (500, 500))
    SCREEN.blit(face, (0, 0))


# Функция для запуска программы
def run():
    global phase_drawing, ground_color
    SCREEN.fill(LIGHT_GRAY)
    # joke()
    pygame.display.update()
    SCREEN.blit(SETTINGS, (WINDOW_WIDTH, 0))
    put_blank()
    screen_text('Draw the environment', TEXT_X, TEXT_Y)
    pygame.display.update()

    # Этап для установки начальной и конечной точек и рисования:
    while not end_pos_flag:
        CLOCK.tick(FPS)
        for e in pygame.event.get():
            buttons_and_events(e)
            if not log_flag:
                # Отмечается стартовая точка и конечная точка;
                if not start_pos_flag and not phase_drawing:
                    starting(e)
                    pygame.draw.rect(SCREEN, YELLOW, (0, 0, SCALE, SCALE))
                    check_pos_on_valid()
                elif not end_pos_flag and not phase_drawing:
                    ending(e)
                    pygame.draw.rect(SCREEN, YELLOW, (0, 0, SCALE, SCALE))
                    put_blank()
                    screen_text('Set finish position', TEXT_X, TEXT_Y)
                    check_pos_on_valid()

                # Создаются препятствия
                elif not start_pos_flag and not end_pos_flag:
                    put_blank()
                    screen_text('Draw the environment', TEXT_X, TEXT_Y)
                    drawing(e)

        pygame.draw.rect(SCREEN, YELLOW, (0, 0, WINDOW_WIDTH, HEIGHT), SCALE)
        if start_pos is not None and not log_flag:
            if ground_color is None:
                ground_color = SCREEN.get_at(start_pos)
            SCREEN.blit(START, (start_pos[0] - SCALE, start_pos[1] - SCALE))
        if end_pos is not None:
            SCREEN.blit(END, (end_pos[0] - SCALE, end_pos[1] - SCALE))
        pygame.display.update()

    # Этап обработки поля в схему для
    # последующей обработки алгоритмом
    put_blank()
    screen_text('Chart is handling...', TEXT_X, TEXT_Y)
    pygame.display.update()
    pygame.time.wait(1000)

    scheme = [[None] * HEIGHT for _ in range(WINDOW_WIDTH)]
    put_blank()
    screen_text('Searching the shortest way...', TEXT_X, TEXT_Y)
    pygame.display.update()
    for x in range(0, WINDOW_WIDTH, COMPRESSION):
        for y in range(0, HEIGHT, COMPRESSION):
            check_on_close()
            pix = SCREEN.get_at((x, y))
            if check_deviation(pix):
                scheme[x][y] = True
            else:
                scheme[x][y] = False

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
            check_on_close()
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
        check_on_close()
        CLOCK.tick(FPS)


# Запуск программы
if __name__ == "__main__":
    run()
