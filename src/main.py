import pygame
import sys
from ._net import Global

class Engine:
    def __init__(self, bg="black", title="Pygame Win", width=800, height=600, RESIZABLE=False, TARGET_FPS=60):
        if RESIZABLE: self._display = pygame.display.set_mode((width, height), flags=pygame.RESIZABLE)
        else: self._display = pygame.display.set_mode((width, height))

        self.screen_dim = (width, height)
        self.RESIZABLE = RESIZABLE

        self.screen = pygame.surface.Surface((width, height))
        self.bg = bg
        self.title = title

        self.clock = pygame.time.Clock()
        self.FPS = TARGET_FPS

        #update global
        Global.display = self._display
        Global.screen = self.screen
        Global.bg = self.bg
        Global.title = self.title
        Global.clock = self.clock

    def Tick(self):
        self.update()
        self.render()

    def update(self):
        #dt
        Global.dt = self.clock.tick(self.FPS) / 1000.0
        #events
        Global.events = pygame.event.get()
        for event in Global.events:
            if event.type == pygame.QUIT:
                self.exit()
            if event.type == pygame.VIDEORESIZE and self.RESIZABLE:
                self._auto_resize(event)
        #updates

    def render(self):
        self.screen.fill(self.bg)
        #render to screen

        #update screen(display)
        self._display.fill(self.bg)
        self._display.blit(self.screen, (0, 0))
        pygame.display.flip()

    def exit(self):
        pygame.quit()
        sys.exit()

    def _auto_resize(self, event):
        w, h = event.size
        self._display = pygame.display.set_mode((w, h), flags=pygame.RESIZABLE)
        self.screen_dim = (w, h)
        Global.FW = w / self.screen_dim[0]
        Global.FH = h / self.screen_dim[1]

    def manual_resize(self, width, height):
        self._display = pygame.display.set_mode((width, height), flags=pygame.RESIZABLE)
        self.screen_dim = (width, height)
        Global.FW = width / self.screen_dim[0]
        Global.FH = height / self.screen_dim[1]


