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

    def horizontal_movement_collision(self):
        player = self.player.sprite
        player.rect.x += player.direction.x * player.speed

        for sprite in self.tiles.sprites():
            if sprite.rect.colliderect(player.rect):
                if player.direction.x < 0:
                    player.rect.left = sprite.rect.right
                elif player.direction.x > 0:
                    player.rect.right = sprite.rect.left

    def vertical_movement_collision(self):
        player = self.player.sprite
        player.apply_gravity()
        
        for sprite in self.tiles.sprites():
            if sprite.rect.colliderect(player.rect):
                if player.direction.y < 0:
                    player.rect.top = sprite.rect.bottom
                    player.direction.y = 0  # When we hit a ceiling when we press jump, this would be able to cancel out the force applied upward.
                elif player.direction.y > 0:
                    player.rect.bottom = sprite.rect.top
                    player.direction.y = 0  # When we hit a floor, this would help stay the player sprite on top of the tile.

    def run(self):
        # Level Tiles
        self.tiles.update(self.world_shift)
        self.tiles.draw(self.display_surface)
        self.scroll_x()
        
        # Player Object
        self.player.update()
        self.horizontal_movement_collision()
        self.vertical_movement_collision()
        self.player.draw(self.display_surface)