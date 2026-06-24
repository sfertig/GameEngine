import pygame

class SubScreen:
    def __init__(self, x, y, width, height, gameScreen, bg="black", name="subScreen"):
        self.x, self.y, self.width, self.height = x, y, width, height
        self._screen: pygame.surface.Surface = gameScreen
        self.bg = bg
        self.name = name
        self.screen = pygame.Surface((width, height))

    def get_screen(self): return self.screen

    def update(self): self.screen.fill(self.bg)

    def get_local_mouse(self, offset_x=0, offset_y=0):
        mpos = pygame.mouse.get_pos()
        mpos = (mpos[0]-self.x+offset_x, mpos[1]-self.y+offset_y)
        return mpos

    def render(self):
        self._screen.blit(self.screen, (self.x, self.y))


