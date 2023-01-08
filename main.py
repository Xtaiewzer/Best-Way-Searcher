import sys
from BFS import *
from consts import *

pygame.init()
screen = pygame.display.set_mode((all_width, win_height))
clock = pygame.time.Clock()
START = pygame.Surface((SCALE * 2, SCALE * 2))
START.fill(GREEN)
END = pygame.Surface((SCALE * 2, SCALE * 2))
END.fill(RED)
SETBOARD = pygame.Surface((set_width, win_height))
SETBOARD.fill(DARK_GRAY)
pygame.display.set_icon(icon_image)


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
    global lines, delay
    pressed = pygame.mouse.get_pressed()
    pos = pygame.mouse.get_pos()
    if e.type == pygame.KEYDOWN and (e.mod & pygame.KMOD_CTRL) \
            and not len(dots):
        lines = not lines

    if lines:
        drawing_lines(e, pos)
    else:
        if pressed[0]:
            pygame.draw.circle(screen, GRAY, pos, SCALE * 2)
            if delay % 20 == 0:
                eraser_s.play()
                delay = 0



def drawing_lines(e, p):
    if e.type == pygame.MOUSEBUTTONDOWN:
        button = e.button
        if button == 1:
            dots.append(p)
            pygame.draw.circle(screen, YELLOW, p, HALF_SCALE)
            dotsl_s.play()
        elif button == 3 and len(dots) >= 2:
            link_dots()
            lines_s.play()

def link_dots():
    pygame.draw.lines(screen, YELLOW, False, dots, SCALE * LINES_SCALE)
    dots.clear()

def funcs():
    for e in pygame.event.get():
        close(e)
        upd_button(e)
        use_reload(e)
        pygame.display.update()

def reload():
    global start_pos_flag, start_pos, end_pos, end_pos_flag, \
        default_end_pos, default_start_pos, dots, lines, objects

    draw_s.stop()
    update_s.play()
    start_pos = None
    start_pos_flag = False
    end_pos = None
    end_pos_flag = False
    default_start_pos = (SCALE * 2, SCALE * 2)
    default_end_pos = (win_width - SCALE * 2, win_height - SCALE * 2)
    dots = []
    lines = True
    objects = []
    run()


def use_reload(e):
    if e.type == pygame.KEYDOWN and e.key == pygame.K_1:
        reload()


def close(e):
    if e.type == pygame.QUIT:
        sys.exit()


def upd_button(event):
    button_surf = pygame.Surface((150, 55))
    text = font.render('UPDATE', True, BLACK)
    text_rect = text.get_rect(center=(700, 50))
    button = button_surf.get_rect(center=(700, 50))
    button_surf.fill(WHITE)
    mouse_pos = pygame.mouse.get_pos()
    if button.collidepoint(mouse_pos):
        button_surf.fill(GRAY)
        if event.type == pygame.MOUSEBUTTONDOWN:
            update_s.play()
            reload()
    screen.blit(button_surf, button)
    screen.blit(text, text_rect)


def screen_text(text, c_x, c_y):
    r_surf = pygame.Surface((400, 30))
    r = r_surf.get_rect(center=(c_x, c_y))
    r_surf.fill(DARK_GRAY)
    scr_text = font.render(text, True, WHITE)
    scr_text_rect = scr_text.get_rect(center=(c_x, c_y))
    screen.blit(r_surf, r)
    screen.blit(scr_text, scr_text_rect)


def run():
    global delay
    pygame.display.set_caption('Shortest way searcher')
    screen.fill(GRAY)
    pygame.display.update()
    phase_drawing = True
    screen.blit(SETBOARD, (win_width, 0))
    screen_text('Set start position', 700, 300)

    while phase_drawing:
        clock.tick(win_fps)
        delay += 1
        for e in pygame.event.get():
            close(e)
            upd_button(e)
            if allow_x[0] < pygame.mouse.get_pos()[0] < allow_x[1]:
                if not start_pos_flag:
                    starting(e)
                    pygame.draw.rect(screen, YELLOW, (0, 0, SCALE, SCALE))
                elif not end_pos_flag:
                    ending(e)
                    pygame.draw.rect(screen, YELLOW, (0, 0, SCALE, SCALE))
                    screen_text('Set finish position', 700, 300)
                elif end_pos_flag:
                    screen_text('Now, draw the environment', 700, 300)
                    drawing(e)
                if e.type == pygame.KEYDOWN:
                    if e.key == pygame.K_SPACE and end_pos_flag:
                        phase_drawing = False
                    elif e.key == pygame.K_1:
                        reload()
        pygame.draw.rect(screen, YELLOW, (0, 0, win_width, win_height), SCALE)
        if start_pos is not None:
            screen.blit(START, (start_pos[0] - SCALE, start_pos[1] - SCALE))
        if end_pos is not None:
            screen.blit(END, (end_pos[0] - SCALE, end_pos[1] - SCALE))
        pygame.display.update()

    scheme = ''
    screen_text('Searching the shortest way...', 700, 300)
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
    screen_text('Drawing the shortest way...', 700, 300)
    pygame.display.update()
    if way[1] < INF:
        draw_s.play()
        for i in way[0]:
            for e in pygame.event.get():
                close(e)
                upd_button(e)
                use_reload(e)
            pygame.draw.rect(screen, ORANGE, rect_hero, SCALE, SCALE)
            pygame.display.update(rect_hero)
            rect_hero.x += i[0] * COMPRESSION
            rect_hero.y += i[1] * COMPRESSION
            pygame.time.wait(SCALE)
        screen_text('The shortest way has drawn!', 700, 300)
        screen_text('Its length is: ' + str(way[1] * COMPRESSION), 700, 350)
        success_s.play()
        pygame.display.update()
        draw_s.stop()
    else:
        screen_text('Sorry,', 700, 300)
        screen_text('there is no shortest way :(', 700, 350)
        error_s.play()
    while 1:
        funcs()


run()
