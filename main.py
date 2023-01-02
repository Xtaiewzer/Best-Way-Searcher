import pygame

win_width = 1280
win_height = 800
win_fps = 360
pygame.init()
screen = pygame.display.set_mode((win_width, win_height))
clock = pygame.time.Clock()
BLUE = (0, 0, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
char_image = pygame.image.load('character.png')

start_pos = (0, 0)
start_pos_flag = False
end_pos = (0, 0)
end_pos_flag = False
moving_flag = False


def starting():
    global start_pos, start_pos_flag
    if event.type == pygame.MOUSEBUTTONDOWN:
        start_pos = event.pos
        start_pos_flag = True
        pygame.draw.rect(screen, BLUE, (start_pos[0], start_pos[1], 10, 10))


def ending():
    global end_pos, end_pos_flag
    if event.type == pygame.MOUSEBUTTONDOWN:
        end_pos = event.pos
        end_pos_flag = True
        pygame.draw.rect(screen, RED, (end_pos[0], end_pos[1], 10, 10))


def drawing():
    pressed = pygame.mouse.get_pressed()
    pos = pygame.mouse.get_pos()
    if pressed[0]:
        pygame.draw.rect(screen, GREEN, (pos[0], pos[1], 10, 10))


class Character(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = char_image
        self.rect = self.image.get_rect()
        self.rect.center = (start_pos[0], start_pos[1])


pygame.display.set_caption('The Best Project Ever')
running = True
while running:
    clock.tick(win_fps)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if not start_pos_flag:
            starting()
        elif not end_pos_flag:
            ending()
        elif start_pos_flag and end_pos_flag and not moving_flag:
            drawing()
            all_sprites = pygame.sprite.Group()
            char = Character()
            all_sprites.add(char)
            all_sprites.draw(screen)
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                moving_flag = True

    pygame.display.flip()

pygame.quit()
