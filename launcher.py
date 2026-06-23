#launcher for creating projects

import pygame
import json
import os
import sys

from engineFeatures import *

#paths
DATA_PATH = "data/launcher_data.json"

#data
data = {}
with open(DATA_PATH, 'r') as f:
    data = json.load(f)
screenData = data["screenData"]
subData = data["subScreenData"]
projects = data["recentProjects"]
butData = data["buttons"]
newScreenData = data["subScreenData"]["newScreen"]


class Launcher:
    def __init__(self):
        self.width = screenData["width"]
        self.height = screenData['height']
        self.title = screenData["title"]
        self.fps = screenData["fps"]
        self.bg_color = screenData["bg color"]
        self.mouse_down = False

        #screen and clock setup
        self.screen = pygame.display.set_mode((self.width, self.height))
        pygame.display.set_caption(self.title)
        self.clock = pygame.time.Clock()

        #subscreens
        self.topBar = SubScreen(0, 0, self.width, self.height//subData["topBar"]["heightF"], self.screen, subData["topBar"]["bg"], "topBar")
        self.projectWin = SubScreen(0, self.height//subData["topBar"]["heightF"], self.width, self.height-self.height//subData["topBar"]["heightF"], self.screen, subData["projectWin"]["bg"])

        #buttons
        self.create_button = Button(butData["create"]["x"], butData["create"]["y"], butData["create"]["width"], butData["create"]["height"], butData["create"]["color"], butData["create"]["hoverColor"], self.topBar.screen)
        self.create_button.add_text(butData["create"]["text"], butData["create"]["Tcolor"], butData["create"]["size"])
        #run
        self.run()
    

    def run(self):
        while True:
            self.update()
            self.render()

    def update(self):
        click = False
        self.clock.tick(self.fps)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.shut_down()
            if event.type == pygame.MOUSEBUTTONDOWN: self.mouse_down = True
            if event.type == pygame.MOUSEBUTTONUP:
                if self.mouse_down: 
                    click = True
                    self.mouse_down = False

        #button updates
        self.create_button.update(click)
        if self.create_button.is_pressed: NewProject(self.screen)

        


    def render(self):
        self.screen.fill(self.bg_color)
        #update (clear) SubScreens
        self.topBar.update()
        self.projectWin.update()

        #renders

        #buttons
        self.create_button.render()

        self.topBar.render()
        self.projectWin.render()
        #pygame update
        pygame.display.flip()

    def shut_down(self):
        pygame.quit()
        sys.exit()

    def save_launcher_data(self):
        with open(DATA_PATH, 'w') as f:
            json.dump(data, f)

class NewProject:
    def __init__(self, screen):
        self.screen: pygame.Surface = screen
        self.running = True

        #test input
        self.inputText = Button(10, 10, 100, 25, [33, 38, 46], None, self.screen)
        self.inputText.add_text("Name:", "white", 20)
        self.input = TextInputBox(10, 40, 200, 25, "black", "darkgray", "gray", 20, self.screen)
        self.run()

    def run(self):
        while self.running:
            (self.running)
            self.update()
            if self.running: self.render()

    def update(self):

        for event in pygame.event.get():
            if event.type == pygame.QUIT: 
                self.exit_no_save()
                return
            self.input.update(event)

    def render(self):
        #clear
        self.screen.fill(newScreenData["bg"])
        #renders
        self.inputText.render()
        self.input.render()
        #update pygame
        pygame.display.flip()

    def exit_no_save(self):
        self.running = False


if __name__ == "__main__":
    pygame.init()
    Launcher()
