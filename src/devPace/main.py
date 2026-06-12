import pygame
import sys
import os
import multiprocessing
from ._net import Global, _global_
from .basics.input import Keys
from .physics.collisions import CollisionRect
from .assets.cache import Assets

from .GlobalDebugger import GlobalDebugger


MIN_LAYER = -5
MAX_LAYER = 10
ALL_COLLISION_LAYERS = [-5, -4, -3, -2, -1, 0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10]

class Engine:
    def __init__(self, bg="black", title="Pygame Win", width=800, height=600, EXPERIMENTAL_RESIZABLE=False, TARGET_FPS=60, EXPERIMENTAL_DEBUG=False):
        if EXPERIMENTAL_RESIZABLE: self._display = pygame.display.set_mode((width, height), flags=pygame.RESIZABLE)
        else: self._display = pygame.display.set_mode((width, height))
        pygame.display.set_caption(title)

        if EXPERIMENTAL_DEBUG:
            print("Starting GlobalDebugger...")
            self.log_queue = multiprocessing.Queue()
            self.debug_prossess = multiprocessing.Process(target=GlobalDebugger, args=(self.log_queue,)).start()


        self.screen_dim = (width, height)
        self.width = width
        self.height = height
        self.RESIZABLE = EXPERIMENTAL_RESIZABLE

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
        Global.assets = Assets
        Global.all_collision_layers = ALL_COLLISION_LAYERS

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

        #keys
        Keys.update()

        #cam
        Global.cam.update()
        #objects
        layer=MIN_LAYER
        while layer<=MAX_LAYER:
            if layer in Global.objects:
                i = Global.objects[layer]
                for obj in i:
                    try:
                        obj.update()
                    except AttributeError:
                        pass
            layer+=1
        

    def render(self):
        self.screen.fill(self.bg)
        #render to screen
        layer=MIN_LAYER
        while layer<=MAX_LAYER:
            if layer in Global.objects:
                i = Global.objects[layer]
                for obj in i:
                    try:
                        obj.render()
                    except AttributeError:
                        pass
            layer+=1
        

        #update screen(display)
        self._display.fill(self.bg)
        self._display.blit(pygame.transform.scale(self.screen, self.screen_dim), (0, 0))
        pygame.display.flip()

    def exit(self):
        os.system("cls")
        pygame.quit()
        sys.exit()

    def _auto_resize(self, event):
        w, h = event.size
        self._display = pygame.display.set_mode((w, h), flags=pygame.RESIZABLE)
        self.screen_dim = (w, h)
        Global.FW = w / self.screen_dim[0]
        Global.FH = h / self.screen_dim[1]
    def all_colision_layers(self):
        return ALL_COLLISION_LAYERS

    def manual_resize(self, width, height):
        self._display = pygame.display.set_mode((width, height), flags=pygame.RESIZABLE)
        self.screen_dim = (width, height)
        Global.FW = width / self.screen_dim[0]
        Global.FH = height / self.screen_dim[1]

    def create_aroundScreen_bounds(self):
        CollisionRect(0, -5, self.screen_dim[0], 5, ALL_COLLISION_LAYERS)
        CollisionRect(-5, 0, 5, self.screen_dim[1], ALL_COLLISION_LAYERS)
        CollisionRect(self.screen_dim[0], 0, 5, self.screen_dim[1], ALL_COLLISION_LAYERS)
        CollisionRect(0, self.screen_dim[1], self.screen_dim[0], 5, ALL_COLLISION_LAYERS)

    def _func_get_global_(self) -> _global_:
        print("<Engine> Global accsesed")
        return Global
    
    def get_current_fps(self):
        return self.clock.get_fps()
    
    def change_title(self, title):
        Global.title = title
        pygame.display.set_caption(title)
        self.title = title

    #scene logic
    def new_scene(self, name, scene):
        Global.scenes[name] = scene
    def change_scene(self, name, resetCam=True, resetObjects=True):
        if resetCam: Global.cam = None
        if resetObjects: 
            Global.tilemaps = {}
            Global.objects = {}
        if name in Global.scenes:
            if Global.current_scene is not None:
                Global.last_scene = Global.current_scene
                Global.current_scene.on_end()
            Global.current_scene = Global.scenes[name]
            Global.current_scene.on_end()
            Global.current_scene.on_start()
            Global.current_scene.run()

    def reload_scene(self, resetCam=True, resetObjects=True, end=True, start=True):
        if Global.current_scene is not None:
            if resetCam: 
                Global.tilemaps = {}
                Global.cam = None
            if resetObjects: Global.objects = {}
            if end: Global.current_scene.on_end()
            if start: Global.current_scene.on_start()
            Global.current_scene.run()

    def back_scene(self):
        if Global.last_scene is not None:
            self.change_scene(Global.last_scene)

    def remove_scene(self, name):
        if name in Global.scenes:
            del Global.scenes[name]
class Scene:
    def __init__(self):
        pass
    def run(self):
        pass
    def on_start(self):
        pass
    def on_end(self):
        pass
