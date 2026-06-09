import pygame

from .._net import Global
from ..assets.animations import AnimationManager

class _constraints_:
    def __init__(self):
        #define dir <>^_#o
        self.dir_up = '^'
        self.dir_down = 'v'
        self.dir_left = '<'
        self.dir_right = '>'
        self.dir_any = '#'
        self.dir_none = 'o'

Constraints = _constraints_()

class StateManager:
    def __init__(self):
        Global.add_object(0, self)
        self.current_state = None
        self.states: dict[list[str], str] = {}

    def new_state(self, name, constraints):
        self.states[constraints] = name
    def remove_state(self, name):
        self.states.pop(name)