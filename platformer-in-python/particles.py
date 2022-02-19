from pathlib import Path

import pygame

from extract_folder import import_folder

class ParticleEffect(pygame.sprite.Sprite):
    
    def __init__(self, pos, file_type):
        super().__init__()
        self.frame_index = 0
        self.animation_speed = 0.5
        if file_type == 'Jump':
            self.frames = import_folder(Path('../Treasure Hunters/Captain Clown Nose/Sprites/Dust Particles/Jump'))
        if file_type == 'Fall':
            self.frames = import_folder(Path('../Treasure Hunters/Captain Clown Nose/Sprites/Dust Particles/Fall'))
        self.image = self.frames[self.frame_index]
        self.rect = self.image.get_rect(center=pos)

    def animate(self):
        self.frame_index += self.animation_speed
        if self.frame_index >= len(self.frames):
            self.kill()
        else:
            self.image = self.frames[int(self.frame_index)]
        
    def update(self, x_shift):
        self.animate()
        self.rect.x += x_shift