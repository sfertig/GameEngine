import pygame

class _global_:
    def __init__(self):
        #screen info
        self.screen: pygame.Surface = None
        self.display = pygame.Surface = None
        self.ScreenDim: tuple = (800, 600)
        self.title: str = "Pygame Window"

        self.FW = 0.0 #diference used for resizing
        self.FH = 0.0

        #basics
        self.cam = None
        self.clock: pygame.time.Clock = None
        self.bg: str = "black"
        self.dt: float = 0.0
        self.events: list[pygame.event.Event] = []

        #assets
        self.assets = None

        #objects
        self.objects = {}

        #collisions
        self.collisions = []
        self.all_collision_layers = None

    def add_object(self, layer: str, obj):
        if layer not in self.objects:
            self.objects[layer] = []
        self.objects[layer].append(obj)

    def remove_object(self, layer: str, obj):
        if layer in self.objects:
            self.objects[layer].remove(obj)

Global = _global_()

