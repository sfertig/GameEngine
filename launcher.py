#launcher for creating projects

import pygame
import json
import os
import sys
import time

from engineFeatures import *
from runner import Runner
from Editor import Editor


#paths
DATA_PATH = "data/launcher_data.json"

#data
Data = {}
with open(DATA_PATH, 'r') as f:
    Data = json.load(f)
screenData = Data["screenData"]
subData = Data["subScreenData"]
projects = Data["recentProjects"]
butData = Data["buttons"]
newScreenData = Data["subScreenData"]["newScreen"]
projectTemplate = Data["project_template"]

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
        self.projects: list = []

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
        #gen
        self.gen_projects()
        #run
        self.run()
    

    def run(self):
        while True:
            self.update()
            self.render()

    def gen_projects(self):
        self.projects = []
        y = 10
        for p in projects:
            #check if project folder exists
            """if not os.path.exists(p["path"]):
                continue"""
                #create project
            self.projects.append(ProjectDisplay(10, y, 500, 100, self.projectWin.screen, p))
            y += 110

    def update(self):
        click = False
        self.clock.tick(self.fps)
        events = pygame.event.get()
        for event in events:
            if event.type == pygame.QUIT:
                self.shut_down()
            if event.type == pygame.MOUSEBUTTONDOWN: self.mouse_down = True
            if event.type == pygame.MOUSEBUTTONUP:
                if self.mouse_down: 
                    click = True
                    self.mouse_down = False

        #button updates
        self.create_button.update(click)
        if self.create_button.is_pressed: 
            NewProject(self.screen)
            self.gen_projects()

        #update projects
        for p in self.projects:
            p.update(events)
            if p.run_button.is_pressed:
                save_launcher_data()
                pygame.quit()
                time.sleep(0.1)
                Runner(p.p["path"], ENGINE_VERSION)
                print("<LAUNCHER>: EXITTING WITH CODE 01")
                sys.exit()
            elif p.edit_button.is_pressed:
                save_launcher_data()
                pygame.quit()
                time.sleep(0.1)
                Editor(p.p["path"], ENGINE_VERSION)
                sys.exit()
            

    def render(self):
        self.screen.fill(self.bg_color)
        #update (clear) SubScreens
        self.topBar.update()
        self.projectWin.update()

        #renders

        #buttons
        self.create_button.render()
        #render projects
        for p in self.projects:
            p.render()

        self.topBar.render()
        self.projectWin.render()

        #pygame update
        pygame.display.flip()

    def shut_down(self):
        print("<LAUNCHER>: EXITTING WITH CODE 00")
        pygame.quit()
        sys.exit()

def save_launcher_data():
        with open(DATA_PATH, 'w') as f:
            json.dump(Data, f)

class ProjectDisplay:
    def __init__(self, x, y, width, height, screen, project:dict, bg="black"):
        self.x, self.y, self.width, self.height = x, y, width, height
        self.screen = SubScreen(x, y, width, height, screen, bg)
        self.p = project
        self.speed = 100
        self.mouse_down = False
        #info
        self.name = Button(5, 5, width//2, 25, [33, 38, 46], [100, 100, 100], self.screen.screen)
        self.name.add_text(project["name"], "white", 20)
        self.path = Button(5, 35, width//2, 25, [33, 38, 46], [100, 100, 100], self.screen.screen)
        self.path.add_text(project["path"], "white", 20)
        self.version = Button(5, 65, width//2, 25, [33, 38, 46], [100, 100, 100], self.screen.screen)
        self.version.add_text("version: "+ project["version"], "white", 20)
        #buttons: run, edit, remove
        self.run_button = Button(width//2+10, 5, width//2-15, 25, [33, 38, 46], [100, 100, 100], self.screen.screen)
        self.run_button.add_text("Run", "white", 20)
        self.edit_button = Button(width//2+10, 35, width//2-15, 25, [33, 38, 46], [100, 100, 100], self.screen.screen)
        self.edit_button.add_text("Edit", "white", 20)
        self.remove_button = Button(width//2+10, 65, width//2-15, 25, [33, 38, 46], [100, 100, 100], self.screen.screen)
        self.remove_button.add_text("Remove", "white", 20)

    def update(self, events):
        click = False
        for event in events:
            if event.type == pygame.MOUSEWHEEL:
                #scroll down
                if event.y < 0:
                    self.screen.y += self.speed
                    self.screen.screen.get_rect().y += self.speed
                #scroll up
                if event.y > 0:
                    self.screen.y -= self.speed
                    self.screen.screen.get_rect().y -= self.speed
            if event.type == pygame.MOUSEBUTTONDOWN: self.mouse_down = True
            if event.type == pygame.MOUSEBUTTONUP:
                if self.mouse_down: 
                    click = True
                    self.mouse_down = False
        #gen right mpos for each button
        self.run_button.update(click, self.screen.get_local_mouse(0, -20))
        self.edit_button.update(click, self.screen.get_local_mouse(0, -20))
        self.remove_button.update(click, self.screen.get_local_mouse(0, -20))        


    def render(self):
        self.screen.update()

        self.name.render()
        self.path.render()
        self.version.render()

        self.run_button.render()
        self.edit_button.render()
        self.remove_button.render()

        self.screen.render()



class NewProject:
    def __init__(self, screen):
        self.screen: pygame.Surface = screen
        self.running = True
        self.mouse_down = False

        # name input
        self.inputText = Button(10, 10, 200, 25, [33, 38, 46], None, self.screen)
        self.inputText.add_text("Name:", "white", 20)
        self.input = TextInputBox(10, 40, 200, 25, "black", [100, 100, 100], "gray", 20, self.screen)
        self.input.active = True

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

        #add to recent projects
        data: dict = Data["recentTemplate"].copy()
        data["name"] = name
        data["path"] = folder
        data["version"] = ENGINE_VERSION
        projects.append(data)
        save_launcher_data()

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
