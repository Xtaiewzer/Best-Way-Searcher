import pygame

win_width = 1280
win_height = 800
win_fps = 30
pygame.init()
screen = pygame.display.set_mode((win_width, win_height))
clock = pygame.time.Clock()
BLUE = (0, 0, 255)
RED = (255, 0, 0)

start_pos = (0, 0)
start_pos_flag = False
end_pos = (0, 0)
end_pos_flag = False


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

    pygame.display.flip()

pygame.quit()
