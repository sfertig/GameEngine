import pygame
from .._net import Global
from ..helpers.utils import change_layer
from ..basics.camera import Camera
from ..basics.input import Keys
from ..physics.collisions import CollisionRect

from ..helpers._tilemap_files import __saveTileMap_json__, __loadTileMap_json__

#tilemap collision types
COL_FULL = 1
COL_HALF_TOP = 2
COL_HALF_BOTTOM = 3
COL_HALF_LEFT = 4
COL_HALF_RIGHT = 5

class Tilemap:
    def __init__(self, name, tileset, show=True, layer=3, dataFile=None, collisionLayers=None):
        self.name = name
        self.tileset: dict[tuple[int, int], pygame.surface.Surface] = tileset
        self.width = tileset[0, 0].get_width()
        self.height = tileset[0, 0].get_height()
        self.show = show
        self.layer = layer

        if collisionLayers is not None: self.collisionLayers = collisionLayers
        else: self.collisionLayers = [layer]

        self.dataFile = dataFile

        self.tiles: dict[tuple[int, int ], tuple[int, int]] = {}
        self.collisions = []
        self.collDef: dict[tuple[int, int], int] = {}

        Global.add_object(layer, self)

        #fallback for hardcoded tilemaps (no loading from file)
        self.__gen_collision_shapes()

    def change_layer(self, new_layer):
        change_layer(self, new_layer, self.layer)
        self.layer = new_layer

    def __gen_collision_shapes(self):
        self.collisions.clear()
        
        # Separate tiles into shapes
        full = []
        
        for key, value in self.tiles.items():
            if value not in self.collDef: 
                continue
            # CORRECTION: Appending 'key' (grid pos) instead of 'value' (tile type)
            if self.collDef[value] == COL_FULL:
                full.append(key)

        # Gen collision shapes
        used = []
        rows = []
        
        # CORRECTION: Explicitly copy full to prevent list modification issues while iterating
        remaining_full = list(full)
        
        while len(remaining_full) > 0:
            # CORRECTION: Pop the first unvisited position to evaluate
            pos = remaining_full.pop(0)
            if pos in used:
                continue
                
            col = CollisionRect(pos[0]*self.width, pos[1]*self.height, self.width, self.height, self.collisionLayers)
            used.append(pos)
            
            # Other tile check
            for tile in full:
                if tile in used: 
                    continue
                if not tile_beside(pos, tile): 
                    continue
                    
                if tile[0] == pos[0]+1 and tile[1] == pos[1]: # Beside to the right
                    col.width += self.width
                    # CORRECTION: Removed 'col.x -= self.width'. Growing right only increases width.
                    used.append(tile)
                elif tile[0] == pos[0]-1 and tile[1] == pos[1]: # Beside to the left
                    col.width += self.width
                    col.x -= self.width # Growing left shifts the start position back
                    used.append(tile)
                    
            # else tile is not to left or right
            rows.append(col)
            # CORRECTION: Re-sync remaining items based on global used list
            remaining_full = [t for t in full if t not in used]
            
        # CORRECTION: Make sure generated rectangles are actually added to your active collisions list
        for r in rows:
            self.collisions.append(r)
            
        print(self.collisions)






    def manual_save_json(self, path=None):
        if path and self.dataFile == None: return
        if path is None: path = self.dataFile
        __saveTileMap_json__(path, self.tiles, self.collDef)
    def manual_load_json(self, path):
        if path and self.dataFile == None: return
        if path is None: path = self.dataFile
        self.tiles, self.collDef = __loadTileMap_json__(path)
        self.__gen_collision_shapes()

    def activateEditor(self):
        _TileMapEditor(600, 800, self).run()
        self.manual_save_json()
        self.__gen_collision_shapes()

    def render(self):
        if not self.show: return
        for pos, tile in self.tiles.items():
            tx = pos[0] * self.width - Global.cam.x
            ty = pos[1] * self.height - Global.cam.y
            if tx > -self.width and tx < Global.screen.get_width()+self.width and ty > -self.height and ty < Global.screen.get_height()+self.height:
                image = self.tileset[tile]
                Global.screen.blit(image, (tx, ty))
        #collision rendering for debug
        for collision in self.collisions:
            collision.render()

def tile_beside(pos, _pos):
    if _pos[0] == pos[0]+1: return True
    elif _pos[0] == pos[0]-1: return True
    elif _pos[1] == pos[1]+1: return True
    elif _pos[1] == pos[1]-1: return True
    return False

class _TileMapEditor:
    def __init__(self, width, height, map: Tilemap):
        self.width, self.height = width, height
        self.map = map
        self.running = True

        self.cam = Camera(-width/2, -height/2)
        self.cam_speed = 275

        self.win = pygame.Window("Tilemap Editor", (width, height))
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

        #cam movement
        if Keys.is_held(Keys.a): self.cam.x -= self.cam_speed*self.dt
        if Keys.is_held(Keys.d): self.cam.x += self.cam_speed*self.dt
        if Keys.is_held(Keys.w): self.cam.y -= self.cam_speed*self.dt
        if Keys.is_held(Keys.s): self.cam.y += self.cam_speed*self.dt
        self.cam.update()

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

    def render(self):
        self.screen.fill("black")
        #render

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

        #test
        #pygame.draw.rect(self.screen, "gray", pygame.Rect(0, 0, self.width, 200))

        #update
        self.win.flip()

def point_world_to_tilemap(x, y, width, height):
    return (x//width, y//height)


            
