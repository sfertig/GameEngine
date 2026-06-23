import pygame

class Button:
    def __init__(self, x, y, width, height, color, hover_color, screen):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.rect = pygame.Rect(x, y, width, height)
        self.color = color
        self.H_color = hover_color

        self.screen = screen

        self.text = ""
        self.T_color = None
        self.size = 0
        self.font = None
        self.text_render = None
        self.text_rect = None

        self.is_hovering = False
        self.is_pressed = False
        #TODO: maby add sygnal: self.pressed_signal = None

    def update(self, click):
        mpos = pygame.mouse.get_pos()
        self.is_hovering = self.rect.collidepoint(mpos)
        if click and self.is_hovering:
            self.hovering = False
            self.is_pressed = True

    def add_text(self, text, color, size):
        self.text = text
        self.T_color = color
        self.size = size
        self.font = pygame.font.SysFont("Arial", size)
        self.text_render = self.font.render(text, True, color)
        #center text
        self.text_rect = self.text_render.get_rect()
        self.text_rect.center = self.rect.center

    def render(self):
        #render rect, then text
        color = self.color
        if self.is_hovering: color = self.H_color
        pygame.draw.rect(self.screen, color, self.rect)
        self.screen.blit(self.text_render, self.text_rect)

