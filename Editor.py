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
        ENGINE_VERSION = _ENGINE_VERSION
        self.width = 1280
        self.height = 720
        self.fps = 60
        self.bg_color = (0, 0, 0)
        self.DW, self.DH = 0.0, 0.0
        self.display = pygame.display.set_mode((self.width, self.height), flags=pygame.RESIZABLE)
        self.screen = pygame.Surface((self.width, self.height))
        pygame.display.set_caption("Editor")
        self.clock = pygame.time.Clock()
        #self.run()
        print("Editor v" + ENGINE_VERSION)