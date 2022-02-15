import pygame

from player import Player
from settings import tile_size
from settings import screen_width
from tiles import Tile

class Level:

    def __init__(self, level_data, surface):
        self.display_surface = surface
        self.setup_level(level_data)
        
        # The more positive the update number (moves to the right) and vice-versa.
        self.world_shift = 0

    def setup_level(self, layout):
        self.tiles = pygame.sprite.Group()
        self.player = pygame.sprite.GroupSingle()  # Responsible for only containing one Sprite / most recent sprite
        
        # Looping through each cell if it's populated or left blank
        for row_index, cell in enumerate(layout):
            for col_index, cell in enumerate(cell):
                x = col_index * tile_size
                y = row_index * tile_size
                
                if cell == "x":
                    tile = Tile((x, y), tile_size)
                    self.tiles.add(tile)
                if cell == "P":
                    player_pos = Player((x,y))
                    self.player.add(player_pos)

    def scroll_x(self):
        player = self.player.sprite
        player_x = player.rect.centerx
        direction_x = player.direction.x
        
        if player_x <= (screen_width / 4) and direction_x < 0:
            self.world_shift = 8
            player.speed = 0
        elif player_x >= (screen_width - (screen_width / 4)) and direction_x > 0:
            self.world_shift = -8
            player.speed = 0
        else:
            self.world_shift = 0
            player.speed = 8

    def run(self):
        
        # Level Tiles
        self.tiles.update(self.world_shift)
        self.tiles.draw(self.display_surface)
        
        # Player Object
        self.player.update()
        self.player.draw(self.display_surface)
        self.scroll_x()