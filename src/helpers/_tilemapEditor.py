import pygame

from ..basics.camera import Camera
from ..basics.input import Keys
from .._net import Global

def gen_collision_rects(width, height):
    return {
        1: pygame.Rect(0, 0, width, height),
        2: pygame.Rect(0, 0, width, height//2),
        3: pygame.Rect(0, height//2, width, height//2),
        4: pygame.Rect(0, 0, width//2, height),
        5: pygame.Rect(width//2, 0, width//2, height)
    }

class _TileMapEditor:
    def __init__(self, x, y, width, height, map, exit_key, pin=(0, 0)):
        self.width, self.height = width, height
        self.map = map
        self.running = True
        self.exit_key = exit_key
        self._pin = pin

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
        #get the dim of the original tileset
        self.setDim = Global.assets._tileset_cache_data[self.map.name]
        self.setDim = (self.setDim[0]-1, self.setDim[1]-1)
        self.colTypes = gen_collision_rects(self.map.width, self.map.height)
        self.current_col_type = 1
        self.mapColType = 5        

        #keys
        self.key_picking = Keys.tab
        self.key_picking_exit = False
        self.save_cam_pos = (0, 0)
        self.can_click = True
        self.key_collision = Keys.c
        self.key_collision_exit = False

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

        self.change_title(self.mode)
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
            if Keys.is_pressed(self.key_picking):
                self.mode = "picking"
                self.save_cam_pos = (self.cam.x, self.cam.y)
                self.cam.x, self.cam.y = 0, 0
            elif Keys.is_pressed(self.key_collision):
                self.mode = "collision"
                self.save_cam_pos = (self.cam.x, self.cam.y)
                self.cam.x, self.cam.y = 0, 0
        elif self.mode == "picking":
            if Keys.is_pressed(self.key_picking) and self.key_picking_exit:
                self.mode = "painting"
                self.cam.x, self.cam.y = self.save_cam_pos
                self.key_picking_exit = False
            else: self.key_picking_exit = True
            if Keys.is_pressed(self.key_collision):
                self.mode = "collision"
                self.save_cam_pos = (self.cam.x, self.cam.y)
                self.cam.x, self.cam.y = 0, 0
            #update logic
            self.cam_movement()
            self.picking_logic()
            self.basic_tile_selecting()
        elif self.mode == "collision":
            if Keys.is_pressed(self.key_collision) and self.key_collision_exit:
                self.mode = "painting"
                self.key_collision_exit = False
                self.cam.x, self.cam.y = self.save_cam_pos
            else: self.key_collision_exit = True
            self.cam_movement()
            self.collision_logic()

    def render(self):
        self.screen.fill("black")
        #render
        if self.mode == "painting":
            self.render_otherTilemaps()
            self.render_tiles()
        elif self.mode == "picking":
            self.render_picking()
        elif self.mode == "collision":
            self.render_collision()

        #update
        self.win.flip()

    def collision_logic(self):
        #change col type based on mouse wheel
        for event in Global.events:
            if event.type == pygame.MOUSEWHEEL:
                if event.y > 0: self.current_col_type += 1
                else: self.current_col_type -= 1
                #wrap around
                if self.current_col_type < 1: self.current_col_type = 5
                elif self.current_col_type > 5: self.current_col_type = 1
                break
            if event.type == pygame.MOUSEBUTTONDOWN:
                mpos = pygame.mouse.get_pos()
                tpos = point_world_to_tilemap(mpos[0]+self.cam.x, mpos[1]+self.cam.y, self.map.width, self.map.height)
                if event.button == 1:
                    self.map.collDef[tpos] = self.current_col_type
                elif event.button == 3:
                    self.map.collDef.pop(tpos, None)
    def render_collision(self):
        #render tileset
        for pos, image in self.map.tileset.items():
            tx = pos[0] * self.map.width
            ty = pos[1] * self.map.height
            self.screen.blit(image, (tx-self.cam.x, ty-self.cam.y))
        #render existing collisions on tiles
        for pos, num in self.map.collDef.items():
            rect = self.colTypes[num].copy()
            rect.x += pos[0] * self.map.width - self.cam.x
            rect.y += pos[1] * self.map.height - self.cam.y
            pygame.draw.rect(self.screen, "red", rect, 2)
        #render col rect on mouse
        #draw square around mouse
        mpos = pygame.mouse.get_pos()
        tpos = point_world_to_tilemap(mpos[0]+self.cam.x, mpos[1]+self.cam.y, self.map.width, self.map.height)
        rect = self.colTypes[self.current_col_type].copy()
        rect.x += tpos[0] * self.map.width - self.cam.x
        rect.y += tpos[1] * self.map.height - self.cam.y
        pygame.draw.rect(self.screen, "green", rect)
        pygame.draw.rect(self.screen, "white", (tpos[0]*self.map.width-self.cam.x, tpos[1]*self.map.height-self.cam.y, self.map.width, self.map.height), 1)

    def picking_logic(self):
        if pygame.mouse.get_pressed()[0]:
            mpos = pygame.mouse.get_pos()
            tpos = point_world_to_tilemap(mpos[0]+self.cam.x, mpos[1]+self.cam.y, self.map.width, self.map.height)
            self.selected_tile = tpos
            self.mode = "painting"
            self.cam.x, self.cam.y = self.save_cam_pos
            self.key_picking_exit = False
            self.can_click = False
        elif Keys.is_pressed(Keys.enter):
            self.mode = "painting"
            self.cam.x, self.cam.y = self.save_cam_pos
            self.key_picking_exit = False
            self.can_click = False

    def render_picking(self):
        #render tileset
        for pos, image in self.map.tileset.items():
            tx = pos[0] * self.map.width
            ty = pos[1] * self.map.height
            self.screen.blit(image, (tx-self.cam.x, ty-self.cam.y))
        #render box around selected tile
        tx = self.selected_tile[0] * self.map.width - self.cam.x
        ty = self.selected_tile[1] * self.map.height - self.cam.y
        pygame.draw.rect(self.screen, "yellow", (tx, ty, self.map.width, self.map.height), 2)
        #draw square around mouse
        mpos = pygame.mouse.get_pos()
        tpos = point_world_to_tilemap(mpos[0]+self.cam.x, mpos[1]+self.cam.y, self.map.width, self.map.height)
        pygame.draw.rect(self.screen, "white", (tpos[0]*self.map.width-self.cam.x, tpos[1]*self.map.height-self.cam.y, self.map.width, self.map.height), 1)

    def render_tiles(self):
        #draw orgin
        point = (self._pin[0]-self.cam.x, self._pin[1]-self.cam.y)
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
        if pygame.mouse.get_pressed()[0] and self.can_click and not Keys.is_held(Keys.f):
            mpos = pygame.mouse.get_pos()
            tpos = point_world_to_tilemap(mpos[0]+self.cam.x, mpos[1]+self.cam.y, self.map.width, self.map.height)
            self.map.tiles[tpos] = self.selected_tile
        elif not pygame.mouse.get_pressed()[0]: self.can_click = True
        elif pygame.mouse.get_pressed()[0] and self.can_click and Keys.is_held(Keys.f):
            #fill area logic
            self.fillBrushLogic()
        #erasing logic
        if pygame.mouse.get_pressed()[2]:
            mpos = pygame.mouse.get_pos()
            tpos = point_world_to_tilemap(mpos[0]+self.cam.x, mpos[1]+self.cam.y, self.map.width, self.map.height)
            self.map.tiles.pop(tpos, None)

    def fillBrushLogic(self):
        # 1. Get the mouse position in World Pixels
        mpos = pygame.mouse.get_pos()
        world_x = mpos[0] + self.cam.x
        world_y = mpos[1] + self.cam.y
        
        # 2. Convert to Grid/Tile coordinates (e.g., 0, 1, 2... NOT pixels like 32, 64)
        start_tile = point_world_to_tilemap(world_x, world_y, self.map.width, self.map.height)
        
        # If the starting tile is already occupied, don't fill anything
        if start_tile in self.map.tiles:
            return

        # 3. Setup our Queue and Tracker sets
        queue = [start_tile]
        used = set([start_tile])
        tiles_to_place = []
        
        # Safety limit to prevent freezing if filling an unbounded open screen
        MAX_FILL_TILES = 1000 

        # 4. The Flood Fill Loop
        while len(queue) > 0:
            if len(tiles_to_place) > MAX_FILL_TILES:
                return # Cancel completely to avoid a system freeze
                
            # Pop the first tile coordinate out of the front of our queue
            current_tile = queue.pop(0)
            tiles_to_place.append(current_tile)
            
            # 5. Define 4-directional neighbors in Grid Space
            cx, cy = current_tile
            neighbors = [
                (cx + 1, cy), # Right
                (cx - 1, cy), # Left
                (cx, cy + 1), # Down
                (cx, cy - 1)  # Up
            ]
            
            for n in neighbors:
                # Skip if we already evaluated or queued this tile position
                if n in used:
                    continue
                    
                # Skip if there is an existing tile acting as a boundary wall
                if n in self.map.tiles:
                    continue
                    
                # It's an open, unvisited tile! Mark it used and queue it up
                used.add(n)
                queue.append(n)

        # 6. Execution Phase
        # Commit all computed tiles straight to the engine map matrix array
        for tile_pos in tiles_to_place:
            # Matches your engine style: storing directly via grid tuples
            self.map.tiles[tile_pos] = self.selected_tile


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

    def render_otherTilemaps(self):
        #render tilemaps from Global with respective layers
        layer = -5
        max_layer = 10
        while layer <= max_layer:
            if layer in Global.tilemaps and layer != self.map.layer:
                for map in Global.tilemaps[layer]:
                    for pos, tile in map.tiles.items():
                        tx = pos[0] * map.width - self.cam.x
                        ty = pos[1] * map.height - self.cam.y
                        if tx > -map.width and tx < self.width+map.width and ty > -map.height and ty < self.height+map.height:
                            image = map.tileset[tile]
                            self.screen.blit(image, (tx, ty))
            layer += 1

    def change_title(self, mode):
        self.win.title = f"Tilemap Editor - {mode.capitalize()} Mode"

def point_world_to_tilemap(x, y, width, height):
    return (int(x//width), int(y//height))

def around(pos):
    return [(pos[0]-1, pos[1]), (pos[0]+1, pos[1]), (pos[0], pos[1]-1), (pos[0], pos[1]+1), (pos[0]-1, pos[1]-1), (pos[0]-1, pos[1]+1), (pos[0]+1, pos[1]-1), (pos[0]+1, pos[1]+1)]


            
