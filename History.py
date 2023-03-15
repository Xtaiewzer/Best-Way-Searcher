import pygame
from consts import WHITE_GRAY, BLACK, DARK_WHITE, GRAY, SCREEN, FONT


class Log:
    def __init__(self, filename, number, text):
        self.filename = filename
        self.number = number
        if len(text) > 9:
            self.text = FONT.render(text[0:8] + '...', True, BLACK)
        else:
            self.text = FONT.render(text, True, BLACK)
        self.text_rect = self.text.get_rect(center=(750, 35 + 75 * self.number))
        self.surf_rect = pygame.Surface((400, 70))
        self.center = (700, 35 + 75 * self.number)
        self.surf = self.surf_rect.get_rect(center=self.center)
        self.image = pygame.transform.scale(pygame.image.load(self.filename), (100, 50))
        self.image_rect = self.image.get_rect(center=(550, self.center[1]))
        self.clicked = False

        self.trash_surf = pygame.image.load('images/trashbox.png')
        self.trash = pygame.transform.scale(self.trash_surf, (65, 65))
        self.trash_rect = self.trash.get_rect(center=(850, 35 + 75 * self.number))
        self.del_click = False
        self.onbutton = False

        self.preview = pygame.transform.scale(pygame.image.load(self.filename), (500, 500))
        self.preview_rect = self.preview.get_rect(center=(250, 250))

    def display(self, event):
        if self.surf.collidepoint(pygame.mouse.get_pos()):
            self.surf_rect.fill(WHITE_GRAY)
            if event.type == pygame.MOUSEBUTTONDOWN and not self.trash_rect.collidepoint(pygame.mouse.get_pos()):
                self.clicked = True

            if self.image_rect.collidepoint(pygame.mouse.get_pos()):
                SCREEN.blit(self.preview, self.preview_rect)

            if not (self.image_rect.collidepoint(pygame.mouse.get_pos())):
                surf = pygame.Surface((500, 500))
                surf.fill(GRAY)
                surf_rect = surf.get_rect(center=(250, 250))
                SCREEN.blit(surf, surf_rect)
            if self.trash_rect.collidepoint(pygame.mouse.get_pos()):
                if event.type == pygame.MOUSEBUTTONDOWN:
                    self.del_click = True
        else:
            self.surf_rect.fill(DARK_WHITE)
        SCREEN.blit(self.surf_rect, self.surf)
        SCREEN.blit(self.image, self.image_rect)
        SCREEN.blit(self.text, self.text_rect)
        SCREEN.blit(self.trash, self.trash_rect)
