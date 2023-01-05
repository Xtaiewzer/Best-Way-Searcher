import pygame
import sys

SCALE = 5
win_width = 100 * SCALE
win_height = 100 * SCALE
win_fps = 60
pygame.init()
screen = pygame.display.set_mode((win_width, win_height))
clock = pygame.time.Clock()
BLUE = (0, 140, 240, 255)
RED = (255, 0, 0, 255)
GREEN = (0, 255, 0, 255)
GRAY = (70, 70, 70, 255)
HALF_SCALE = SCALE // 2
if HALF_SCALE >= 0:
    HALF_SCALE = 1
START = pygame.Surface((SCALE, SCALE))
START.fill(BLUE)
END = pygame.Surface((SCALE, SCALE))
END.fill(RED)
char_image = pygame.image.load('character.png')
start_pos = None
start_pos_flag = False
end_pos = None
end_pos_flag = False
moving_flag = False
default_start_pos = (SCALE, SCALE)
default_end_pos = (win_width - SCALE * 2, win_height - SCALE * 2)
pods = []
lines = True


def starting():
    global start_pos, start_pos_flag
    if event.type == pygame.MOUSEBUTTONDOWN:
        pos = event.pos
        color = screen.get_at(pos)
        if color == GREEN:
            start_pos = default_start_pos
        else:
            start_pos = pos

        start_pos_flag = True


def ending():
    global end_pos, end_pos_flag, default_end_pos
    if event.type == pygame.MOUSEBUTTONDOWN:
        pos = event.pos
        color = screen.get_at(pos)
        if screen.get_at(default_end_pos) == BLUE:
            default_end_pos = default_start_pos
        if color == GREEN or color == BLUE:
            end_pos = default_end_pos
        else:
            end_pos = pos
        end_pos_flag = True


def drawing(e):
    global lines
    pressed = pygame.mouse.get_pressed()
    pos = pygame.mouse.get_pos()
    if e.type == pygame.KEYDOWN and (e.mod & pygame.KMOD_CTRL):
        lines = not lines
    if lines:
        drawing_lines(e, pos)
    else:
        if pressed[0]:
            pygame.draw.circle(screen, GRAY, pos, SCALE * 2)


def drawing_lines(e, p):
    if e.type == pygame.MOUSEBUTTONDOWN:
        button = e.button
        if button == 1:
            pods.append(p)
            pygame.draw.circle(screen, GREEN, p, HALF_SCALE)
        elif button == 3 and len(pods) >= 2:
            pygame.draw.lines(screen, GREEN, False, pods, SCALE)
            pods.clear()


class Character(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = char_image
        self.rect = self.image.get_rect()
        self.rect.center = (start_pos[0], start_pos[1])


pygame.display.set_caption('The Best Project Ever')
screen.fill(GRAY)
pygame.display.update()
phase_drawing = True
pygame.draw.rect(screen, GREEN, (0, 0, win_width, win_height), SCALE)

while phase_drawing:
    clock.tick(win_fps)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
        if not start_pos_flag:
            starting()
            pygame.draw.rect(screen, GREEN, (0, 0, SCALE, SCALE))
        elif not end_pos_flag:
            ending()
            pygame.draw.rect(screen, GREEN, (0, 0, SCALE, SCALE))
        elif start_pos_flag and end_pos_flag:
            drawing(event)
            # all_sprites = pygame.sprite.Group()
            # char = Character()
            # all_sprites.add(char)
            # all_sprites.draw(screen)
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                phase_drawing = False
    pygame.draw.rect(screen, GREEN, (0, 0, win_width, win_height), SCALE)
    if start_pos is not None:
        screen.blit(START, start_pos)
    if end_pos is not None:
        screen.blit(END, end_pos)
    pygame.display.flip()

scheme = ''
for x in range(0, win_width, SCALE):
    for y in range(0, win_height, SCALE):
        pix = screen.get_at((x, y))
        if pix == GREEN:
            scheme += '#'
        elif pix == BLUE:
            scheme += 'S'
        elif pix == RED:
            scheme += 'T'
        else:
            scheme += '.'
    scheme += '\n'
print(scheme)
