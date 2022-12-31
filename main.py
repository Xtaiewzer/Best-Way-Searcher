import pygame

win_width = 1280
win_height = 800
win_fps = 30
pygame.init()
screen = pygame.display.set_mode((win_width, win_height))
clock = pygame.time.Clock()

running = True
while running:
    clock.tick(win_fps)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    pygame.display.flip()

pygame.quit()