#launcher for creating projects

import pygame
import json
import os
import sys

#paths
DATA_PATH = "data/launcher_data.json"

#data
data = {}
with open(DATA_PATH, 'r') as f:
    data = json.load(f)
screenData = data["screenData"]


class Launcher:
    def __init__(self):
        self.width = screenData["width"]
        self.height = screenData['height']
        self.title = screenData["title"]
        self.fps = screenData["fps"]
        self.bg_color = screenData["bg color"]

        #screen and clock setup
        self.screen = pygame.display.set_mode((self.width, self.height))
        pygame.display.set_caption(self.title)
        self.clock = pygame.time.Clock()

        #run
        self.run()
    

    def run(self):
        while True:
            self.update()
            self.render()

    def update(self):
        self.clock.tick(self.fps)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.shut_down()

    def render(self):
        self.screen.fill(self.bg_color)

        #renders

        #pygame update
        pygame.display.flip()

    def shut_down(self):
        pygame.quit()
        sys.exit()

    def save_launcher_data(self):
        with open(DATA_PATH, 'w') as f:
            json.dump(data, f)

if __name__ == "__main__":
    Launcher()
