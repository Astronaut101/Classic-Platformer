import sys

import pygame

from levels import Level
from settings import level_map
from settings import screen_height, screen_width
from tiles import Tile

# Initializing game level variables
screen_width = 1200
screen_height = 700

pygame.init()
screen = pygame.display.set_mode((screen_width, screen_height))
clock = pygame.time.Clock()
level = Level(level_map, screen)

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
    
    screen.fill('black')
    level.run()

    pygame.display.update()
    clock.tick(60)