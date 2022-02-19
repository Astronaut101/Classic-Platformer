from pathlib import Path

from extract_folder import import_folder

import pygame

class Player(pygame.sprite.Sprite):
    
    def __init__(self, pos: tuple, surface: tuple, create_jump_particles):
        super().__init__()
        self.import_character_assets()  # Making sure that we are reflecting the animations properly
        self.frame_index = 0
        self.animation_speed = 0.15
        self.image = self.animations['09-Idle Sword'][self.frame_index]
        self.rect = self.image.get_rect(topleft=pos)
        # self.image = pygame.Surface((32,64))
        # self.image.fill('red')
        
        # Dust Particles
        self.import_dust_run_particles()
        self.dust_frame_index = 0
        self.dust_animation_speed = 0.15
        self.display_surface = surface
        self.create_jump_articles = create_jump_particles

        # Player Movement
        self.direction = pygame.math.Vector2(0,0)
        self.speed = 7
        self.gravity = 0.8
        self.jump_speed = -16
    
        # Player Status
        self.status = '09-Idle Sword'  # original animation state of the player
        self.facing_right = True  # being able to make the character face left or face right
        self.facing_left = True
        self.on_ground = False
        self.on_ceiling = False
        self.on_left = False
        self.on_right = False

    def import_character_assets(self):
        character_path = Path('../Treasure Hunters/Captain Clown Nose/Sprites/Captain Clown Nose/Captain Clown Nose with Sword')
        self.animations = {'09-Idle Sword': [], '10-Run Sword': [], '11-Jump Sword': [], '12-Fall Sword': []}
        
        for animation in self.animations.keys():
            full_path = character_path / Path(animation)
            self.animations[animation] = import_folder(full_path)

    def import_dust_run_particles(self):
        self.dust_run_particles = import_folder(Path('../Treasure Hunters/Captain Clown Nose/Sprites/Dust Particles/Run'))

    def animate(self):
        animation = self.animations[self.status]  # NOTE: dynamically tracking its latest movement of the player
        
        # Looping over the frame index
        self.frame_index += self.animation_speed
        if self.frame_index > len(animation):
            self.frame_index = 0  # Resetting the animation frame to fit within the size of the sprite elements
        
        image = animation[int(self.frame_index)]  # Converting float values from the animation speed values into integers
        if self.facing_right:
            self.image = image
        else:
            flipped_image = pygame.transform.flip(image,True,False)  # Arguments that take in the image that we need to either face right or left 
            self.image = flipped_image
    
        # set the rectangle animation frame of each animation state
        # NOTE: collision detection to have tight checks if the character is colliding in a certain wall (left or right)
        if self.on_ground and self.on_right:
            self.rect = self.image.get_rect(bottomright=self.rect.bottomright)
        elif self.on_ground and self.on_left:
            self.rect = self.image.get_rect(bottomleft=self.rect.bottomleft)
        elif self.on_ground:
            self.rect = self.image.get_rect(midbottom=self.rect.midbottom)

        # NOTE: collision detection to have tight checks if the character is colliding in a certain ceiling (top)
        elif self.on_ceiling and self.on_right:
            self.rect = self.image.get_rect(topright=self.rect.topright)
        elif self.on_ceiling and self.on_left:
            self.rect = self.image.get_rect(topright=self.rect.topleft)
        elif self.on_ceiling:
            self.rect = self.image.get_rect(midtop=self.rect.midtop)
        
        else:
            self.rect = self.image.get_rect(center=self.rect.center)

    def run_dust_animation(self):
        if self.status == '10-Run Sword' and self.on_ground:
            self.dust_frame_index += self.dust_animation_speed
            if self.dust_frame_index >= len(self.dust_run_particles):
                self.dust_frame_index = 0

            dust_particle = self.dust_run_particles[int(self.dust_frame_index)]

            if self.facing_right:
                pos = self.rect.bottomleft - pygame.math.Vector2(2,20)
                self.display_surface.blit(dust_particle,pos)
            elif self.facing_left:
                pos = self.rect.bottomright - pygame.math.Vector2(45,20)
                flipped_dust_particle = pygame.transform.flip(dust_particle,True,False)
                self.display_surface.blit(flipped_dust_particle,pos)

    def get_input(self):
        keys = pygame.key.get_pressed()
        
        if keys[pygame.K_RIGHT]:
            self.direction.x = 1
            self.facing_right = True
        elif keys[pygame.K_LEFT]:
            self.direction.x = -1
            self.facing_right = False
        else:
            self.direction.x = 0
            
        if keys[pygame.K_SPACE] and self.on_ground:  # Checking that the player will only jump if it is only on the ground.
            self.jump()
            self.create_jump_articles(self.rect.midbottom)

    def get_status(self):
        """Handling the Animation states (State Machine Concept) of every movement of the player"""
        if self.direction.y < 0:
            self.status = '11-Jump Sword'
        # NOTE: In order to handle the smooth transition of the animation of idling / falling / running / jumping,
        # we must be able to check if the y-direction of our player is always greater than the value of the 
        # gravity. 
        elif self.direction.y > 1:
            self.status = '12-Fall Sword'
        elif self.direction.x == 0 and self.direction.y == 0:
            self.status = '09-Idle Sword'
        elif self.direction.x != 0 and self.direction.y == 0:
            self.status = '10-Run Sword'

    def apply_gravity(self):
        self.direction.y += self.gravity
        self.rect.y += self.direction.y 
        
    def jump(self):
        # NOTE: No need to apply add capability for every SPACE key interaction for the jump mechanic
        self.direction.y = self.jump_speed
            
    def update(self):
        self.get_input()
        self.get_status()
        self.animate()
        self.run_dust_animation()