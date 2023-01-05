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
SIDE = 1 * SCALE
HALF_SIDE = SIDE // 2
if HALF_SIDE >= 0:
    HALF_SIDE = 1
START = pygame.Surface((SIDE, SIDE))
START.fill(BLUE)
END = pygame.Surface((SIDE, SIDE))
END.fill(RED)
char_image = pygame.image.load('character.png')
start_pos = (0, 0)
start_pos_flag = False
end_pos = (0, 0)
end_pos_flag = False
moving_flag = False
pods = []
lines = True


def starting():
    global start_pos, start_pos_flag
    if event.type == pygame.MOUSEBUTTONDOWN:
        start_pos = event.pos
        start_pos_flag = True


def ending():
    global end_pos, end_pos_flag
    if event.type == pygame.MOUSEBUTTONDOWN:
        end_pos = event.pos
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
            pygame.draw.circle(screen, GREEN, pos, HALF_SIDE)


def drawing_lines(e, p):
    if e.type == pygame.MOUSEBUTTONDOWN:
        button = e.button
        if button == 1:
            pods.append(p)
            pygame.draw.circle(screen, GREEN, p, HALF_SIDE)
        elif button == 3 and len(pods) >= 2:
            pygame.draw.lines(screen, GREEN, False, pods, SIDE)
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
pygame.draw.rect(screen, GREEN, (0, 0, win_width, win_height), SIDE)

while phase_drawing:
    clock.tick(win_fps)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
        if not start_pos_flag:
            starting()
            pygame.draw.rect(screen, GREEN, (0, 0, SIDE, SIDE))
        elif not end_pos_flag:
            ending()
            pygame.draw.rect(screen, GREEN, (0, 0, SIDE, SIDE))
        elif start_pos_flag and end_pos_flag:
            drawing(event)
            # all_sprites = pygame.sprite.Group()
            # char = Character()
            # all_sprites.add(char)
            # all_sprites.draw(screen)
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                phase_drawing = False
    screen.blit(START, start_pos)
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
