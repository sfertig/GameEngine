import pygame
import os
import sys
import json

from engineFeatures import *

ENGINE_VERSION = "0.0.1"

CREATION_PATH = "data/objectCreation.json"
with open(CREATION_PATH, "r") as f:
    CREATION_DATA = json.load(f)

class Editor:
    def __init__(self, project_path, _ENGINE_VERSION="0.0.0"):
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
        self.fps = 60
        self.bg_color = (0, 0, 0)
        self.DW, self.DH = 0.0, 0.0
        self.display = pygame.display.set_mode((self.width, self.height), flags=pygame.RESIZABLE)
        self.screen = pygame.Surface((self.width, self.height))
        pygame.display.set_caption(f"Editing Project: {self.name}  |  DevPace v{ENGINE_VERSION}")
        self.clock = pygame.time.Clock()
        self.dt = 0.0
        print("Editor v" + ENGINE_VERSION)
        self.run()

    def run(self):
        self.running = True
        while self.running:
            self.update()
            self.render()

    def update(self):
        events = pygame.event.get()
        for event in events:
            self.handle_scaling(event)
            if event.type == pygame.QUIT:
                if not self.config["relaunch"]:self.shut_down()
                else: self.running = False

    def render(self):
        self.screen.fill("green") #color to make sure no parts are left
        #clear all screens

        #render objects

        #update and scale screen
        self.display.blit(pygame.transform.scale(self.screen, self.display.get_size()),(0, 0))
        pygame.display.flip()

    def handle_scaling(self, event):
        if event.type == pygame.VIDEORESIZE:
            self.DW = event.w/self.width
            self.DH = event.h/self.height
            self.display = pygame.display.set_mode((event.w, event.h), flags=pygame.RESIZABLE)

    def shut_down(self):
        pygame.quit()
        sys.exit()
        