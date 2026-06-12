import pygame
from .._net import Global

class Timer:
    def __init__(self, duration, loops=False):
        self.duration = duration  # Time in seconds (e.g., 2.0 for two seconds)
        self.loops = loops
        self.time_elapsed = 0.0
        self.active = True
        self.triggered = False

        Global.add_object(0, self)

    def update(self):
        if not self.active:
            return

        self.triggered = False
        self.time_elapsed += Global.dt

        if self.time_elapsed >= self.duration:
            self.triggered = True
            if self.loops:
                self.time_elapsed = 0.0  # Reset and loop
            else:
                self.active = False      # Stop running

    def start(self):
        self.time_elapsed = 0.0
        self.active = True
        self.triggered = False

    def stop(self):
        self.active = False

    def is_done(self):
        return not self.active