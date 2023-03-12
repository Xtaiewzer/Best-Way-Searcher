import pygame
from consts import WHITE_GRAY, BLACK, DARK_WHITE, SCREEN, FONT


class Log:
    def __init__(self, filename, number, text):
        self.filename = filename
        self.number = number
        self.text = FONT.render(text, True, BLACK)
        self.text_rect = self.text.get_rect(center=(750, 35 + 75 * self.number))
        self.surf_rect = pygame.Surface((400, 70))
        self.center = (700, 35 + 75 * self.number)
        self.surf = self.surf_rect.get_rect(center=self.center)
        self.image = pygame.transform.scale(pygame.image.load(self.filename), (100, 50))
        self.image_rect = self.image.get_rect(center=(550, self.center[1]))

    def display(self):
        if self.surf.collidepoint(pygame.mouse.get_pos()):
            self.surf_rect.fill(WHITE_GRAY)
        else:
            self.surf_rect.fill(DARK_WHITE)
        SCREEN.blit(self.surf_rect, self.surf)
        SCREEN.blit(self.image, self.image_rect)
        SCREEN.blit(self.text, self.text_rect)