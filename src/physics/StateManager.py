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

class AutoStateManager:
    def __init__(self, manager: AnimationManager = None, obj=None):
        Global.add_object(1, self)
        self.manager = manager
        self.state = None
        self.states: dict[list[str], str] = {}
        self.obj = obj

    def add_state(self, constraints: list[str], state: str):
        self.states[tuple(constraints)] = state
    def remove_state(self, state: str):
        self.states.remove(state)
    def set_state(self, name):
        self.current_state = name
        if self.manager is not None and name in self.manager.animations:
            self.manager.play_animation(name)