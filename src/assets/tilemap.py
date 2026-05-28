import pygame
from .._net import Global
from ..helpers.utils import change_layer

class Tilemap:
    def __init__(self, tileset, show=True, layer=3):
        self.tileset: dict[tuple[int, int], pygame.surface.Surface] = tileset
        self.width = tileset[0, 0].get_width()
        self.height = tileset[0, 0].get_height()
        self.show = show
        self.layer = layer

        self.tiles: dict[tuple[int, int ], tuple[int, int]] = {}

        Global.add_object(layer, self)

    def change_layer(self, new_layer):
        change_layer(self, new_layer, self.layer)
        self.layer = new_layer

    def activateEditor(self):
        _TileMapEditor(600, 800, self).run()

    def render(self):
        if not self.show: return
        for pos, tile in self.tiles.items():
            tx = pos[0] * self.width - Global.cam.x
            ty = pos[1] * self.height - Global.cam.y
            if tx > -self.width and tx < Global.screen.get_width()+self.width and ty > -self.height and ty < Global.screen.get_height()+self.height:
                image = self.tileset[tile]
                Global.screen.blit(image, (tx, ty))

class _TileMapEditor:
    def __init__(self, width, height, map: Tilemap):
        self.width, self.height = width, height
        self.map = map
        self.running = True

        self.win = pygame.Window("Tilemap Editor", (width, height))
        self.screen = self.win.get_surface()

    def run(self):
        while self.running:
            self.update()
            if not self.running: break
            self.render()

    def update(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.win.close()
                self.running = False
            if event.type == pygame.WINDOWCLOSE:
                event.window.destroy()
                self.running = False

    def render(self):
        self.screen.fill("black")
        #render

        #update
        self.win.flip()


            
