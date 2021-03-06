import pygame


class Tile(pygame.sprite.Sprite):
    
    def __init__(self, pos, size):
        super().__init__()

        ## NOTE: Creating an image of the tile, and filling it with a color.
        ## Can also be loaded from disk. 
        self.image = pygame.Surface((size, size))
        self.image.fill(color='Grey')

        ## Fetching rectangle object has the dimensions of the image.
        ## Update the positions of this object by setting the values of rect.x and rect.y
        self.rect = self.image.get_rect(topleft=(pos))
        
    def update(self, x_shift):
        """Responsible for moving the group of tiles left or right"""
        self.rect.x += x_shift