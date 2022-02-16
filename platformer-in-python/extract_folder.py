import os
from pathlib import Path

import pygame

def import_folder(path):
    surface_list = []
    
    for _, _, sprite_assets in os.walk(path):
        for image in sprite_assets:
            full_path = path / image
            image_surf = pygame.image.load(full_path).convert_alpha()
            surface_list.append(image_surf)
    
    return surface_list