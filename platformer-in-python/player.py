from pathlib import Path
from extract_folder import import_folder

import pygame

class Player(pygame.sprite.Sprite):
    
    def __init__(self, pos: tuple):
        super().__init__()
        self.import_character_assets()  # Making sure that we are reflecting the animations properly
        self.frame_index = 0
        self.animation_speed = 0.15
        self.image = self.animations['09-Idle Sword'][self.frame_index]
        self.rect = self.image.get_rect(topleft=pos)
        # self.image = pygame.Surface((32,64))
        # self.image.fill('red')
        
        # Player Movement
        self.direction = pygame.math.Vector2(0,0)
        self.speed = 7
        self.gravity = 0.8
        self.jump_speed = -16
    
    def import_character_assets(self):
        character_path = Path('../Treasure Hunters/Captain Clown Nose/Sprites/Captain Clown Nose/Captain Clown Nose with Sword')
        self.animations = {'09-Idle Sword': [], '10-Run Sword': [], '11-Jump Sword': [], '12-Fall Sword': []}
        
        for animation in self.animations.keys():
            full_path = character_path / Path(animation)
            self.animations[animation] = import_folder(full_path)

    def animate(self):
        animation = self.animations["09-Idle Sword"]
        
        # Looping over the frame index
        self.frame_index += self.animation_speed
        if self.frame_index > len(animation):
            self.frame_index = 0  # Resetting the animation frame to fit within the size of the sprite elements
        
        self.image = animation[int(self.frame_index)]  # Converting float values from the animation speed values into integers

    def get_input(self):
        keys = pygame.key.get_pressed()
        
        if keys[pygame.K_RIGHT]:
            self.direction.x = 1
        elif keys[pygame.K_LEFT]:
            self.direction.x = -1
        else:
            self.direction.x = 0
            
        if keys[pygame.K_SPACE]:
            self.jump()
            
    def apply_gravity(self):
        self.direction.y += self.gravity
        self.rect.y += self.direction.y 
        
    def jump(self):
        # NOTE: No need to apply add capability for every SPACE key interaction for the jump mechanic
        self.direction.y = self.jump_speed
            
    def update(self):
        self.get_input()
        self.animate()