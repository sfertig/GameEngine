#launcher for creating projects

import pygame
import json
import os
import sys
import time

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
projectTemplate = data["project_template"]

ENGINE_VERSION = "0.0.1"


class Launcher:
    def __init__(self, _ENGINE_VERSION="0.0.1"):
        self.width = screenData["width"]
        self.height = screenData['height']
        self.title = screenData["title"]
        self.fps = screenData["fps"]
        self.bg_color = screenData["bg color"]
        self.mouse_down = False
        ENGINE_VERSION = _ENGINE_VERSION

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

def save_launcher_data():
        with open(DATA_PATH, 'w') as f:
            json.dump(data, f)


class NewProject:
    def __init__(self, screen):
        self.screen: pygame.Surface = screen
        self.running = True
        self.mouse_down = False

        # name input
        self.inputText = Button(10, 10, 200, 25, [33, 38, 46], None, self.screen)
        self.inputText.add_text("Name:", "white", 20)
        self.input = TextInputBox(10, 40, 200, 25, "black", [100, 100, 100], "gray", 20, self.screen)

        # path input
        self.pathText = Button(10, 100, 200, 25, [33, 38, 46], None, self.screen)
        self.pathText.add_text("Path:", "white", 20)
        self.pathBox = TextInputBox(10, 130, 200, 25, "black", [100, 100, 100], "gray", 20, self.screen)
        self.pathBox.text = "projects/"

        #interactable buttons
        self.cancel = Button(10, 200, 100, 30, [33, 38, 46], [100, 100, 100], self.screen)
        self.cancel.add_text("Cancel", "white", 20)
        self.create = Button(130, 200, 100, 30, [33, 38, 46], [100, 100, 100], self.screen)
        self.create.add_text("Create", "white", 20)

        #run
        self.run()

    def run(self):
        while self.running:
            (self.running)
            self.update()
            if self.running: self.render()

    def update(self):
        click = False
        for event in pygame.event.get():
            if event.type == pygame.QUIT: 
                self.shut_down()
                return
            if event.type == pygame.MOUSEBUTTONDOWN: self.mouse_down = True
            if event.type == pygame.MOUSEBUTTONUP:
                if self.mouse_down: 
                    click = True
                    self.mouse_down = False
            self.input.update(event)
            self.pathBox.update(event)
        self.cancel.update(click)
        self.create.update(click)
        if self.cancel.is_pressed: self.exit_no_new()
        if self.create.is_pressed: self.create_project()

    def render(self):
        #clear
        self.screen.fill(newScreenData["bg"])
        #renders
        self.inputText.render()
        self.input.render()
        self.pathText.render()
        self.pathBox.render()
        self.cancel.render()
        self.create.render()
        #update pygame
        pygame.display.flip()

    def exit_no_new(self):
        self.running = False

    def shut_down(self):
        save_launcher_data()
        pygame.quit()
        sys.exit()

    def create_project(self):
        name = self.format_project_name()
        path = self.gen_project_path()
        print(name, path)
        folder = path + name
        #generate folder with name
        try:
            os.mkdir(folder)
        except:
            self.exit_no_new()
        #populate directory with folders
        try:
            os.mkdir(folder + "/data")
            os.mkdir(folder + "/data/scenes")
            os.mkdir(folder + "/data/scripts")
            os.mkdir(folder + "/assets")
            os.mkdir(folder + "/assets/images")
            os.mkdir(folder + "/assets/sounds")
            os.mkdir(folder + "/assets/fonts")
        except:
            self.exit_no_new()
        #populate details.json
        data: dict = projectTemplate.copy()
        data["project_name"] = name
        data["path"] = folder
        data["engine_version"] = ENGINE_VERSION
        with open(folder + "/details.json", "w") as f:
            json.dump(data, f)

        self.exit_no_new()

    def format_project_name(self):
        n = list(self.input.text)
        name=""
        for i in n:
            if i == " ": name += "-"
            elif i == "/": pass
            elif i == "\\": pass
            elif i == ":": pass
            elif i == "*": pass
            elif i == "?": pass
            elif i == '"': pass
            elif i == "<": pass
            elif i == ">": pass
            elif i == "|": pass
            elif i == ".": pass            
            else: name += i
        return name
    
    def gen_project_path(self):
        #if internal path
        p = self.pathBox.text
        if p == "projects/": return p
        #if external path
        if p[-1] != "/": p += "/"
        return p
        


if __name__ == "__main__":
    pygame.init()
    Launcher()
