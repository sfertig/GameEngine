import pygame
import json
import os
import sys

ENGINE_VERSION = "0.0.1"

data: dict = {}
config: dict = {}

class Runner:
    def __init__(self, project_path, _ENGINE_VERSION="0.0.0"):
        self.project_path = project_path
        ENGINE_VERSION = _ENGINE_VERSION
        #get screen values
        with open(project_path + "/details.json", "r") as f: data = json.load(f)
        config = data["config"]
        self.width = config["screen_width"]
        self.height = config["screen_height"]
        self.fps = config["target_fps"]
        #set up screen
        self.display = pygame.display.set_mode((self.width, self.height))
        self.screen = pygame.Surface((self.width, self.height))
        pygame.display.set_caption(data["project_name"])
        #clock
        self.clock = pygame.time.Clock()
        #run
        self.run()


    def run(self): #test function
        while True:
            self.clock.tick(self.fps)
            self.screen.fill((0, 0, 0))
            self.display.blit(self.screen, (0, 0))
            pygame.display.update()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
