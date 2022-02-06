# 2D Platformer settings
#
# TBC: Initializing on how the levels would be created
# Helpful articles and sites for reference:
# http://www.roguebasin.com/index.php?title=Cellular_Automata_Method_for_Generating_Random_Cave-Like_Levels
# https://stackoverflow.com/questions/17779480/python-random-map-generation-with-perlin-noise

import random

level_map = [
'                   '  # row 0
'                   '
'                   '
'                   '
'                   '
'                   '
'                   '
'                   '
'                   '
'                   '
'                   '
]

tile_size = 64  # in pixels dimensions (64px)
screen_width = 1200
screen_height = len(level_map) * tile_size

# Dynamic Update for Random Map Generation
# level_map_dynamic = [' ' * 19 for _ in range(10)]