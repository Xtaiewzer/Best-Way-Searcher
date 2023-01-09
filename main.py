import sys
import pygame.event
from BFS import *
from consts import *

pygame.init()
screen = pygame.display.set_mode((all_width, win_height))
pygame.display.set_caption('Shortest way searcher')
clock = pygame.time.Clock()
START = pygame.Surface((SCALE * 2, SCALE * 2))
START.fill(GREEN)
END = pygame.Surface((SCALE * 2, SCALE * 2))
END.fill(RED)
SETBOARD = pygame.Surface((set_width, win_height))
SETBOARD.fill(DARK_GRAY)
pygame.display.set_icon(icon_image)
blank = pygame.surface.Surface((350, 175))
blank.fill(GRAY)


def starting(event):
    global start_pos, start_pos_flag

    if event.type == pygame.MOUSEBUTTONDOWN:
        pos = event.pos
        color = screen.get_at(pos)

        if color == YELLOW:
            start_pos = default_start_pos
        else:
            start_pos = pos

        dots_s.play()
        start_pos_flag = True


def ending(event):
    global end_pos, end_pos_flag, default_end_pos

    if event.type == pygame.MOUSEBUTTONDOWN:
        pos = event.pos
        color = screen.get_at(pos)

        if screen.get_at(default_end_pos) == GREEN:
            default_end_pos = default_start_pos

        if color == YELLOW or color == GREEN:
            end_pos = default_end_pos
        else:
            end_pos = pos

        dots_s.play()
        end_pos_flag = True


def drawing(e):
    global mode, delay
    pressed = pygame.mouse.get_pressed()
    pos = pygame.mouse.get_pos()
    # if e.type == pygame.KEYDOWN and (e.mod & pygame.KMOD_CTRL) \
    #         and not len(dots):
    #     change_mode()

    if mode == LINES:
        drawing_lines(e, pos)
    else:
        if pressed[0]:
            pygame.draw.circle(screen, LIGHT_GRAY, pos, SCALE * 2)
            delay += 1
            if delay % 10 == 0:
                eraser_s.play()
                delay = 0


def change_mode():
    global mode
    if mode == LINES:
        mode = ERASER
    else:
        mode = LINES


def drawing_lines(e, p):
    if e.type == pygame.MOUSEBUTTONDOWN:
        button = e.button
        if button == 1:
            dots.append(p)
            pygame.draw.circle(screen, YELLOW, p, HALF_SCALE)
            dotsl_s.play()
        # elif button == 3 and len(dots) >= 2:
        #     link_dots()


def link_dots():
    pygame.draw.lines(screen, YELLOW, False, dots, SCALE * LINES_SCALE)
    dots.clear()
    lines_s.play()


def funcs():
    for e in pygame.event.get():
        buttons(e)
        # use_reload(e)
        pygame.display.update()


def reload():
    global start_pos_flag, start_pos, end_pos, end_pos_flag, \
        default_end_pos, default_start_pos, dots, mode, objects, \
        phase_drawing

    draw_s.stop()
    update_s.play()
    start_pos = None
    phase_drawing = True
    start_pos_flag = False
    end_pos = None
    end_pos_flag = False
    default_start_pos = (SCALE * 2, SCALE * 2)
    default_end_pos = (win_width - SCALE * 2, win_height - SCALE * 2)
    dots = []
    mode = LINES
    objects = []
    run()


# def use_reload(e):
#     if e.type == pygame.KEYDOWN and e.key == pygame.K_1:
#         reload()


def close(e):
    if e.type == pygame.QUIT:
        sys.exit()


def upd_button(event):
    button_surf = pygame.Surface((300, 55))
    text = font.render('UPDATE', True, BLACK)
    center = (700, 250)
    text_rect = text.get_rect(center=center)
    button = button_surf.get_rect(center=center)
    button_surf.fill(WHITE)
    mouse_pos = pygame.mouse.get_pos()
    if button.collidepoint(mouse_pos):
        button_surf.fill(LIGHT_GRAY)
        if event.type == pygame.MOUSEBUTTONDOWN:
            reload()
            button_s.play()
    screen.blit(button_surf, button)
    screen.blit(text, text_rect)


def random_button(event):
    button_surf = pygame.Surface((150, 55))
    text = font.render('RANDOM', True, BLACK)
    center = (800, 50)
    text_rect = text.get_rect(center=center)
    button = button_surf.get_rect(center=center)
    if phase_drawing and end_pos_flag:
        button_surf.fill(WHITE)
        mouse_pos = pygame.mouse.get_pos()
        if button.collidepoint(mouse_pos):
            button_surf.fill(LIGHT_GRAY)
            if event.type == pygame.MOUSEBUTTONDOWN:
                button_s.play()
    else:
        button_surf.fill(LIGHT_GRAY)
    screen.blit(button_surf, button)
    screen.blit(text, text_rect)


def draw_button(event):
    button_surf = pygame.Surface((150, 55))
    text = font.render('DRAW', True, BLACK)
    center = (600, 150)
    text_rect = text.get_rect(center=center)
    button = button_surf.get_rect(center=center)
    if phase_drawing and end_pos_flag and len(dots) > 1\
            and mode == LINES:
        button_surf.fill(WHITE)
        mouse_pos = pygame.mouse.get_pos()
        if button.collidepoint(mouse_pos):
            button_surf.fill(LIGHT_GRAY)
            if event.type == pygame.MOUSEBUTTONDOWN:
                link_dots()
    else:
        button_surf.fill(LIGHT_GRAY)
    screen.blit(button_surf, button)
    screen.blit(text, text_rect)


def test_button(event):
    global phase_drawing
    button_surf = pygame.Surface((150, 55))
    text = font.render('TEST', True, BLACK)
    center = (600, 50)
    text_rect = text.get_rect(center=center)
    button = button_surf.get_rect(center=center)
    if phase_drawing and end_pos_flag:
        button_surf.fill(WHITE)
        mouse_pos = pygame.mouse.get_pos()
        if button.collidepoint(mouse_pos):
            button_surf.fill(LIGHT_GRAY)
            if event.type == pygame.MOUSEBUTTONDOWN:
                phase_drawing = False
                button_s.play()
    else:
        button_surf.fill(LIGHT_GRAY)
    screen.blit(button_surf, button)
    screen.blit(text, text_rect)


def mode_button(event):
    button_surf = pygame.Surface((150, 55))
    text = font.render(mode, True, BLACK)
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
                button_s.play()
    else:
        button_surf.fill(LIGHT_GRAY)
    screen.blit(button_surf, button)
    screen.blit(text, text_rect)


def screen_text(text, c_x, c_y):
    scr_text = font.render(text, True, WHITE)
    scr_text_rect = scr_text.get_rect(center=(c_x, c_y))
    screen.blit(scr_text, scr_text_rect)

def put_blank():
    screen.blit(blank, (525, 300))
    pygame.draw.line(screen, YELLOW, (525, 300), (875, 300), 5)
    pygame.draw.line(screen, YELLOW, (525, 475), (875, 475), 5)


def buttons(e):
    close(e)
    upd_button(e)
    random_button(e)
    draw_button(e)
    test_button(e)
    mode_button(e)


def run():
    global phase_drawing
    screen.fill(LIGHT_GRAY)
    pygame.display.update()
    screen.blit(SETBOARD, (win_width, 0))
    put_blank()
    screen_text('Set start position', text_x, text_y)

    while phase_drawing:
        clock.tick(win_fps)
        # delay += 1
        for e in pygame.event.get():
            buttons(e)
            if allow_x[0] < pygame.mouse.get_pos()[0] < allow_x[1]:
                if not start_pos_flag:
                    starting(e)
                    pygame.draw.rect(screen, YELLOW, (0, 0, SCALE, SCALE))
                elif not end_pos_flag:
                    ending(e)
                    pygame.draw.rect(screen, YELLOW, (0, 0, SCALE, SCALE))
                    put_blank()
                    screen_text('Set finish position', text_x, text_y)
                elif end_pos_flag:
                    put_blank()
                    screen_text('Now, draw the environment', text_x, text_y)
                    drawing(e)
                # if e.type == pygame.KEYDOWN:
                #     if e.key == pygame.K_SPACE and end_pos_flag:
                #         phase_drawing = False
                #     elif e.key == pygame.K_1:
                #         reload()
        pygame.draw.rect(screen, YELLOW, (0, 0, win_width, win_height), SCALE)
        if start_pos is not None:
            screen.blit(START, (start_pos[0] - SCALE, start_pos[1] - SCALE))
        if end_pos is not None:
            screen.blit(END, (end_pos[0] - SCALE, end_pos[1] - SCALE))
        pygame.display.update()

    scheme = ''
    put_blank()
    screen_text('Searching the shortest way...', text_x, text_y)
    pygame.display.update()
    for x in range(0, win_width, COMPRESSION):
        for y in range(0, win_height, COMPRESSION):
            funcs()
            pix = screen.get_at((x, y))
            if pix == YELLOW:
                scheme += '#'
            else:
                scheme += '.'
        scheme += '\n'
    scheme = scheme.split('\n')
    way = SWM(scheme, (start_pos[0] // COMPRESSION, start_pos[1] // COMPRESSION),
              (end_pos[0] // COMPRESSION,
               end_pos[1] // COMPRESSION))
    rect_hero = pygame.Rect(start_pos[0], start_pos[1], SCALE, SCALE)
    pygame.display.update()
    if way[1] < INF:
        put_blank()
        screen_text('Drawing the shortest way...', text_x, text_y)
        pygame.display.update()
        draw_s.play()
        for i in way[0]:
            funcs()
            pygame.draw.rect(screen, ORANGE, rect_hero, SCALE, SCALE)
            pygame.display.update(rect_hero)
            rect_hero.x += i[0] * COMPRESSION
            rect_hero.y += i[1] * COMPRESSION
            pygame.time.wait(SCALE)
        put_blank()
        screen_text('The shortest way has drawn!', text_x, text_y - 20)
        screen_text('Its length is: ' + str(way[1] * COMPRESSION), text_x, text_y + 30)
        draw_s.stop()
        # pygame.time.wait(200)
        success_s.play()
        pygame.display.update()
    else:
        put_blank()
        screen_text('Sorry,', text_x, text_y - 25)
        screen_text('there is no shortest way :(', text_x, text_y + 25)
        error_s.play()
        pygame.display.update()
    while 1:
        funcs()


run()
