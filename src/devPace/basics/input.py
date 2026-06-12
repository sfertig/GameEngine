import pygame

from .._net import Global


class _keys:
    def __init__(self):

        #alphabet
        self.a = pygame.K_a
        self.b = pygame.K_b
        self.c = pygame.K_c
        self.d = pygame.K_d
        self.e = pygame.K_e
        self.f = pygame.K_f
        self.g = pygame.K_g
        self.h = pygame.K_h
        self.i = pygame.K_i
        self.j = pygame.K_j
        self.k = pygame.K_k
        self.l = pygame.K_l
        self.m = pygame.K_m
        self.n = pygame.K_n
        self.o = pygame.K_o
        self.p = pygame.K_p
        self.q = pygame.K_q
        self.r = pygame.K_r
        self.s = pygame.K_s
        self.t = pygame.K_t
        self.u = pygame.K_u
        self.v = pygame.K_v
        self.w = pygame.K_w
        self.x = pygame.K_x
        self.y = pygame.K_y
        self.z = pygame.K_z

        #numbers
        self.n0 = pygame.K_0
        self.n1 = pygame.K_1
        self.n2 = pygame.K_2
        self.n3 = pygame.K_3
        self.n4 = pygame.K_4
        self.n5 = pygame.K_5
        self.n6 = pygame.K_6
        self.n7 = pygame.K_7
        self.n8 = pygame.K_8
        self.n9 = pygame.K_9

        #special keys
        self.enter = pygame.K_RETURN
        self.escape = pygame.K_ESCAPE
        self.space = pygame.K_SPACE
        self.backspace = pygame.K_BACKSPACE
        self.tab = pygame.K_TAB
        self.shift = pygame.K_LSHIFT

        #arrow keys
        self.up = pygame.K_UP
        self.down = pygame.K_DOWN
        self.left = pygame.K_LEFT
        self.right = pygame.K_RIGHT


        #mouse
        self.mouse_x, self.mouse_y = 0, 0

    def is_pressed(self, keys): 
        if type(keys) != list: keys = [keys]
        if Global.events is None: return False
        for event in Global.events:
            if event.type == pygame.KEYDOWN:
                if event.key in keys: return True
        return False

    def is_held(self, key):
        keys = pygame.key.get_pressed()
        return keys[key]

    def update(self): self.mouse_x, self.mouse_y = pygame.mouse.get_pos()

Keys = _keys()

class FastMovement:
    def __init__(self, obj, speed, reset_x=True, reset_y=True, WSAD=True, ARROWS=True, move_x=True, move_y=True, jump=False, jumpForce=0.0, jumpKeys=[Keys.space]):
        self.obj = obj
        self.speed = speed
        self.reset_x = reset_x
        self.reset_y = reset_y

        self.jump = jump
        self.jumpForce = jumpForce
        self.jumpKeys = jumpKeys

        self.WSAD = WSAD
        self.ARROWS = ARROWS

        self.move_x = move_x
        self.move_y = move_y

        if hasattr(self.obj, 'vx') and hasattr(self.obj, 'vy'): self.safe = True
        else: self.safe = False
        if hasattr(self.obj, 'is_on_floor'): self.safeJump = True
        else: self.safeJump = False

        Global.add_object(0, self)

    def update(self):
        if not self.safe: return

        if self.reset_x: self.obj.vx = 0.0
        if self.reset_y: self.obj.vy = 0.0

        if self.WSAD:
            if self.move_x:
                if Keys.is_held(Keys.a): self.obj.vx = -self.speed
                if Keys.is_held(Keys.d): self.obj.vx = self.speed
            if self.move_y:
                if Keys.is_held(Keys.w): self.obj.vy = -self.speed
                if Keys.is_held(Keys.s): self.obj.vy = self.speed

            if self.safeJump and self.jump:
                if Keys.is_pressed(self.jumpKeys) and self.obj.is_on_floor: 
                    self.obj.vy = -self.jumpForce

        if self.ARROWS:
            if self.move_x:
                if Keys.is_held(Keys.left): self.obj.vx = -self.speed
                if Keys.is_held(Keys.right): self.obj.vx = self.speed
            if self.move_y:
                if Keys.is_held(Keys.up): self.obj.vy = -self.speed
                if Keys.is_held(Keys.down): self.obj.vy = self.speed

            if self.safeJump and self.jump:
                if Keys.is_pressed(self.jumpKeys) and self.obj.is_on_floor: self.obj.vy = -self.jumpForce

