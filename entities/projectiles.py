from function import VIRTUAL_WIDTH, VIRTUAL_HEIGHT, REFERENCE_FPS
import pygame
import math
from core.resource_manager import ResourceManager
from function import get_normalize_vector

from entities.base import Projectile
from effects.animations import PencilFolded, BananaHit, SeedHit

class Pencil(Projectile):
    def __init__(self, width, height, location, destination):
        super().__init__()
        rm = ResourceManager.get_instance()
        self.raw_image = rm.get_image("player/attack/pencil.png")
        self.hit_sound = rm.get_sound("player/attack/hit.wav", 0.5)
        self.image = self.raw_image
        self.angle = 0
        
        if destination[0] - location[0] == 0:
            self.image = pygame.transform.rotate(self.image, 90)
            self.angle = 90
        else:
            self.angle = math.atan((destination[1] - location[1]) / (destination[0] - location[0])) * (-180) / math.pi
            self.image = pygame.transform.rotate(self.image, self.angle)
            
        self.rect = self.image.get_rect()
        self.rect.topleft = location
        self.mask = pygame.mask.from_surface(self.image)
        self.width = width
        self.height = height
        self.location = location
        self.vector_x, self.vector_y = get_normalize_vector(location[0], location[1], destination[0], destination[1])
        self.multiple = 13
        self.time = 0.0
        
    def update(self, delta_time, enemies_groups, obstacles_groups, pencilFolded_group):
        time_step = delta_time * REFERENCE_FPS
        if self.time > 35:
            self.multiple = 15
        elif self.time > 25:
            self.multiple = 3
            self.time += time_step
        elif self.time > 20:
            self.multiple = 4
            self.time += time_step
        elif self.time > 15:
            self.multiple = 5
            self.time += time_step
        else:
            self.time += time_step
            
        self.location = (self.location[0] + self.vector_x * self.multiple * time_step, self.location[1] + self.vector_y * self.multiple * time_step)
        self.rect.topleft = self.location

        
        # Kill the projectile if it leaves the screen bounds.
        if (self.location[0] > VIRTUAL_WIDTH + self.width or 
            self.location[0] < -self.width or 
            self.location[1] > VIRTUAL_HEIGHT + self.height or 
            self.location[1] < -self.height):
            self.kill()
            return
            
        # Optimized collision: use spritecollide for C-level rect pre-filtering,
        # then mask-check only the few rect-overlapping sprites.
        for enemy_group in enemies_groups:
            rect_hits = pygame.sprite.spritecollide(self, enemy_group, False)
            for enemy in rect_hits:
                if self.is_colliding_with(enemy):
                    self.hit_sound.play()
                    pencilFolded_group.add(PencilFolded(self.rect.topleft, self.angle))
                    self.kill()
                    enemy.hurt() # Using standard hurt() interface
                    return
        
        for obstacle_group in obstacles_groups:
            rect_hits = pygame.sprite.spritecollide(self, obstacle_group, False)
            for obstacle in rect_hits:
                if self.is_colliding_with(obstacle):
                    pencilFolded_group.add(PencilFolded(self.rect.topleft, self.angle))
                    self.kill()
                    obstacle.hit()
                    return


class Stone(Projectile):
    _scaled_cache = {}  # class-level cache: {(w,h): (image, mask)}

    def __init__(self, width, height, location, destination):
        super().__init__()
        cache_key = (width, height)
        if cache_key not in Stone._scaled_cache:
            rm = ResourceManager.get_instance()
            raw_image = rm.get_image("magician/stone.png")
            scaled = pygame.transform.scale(raw_image, (width, height))
            mask = pygame.mask.from_surface(scaled)
            Stone._scaled_cache[cache_key] = (scaled, mask)
        self.image, self.mask = Stone._scaled_cache[cache_key]
        self.rect = self.image.get_rect()
        self.rect.topleft = location
        self.width = width
        self.height = height
        self.location = list(location)
        self.vector_x, self.vector_y = get_normalize_vector(location[0], location[1], destination[0], destination[1])
        self.multiple = 12

    def update(self, delta_time, player):
        time_step = delta_time * REFERENCE_FPS
        self.location[0] += self.vector_x * self.multiple * time_step
        self.location[1] += self.vector_y * self.multiple * time_step
        self.rect.topleft = (int(self.location[0]), int(self.location[1]))

        # Kill if it leaves the screen bounds.
        if self.rect.centerx < -self.width:
            self.kill()
            return
            
        if self.is_colliding_with(player):
            rm = ResourceManager.get_instance()
            settings = rm.load_config("config/settings.json")["player"]
            player.hurt(settings["damage_taken"]["stone"])
            self.hit()
    
    def hit(self):
        self.kill()


class Banana(Projectile):
    def __init__(self, location, hit_group):
        super().__init__()
        rm = ResourceManager.get_instance()
        self.raw_image = rm.get_image("monkeyKing\\banana\\banana0.png")
        self.mask = pygame.mask.from_surface(self.raw_image)
        self.roalingImages = [
            rm.get_image("monkeyKing\\banana\\banana0.png"), rm.get_image("monkeyKing\\banana\\banana1.png"),
            rm.get_image("monkeyKing\\banana\\banana2.png"), rm.get_image("monkeyKing\\banana\\banana3.png"),
            rm.get_image("monkeyKing\\banana\\banana4.png"), rm.get_image("monkeyKing\\banana\\banana5.png"),
            rm.get_image("monkeyKing\\banana\\banana6.png"), rm.get_image("monkeyKing\\banana\\banana7.png")
        ]
        self.image = self.raw_image
        self.images_index = 0.0
        self.width = self.raw_image.get_width()
        self.rect = self.image.get_rect()
        self.rect.topleft = location
        self.location = list(location)
        self.hit_group = hit_group
    
    def update(self, delta_time, player, bananaHit_group):
        time_step = delta_time * REFERENCE_FPS
        if self.rect.x < -self.width:
            self.kill()
            return
            
        if self.is_colliding_with(player):
            rm = ResourceManager.get_instance()
            settings = rm.load_config("config/settings.json")["player"]
            player.hurt(settings["damage_taken"]["banana"])
            self.hit()
            return
        
        self.location[0] -= 5 * time_step
        self.rect.x = int(self.location[0])

        self.images_index += time_step
        if self.images_index >= 40:
            self.image = self.raw_image
            self.images_index = 0.0
        else:
            idx = min(int(self.images_index) // 5, len(self.roalingImages) - 1)
            self.image = self.roalingImages[idx]
    
    def hit(self):
        self.hit_group.add(BananaHit(self.rect.topleft))
        self.kill()

class Seed(Projectile):
    def __init__(self, location, vx, vy, angle, hit_group):
        super().__init__()
        rm = ResourceManager.get_instance()
        self.raw_image = rm.get_image("bigWhiteMonkey/shootAttack/seed/seed.png")
        
        self.image = pygame.transform.rotate(self.raw_image, angle)
        self.mask = pygame.mask.from_surface(self.image)
        self.width = self.raw_image.get_width()
        self.rect = self.image.get_rect()
        self.rect.midright = location
        self.location = list(self.rect.center)
        
        self.vector_x = vx
        self.vector_y = vy
        
        self.hit_group = hit_group
        
    def update(self, delta_time, player, seedHit_group):
        time_step = delta_time * REFERENCE_FPS
        # Check if the seed is out of bounds
        if self.rect.centerx < -self.width:
            self.kill()
            return
            
        if self.is_colliding_with(player):
            rm = ResourceManager.get_instance()
            settings = rm.load_config("config/settings.json")["player"]
            player.hurt(settings["damage_taken"]["seed"])
            self.hit()
            return
            
        self.location[0] += self.vector_x * time_step
        self.location[1] += self.vector_y * time_step
        self.rect.center = (int(self.location[0]), int(self.location[1]))

    def hit(self):
        self.hit_group.add(SeedHit(self.rect.center))
        self.kill()


