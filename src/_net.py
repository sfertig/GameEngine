import pygame

class _global_:
    def __init__(self):
        #screen info
        self.screen: pygame.Surface = None
        self.display = pygame.Surface = None
        self.ScreenDim: tuple = (800, 600)
        self.title: str = "Pygame Window"

        self.FW = 0.0
        self.FH = 0.0

        #basics
        self.clock: pygame.time.Clock = None
        self.bg: str = "black"
        self.dt: float = 0.0

Global = _global_()

