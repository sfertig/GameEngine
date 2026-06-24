import pygame
from .subscreen import SubScreen

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
        self.is_pressed = False
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

class TextInputBox:
    def __init__(self, x, y, width, height, color, active_color, Tcolor, size, screen):
        self.x, self.y, self.width, self.height = x, y, width, height
        self.active_color = active_color
        self.color = color
        self.Tcolor = Tcolor
        self.size = size
        self.screen = screen
        self.text_screen = SubScreen(x, y, width, height, screen, color)
        self.rect = pygame.Rect(x, y, width, height)

        self.active = False
        self.text = ''

    def update(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            self.active = self.rect.collidepoint(event.pos)
            self.text_screen.bg = self.active_color if self.active else self.color
        
        if event.type == pygame.KEYDOWN and self.active:
            if event.key == pygame.K_BACKSPACE:
                self.text = self.text[:-1]
            elif event.key == pygame.K_RETURN or event.key == pygame.K_ESCAPE:
                self.active = False
                self.text_screen.bg = self.color
            else:
                self.text += event.unicode

    def render(self):
        #clear screen (text render)
        self.text_screen.update()

        #render text
        #get and center text
        text_render = pygame.font.SysFont("Arial", self.size).render(self.text, True, self.Tcolor)
        text_rect = text_render.get_rect()
        text_rect.center = self.rect.center
        self.text_screen.screen.blit(text_render, (0, 0))

        #update render
        self.text_screen.render()



