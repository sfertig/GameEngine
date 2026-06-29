import pygame
import json
import os
import sys

from .gameObjects import *

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
        self.config = config
        self.width = config["screen_width"]
        self.height = config["screen_height"]
        self.fps = config["target_fps"]
        #set up screen
        self.bg_color = config["bg_color"]
        self.DW, self.DH = 0.0, 0.0
        self.display = pygame.display.set_mode((self.width, self.height), flags=pygame.RESIZABLE)
        self.screen = pygame.Surface((self.width, self.height))
        pygame.display.set_caption(data["project_name"])
        #clock
        self.clock = pygame.time.Clock()
        #gameplay info
        self.scene = config["start_scene"]
        if self.scene == "": self.exit_code("02") #if their is no main scene, shut down
        with open(project_path+data["scenes"][self.scene], "r") as f: self.scene_data = json.load(f)
        self.objs = {"-5":[], "-4":[], "-3":[], "-2":[], "-1":[], "0":[], "1":[], "2":[], "3":[], "4":[], "5":[]}
        self.obj_ids = {}
        self.dt = 0.0
        #run
        self.running = True
        self.run()


    def run(self): #test function
        self.new_scene()
        while self.running:
            self.update()
            if self.running:self.render()

    def new_scene(self): #init scene objects
        #reset
        for layer in self.objs: layer = []
        self.obj_ids.clear()
        self.bg_color = self.scene_data["bg"]
        #pass 1: create objects
        for obj in self.scene_data["objects"]: 
            #create the object
            if obj["type"] == "Node": i = Node()
            elif obj["type"] == "Node2D": i = Node2D(*args_from_dict(obj["args"]))
            else: 
                print("invalid object type: " + obj["type"]) #concel error
                continue
            #set layer and append to list
            i.set_layer(obj["layer"])
            self.objs[str(obj["layer"])].append(i)
            self.obj_ids[obj["id"]] = i
        #pass 2: set parents / children
        for obj in self.scene_data["objects"]:
            if len(obj["children"]) == 0: continue
            for child in obj["children"]:
                self.obj_ids[child].parent = self.obj_ids[obj["id"]]
                self.obj_ids[obj["id"]].children.append(self.obj_ids[child])


    def update(self):
        self.dt = self.clock.tick(self.fps)//1000.0
        events = pygame.event.get()
        for event in events:
            self.handle_scaling(event)
            if event.type == pygame.QUIT: 
                if not self.config["relaunch"]:self.shut_down()
                else: self.running = False

        for layer in self.objs:
            for obj in self.objs[layer]:
                obj.update(events, self.dt)

    def render(self):
        self.screen.fill(self.bg_color)

        for layer in self.objs:
            for obj in self.objs[layer]:
                obj.render(self.screen)

        self.display.blit(pygame.transform.scale(self.screen, self.display.get_size()),(0, 0))
        pygame.display.flip()

    def handle_scaling(self, event):
        if event.type == pygame.VIDEORESIZE:
            self.DW = event.w/self.width
            self.DH = event.h/self.height
            self.display = pygame.display.set_mode((event.w, event.h), flags=pygame.RESIZABLE)

    def shut_down(self):
        print("<RUNNER>: EXITING WITH CODE 00")
        pygame.quit()
        sys.exit()

    def exit_code(self, code):
        print(f"<RUNNER>: EXITING WITH CODE {code}")
        pygame.quit()
        sys.exit()

def args_from_dict(d):
    i = []
    for key, value in d.items():
        i.append(value)
    return i
