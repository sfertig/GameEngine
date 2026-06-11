import pygame

from .._net import Global
from ..assets.animations import AnimationManager

class _constraints_:
    def __init__(self):
        #define dir <>^_#o
        self.dir_up = 'V^'
        self.dir_down = 'Vv'
        self.dir_left = 'V<'
        self.dir_right = 'V>'
        self.dir_any = 'V#'
        self.dir_none = 'Vo'

Constraints = _constraints_()

class AutoStateManager:
    def __init__(self, manager: AnimationManager = None, obj=None):
        Global.add_object(1, self)
        self.manager = manager
        self.state = None
        self.states: dict[list[str], str] = {}
        self.weights: dict[str, int] = {}
        self.obj = obj

    def set_obj(self, obj):
        self.obj = obj

    def add_state(self, constraints: list[str], state: str, weight=0):
        self.states[tuple(constraints)] = state
        self.weights[state] = weight
    def remove_state(self, state: str):
        self.states.remove(state)
    def set_state(self, name):
        self.current_state = name
        if self.manager is not None and name in self.manager.animations:
            self.manager.play_animation(name)

    def update(self):
        if self.obj is None: return
        if self.manager is None: return
        #eval all states and pick wining num
        states: dict[str, int] ={}
        for constraints, state in self.states.items():
            #velocity tests
            states = self._eval_velocity(constraints, state, states)
            states[state] += self.weights[state]
        #pick the highest state
        self.state = max(states, key=states.get)
        if self.manager is not None and self.state in self.manager.animations:
            self.manager.play_animation(self.state)


    def _eval_velocity(self, conditions, state, _end):
        if len(conditions) == 0: _end[state] += 0
        #up, down, left, right, all, none
        if not hasattr(self.obj, 'vx') and hasattr(self.obj, 'vy'): return _end
        #else do checks
        if 'V^' in conditions and self.obj.vy < 0: _end[state] += 1
        if 'Vv' in conditions and self.obj.vy > 0: _end[state] += 1
        if 'V<' in conditions and self.obj.vx < 0: _end[state] += 1
        if 'V>' in conditions and self.obj.vx > 0: _end[state] += 1
        if 'V#' in conditions and self.obj.vx != 0 and self.obj.vy != 0: _end[state] += 1
        if 'Vo' in conditions and self.obj.vx == 0 and self.obj.vy == 0: _end[state] += 1
        return _end
        

class StateManager:
    def __init__(self, manager: AnimationManager = None, states=[]):
        #Global.add_object(1, self)
        self.manager = manager
        self.state = None
        self.states: list[str] = states

    def add_state(self, constraints: list[str], state: str):
        if state not in self.states:
            self.states.append(state)
        
    def remove_state(self, state):
        if state in self.states:
            self.states.remove(state)

    def set_state(self, name):
        self.current_state = name
        if self.manager is not None and name in self.manager.animations:
            self.manager.play_animation(name)