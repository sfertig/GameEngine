import pygame

from ..basics.camera import Camera
from ..basics.input import Keys
from .._net import Global

class _TileMapEditor:
    def __init__(self, x, y, width, height, map, exit_key):
        self.width, self.height = width, height
        self.map = map
        self.running = True
        self.exit_key = exit_key

        self.mode = "painting"
        self.cooldown = False

        self.cam = Camera(-width/2, -height/2)
        self.cam_speed = 275

        self.win = pygame.Window("Tilemap Editor", (width, height), (x, y))
        self.screen = self.win.get_surface()

        self.clock = pygame.time.Clock()
        self.FPS = 60
        self.dt = 0.0

        self.selected_tile = (0, 0)
        #get the din of the original tileset
        self.setDim = Global.assets._tileset_cache_data[self.map.name]
        self.setDim = (self.setDim[0]-1, self.setDim[1]-1)

    def run(self):
        pygame.mouse.set_visible(False)
        while self.running:
            self.update()
            if not self.running: break
            self.render()
        pygame.mouse.set_visible(True)

    def update(self):
        #if need to exit
        if Keys.is_pressed(self.exit_key) and self.cooldown:
            self.running = False
            return
        else: self.cooldown = True

        #win updates
        self.dt = self.clock.tick(self.FPS) / 1000
        Global.events = pygame.event.get()
        for event in Global.events:
            if event.type == pygame.QUIT:
                self.win.close()
                self.running = False
            if event.type == pygame.WINDOWCLOSE:
                try:
                    event.window.destroy()
                    self.running = False
                except:
                    pass
        #other updates
        if self.mode == "painting":
            self.cam_movement()
            self.tile_placing()
            self.basic_tile_selecting()
        elif self.mode == "picking":
            pass


    def render(self):
        self.screen.fill("black")
        #render
        if self.mode == "painting":
            self.render_tiles()
        elif self.mode == "picking":
            self.render_picking()
        


        #update
        self.win.flip()

    def render_picking(self):
        #draw square around mouse
        mpos = pygame.mouse.get_pos()
        tpos = point_world_to_tilemap(mpos[0]+self.cam.x, mpos[1]+self.cam.y, self.map.width, self.map.height)
        pygame.draw.rect(self.screen, "white", (tpos[0]*self.map.width-self.cam.x, tpos[1]*self.map.height-self.cam.y, self.map.width, self.map.height), 1)

    def render_tiles(self):
        #draw orgin
        point = (0-self.cam.x, 0-self.cam.y)
        if point[0] > 0 and point[0] < self.width and point[1] > 0 and point[1] < self.height:
            pygame.draw.circle(self.screen, "white", point, 5)

        #render tiles
        for pos, tile in self.map.tiles.items():
            tx = pos[0] * self.map.width - self.cam.x
            ty = pos[1] * self.map.height - self.cam.y
            if tx > -self.map.width and tx < self.width+self.map.width and ty > -self.map.height and ty < self.height+self.map.height:
                image = self.map.tileset[tile]
                self.screen.blit(image, (tx, ty))

        #draw box around mouse and selected tile
        mpos = pygame.mouse.get_pos()
        tpos = point_world_to_tilemap(mpos[0]+self.cam.x, mpos[1]+self.cam.y, self.map.width, self.map.height)
        self.screen.blit(self.map.tileset[self.selected_tile], (tpos[0]*self.map.width-self.cam.x, tpos[1]*self.map.height-self.cam.y))
        pygame.draw.rect(self.screen, "white", (tpos[0]*self.map.width-self.cam.x, tpos[1]*self.map.height-self.cam.y, self.map.width, self.map.height), 1)

    def tile_placing(self):
        #placing tile logic
        if pygame.mouse.get_pressed()[0]:
            mpos = pygame.mouse.get_pos()
            tpos = point_world_to_tilemap(mpos[0]+self.cam.x, mpos[1]+self.cam.y, self.map.width, self.map.height)
            self.map.tiles[tpos] = self.selected_tile
        #erasing logic
        if pygame.mouse.get_pressed()[2]:
            mpos = pygame.mouse.get_pos()
            tpos = point_world_to_tilemap(mpos[0]+self.cam.x, mpos[1]+self.cam.y, self.map.width, self.map.height)
            self.map.tiles.pop(tpos, None)
    def basic_tile_selecting(self):
        #changing tile logic
        if Keys.is_pressed(Keys.up): self.selected_tile = (self.selected_tile[0], self.selected_tile[1]-1)
        if Keys.is_pressed(Keys.down): self.selected_tile = (self.selected_tile[0], self.selected_tile[1]+1)
        if Keys.is_pressed(Keys.left): self.selected_tile = (self.selected_tile[0]-1, self.selected_tile[1])
        if Keys.is_pressed(Keys.right): self.selected_tile = (self.selected_tile[0]+1, self.selected_tile[1])
        #wrap around
        if self.selected_tile[0]<0: self.selected_tile = (self.setDim[0]-1, self.selected_tile[1])
        if self.selected_tile[0]>self.setDim[0]: self.selected_tile = (0, self.selected_tile[1])
        if self.selected_tile[1]<0: self.selected_tile = (self.selected_tile[0], self.setDim[1])
        if self.selected_tile[1]>self.setDim[1]: self.selected_tile = (self.selected_tile[0], 0)
    def cam_movement(self):
        #cam movement
        if Keys.is_held(Keys.a): self.cam.x -= self.cam_speed*self.dt
        if Keys.is_held(Keys.d): self.cam.x += self.cam_speed*self.dt
        if Keys.is_held(Keys.w): self.cam.y -= self.cam_speed*self.dt
        if Keys.is_held(Keys.s): self.cam.y += self.cam_speed*self.dt
        self.cam.update()

def point_world_to_tilemap(x, y, width, height):
    return (x//width, y//height)


            
