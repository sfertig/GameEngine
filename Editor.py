import pygame
import time
import sys
import json

from engineFeatures import *
from runner import Runner

ENGINE_VERSION = "0.0.1"

CREATION_PATH = "data/objectCreation.json"
with open(CREATION_PATH, "r") as f:
    CREATION_DATA = json.load(f)

class Editor:
    def __init__(self, project_path, _ENGINE_VERSION="0.0.0"):
        pygame.init()
        pygame.font.init()
        self.project_path = project_path
        #load project details
        with open(project_path + "/details.json", "r") as f: data = json.load(f)
        config = data["config"]
        self.config = config
        self.data = data
        self.name = data["project_name"]
        self.scenes = data["scenes"].keys()
        ENGINE_VERSION = _ENGINE_VERSION
        self.width = 1280
        self.height = 720
        self.W, self.H = self.width, self.height
        self.fps = 60
        self.bg_color = (0, 0, 0)
        self.DW, self.DH = 0.0, 0.0
        self.display = pygame.display.set_mode((self.W, self.H), flags=pygame.RESIZABLE)
        self.screen = pygame.Surface((self.width, self.height))
        pygame.display.set_caption(f"Editing Project: {self.name}  |  DevPace v{ENGINE_VERSION}")
        self.clock = pygame.time.Clock()
        self.dt = 0.0
        print("Editor v" + ENGINE_VERSION)

        #objects
        self.topBar = topBar(self.screen)
        self.can_run = False

        self.run()

    def reload(self):
        pygame.init()
        pygame.font.init()
        self.display = pygame.display.set_mode((self.W, self.H), flags=pygame.RESIZABLE)
        self.screen = pygame.Surface((self.width, self.height))
        pygame.display.set_caption(f"Editing Project: {self.name}  |  DevPace v{ENGINE_VERSION}")
        self.clock = pygame.time.Clock()
        #objects
        self.topBar = topBar(self.screen)
        self.can_run = False

    def run(self):
        self.running = True
        while self.running:
            self.update()
            if self.can_run:
                time.sleep(0.1)
                Runner(self.project_path, ENGINE_VERSION)
                self.reload()
            self.render()

    def update(self):
        events = pygame.event.get()
        for event in events:
            self.handle_scaling(event)
            if event.type == pygame.QUIT:
                if not self.config["relaunch"]:self.shut_down()
                else: self.running = False
        self.can_run = self.topBar.update(events)

    def render(self):
        self.screen.fill("green") #color to make sure no parts are left
        #clear all screens

        #render objects
        self.topBar.render()

        #update and scale screen
        self.display.blit(pygame.transform.scale(self.screen, self.display.get_size()),(0, 0))
        pygame.display.flip()

    def handle_scaling(self, event):
        if event.type == pygame.VIDEORESIZE:
            self.DW = event.w/self.width
            self.DH = event.h/self.height
            self.display = pygame.display.set_mode((event.w, event.h), flags=pygame.RESIZABLE)
            self.W, self.H = self.display.get_size()

    def shut_down(self):
        pygame.quit()
        sys.exit()

class topBar:
    def __init__(self, screen):
        self.mouse_down = False
        self._screen = screen
        self.screen = SubScreen(0, 0, screen.get_width(), screen.get_height()//15, self._screen)
        self.run = Button(5, 2, 100, 25, [33, 38, 46], [100, 100, 100], self.screen.screen)
        self.run.add_text("Run", "white", 20)

    def update(self, events):
        click = False
        for event in events:
            if event.type == pygame.MOUSEBUTTONDOWN: self.mouse_down = True
            if event.type == pygame.MOUSEBUTTONUP:
                if self.mouse_down: click = True
        self.run.update(click, self.screen.get_local_mouse())
        return self.run.is_pressed

    def render(self):
        self.screen.update()

        self.run.render()

        self.screen.render()
        