import pygame

class SubScreen:
    def __init__(self, x, y, width, height, gameScreen, bg="black", name="subScreen", cam=None):
        self.x, self.y, self.width, self.height = x, y, width, height
        self._screen: pygame.surface.Surface = gameScreen
        self.bg = bg
        self.name = name
        self.screen = pygame.Surface((width, height))

        self.cam = cam

    def get_screen(self): return self.screen

    def update(self): self.screen.fill(self.bg)

    def render(self):
        self._screen.blit(self.screen, (self.x, self.y))


