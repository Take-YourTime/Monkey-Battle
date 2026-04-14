import pygame
import math
from core.resource_manager import ResourceManager
from function import get_normalize_vector

from entities.base import Projectile
from effects.animations import PencilFolded, BananaHit

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
        self.time = 0
        
    def update(self, enemies_groups, obstacles_groups, pencilFolded_group):
        if self.time > 35:
            self.multiple = 15
        elif self.time > 25:
            self.multiple = 3
            self.time += 1
        elif self.time > 20:
            self.multiple = 4
            self.time += 1
        elif self.time > 15:
            self.multiple = 5
            self.time += 1
        else:
            self.time += 1
            
        self.location = (self.location[0] + self.vector_x * self.multiple, self.location[1] + self.vector_y * self.multiple)
        self.rect.topleft = self.location

        if self.check_out_of_bounds():
            return
            
        # Refactored collision checking
        # Iterate over all enemy groups (Magician, Monkey, MonkeyKing)
        for enemy_group in enemies_groups:
            for enemy in enemy_group:
                if self.is_colliding_with(enemy):
                    self.hit_sound.play()
                    pencilFolded_group.add(PencilFolded(self.rect.topleft, self.angle))
                    self.kill()
                    enemy.hurt() # Using standard hurt() interface
                    return
        
        # Iterate over all obstacles (Stones, Bananas)
        for obstacle_group in obstacles_groups:
            for obstacle in obstacle_group:
                if self.is_colliding_with(obstacle):
                    pencilFolded_group.add(PencilFolded(self.rect.topleft, self.angle))
                    self.kill()
                    obstacle.hit()
                    return


class Stone(Projectile):
    def __init__(self, width, height, location, destination):
        super().__init__()
        rm = ResourceManager.get_instance()
        raw_image = rm.get_image("magician/stone.png")
        self.image = pygame.transform.scale(raw_image, (width, height))
        self.rect = self.image.get_rect()
        self.rect.topleft = location
        self.mask = pygame.mask.from_surface(self.image)
        self.width = width
        self.height = height
        self.location = location
        self.vector_x, self.vector_y = get_normalize_vector(location[0], location[1], destination[0], destination[1])
        self.multiple = 12

    def update(self, player):
        self.location = (self.location[0] + self.vector_x * self.multiple, self.location[1] + self.vector_y * self.multiple)
        self.rect.topleft = self.location

        if self.check_out_of_bounds():
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
        self.images_index = 0
        self.width = self.raw_image.get_width()
        self.rect = self.image.get_rect()
        self.rect.topleft = location
        self.location = list(location)
        self.hit_group = hit_group
    
    def update(self, player, bananaHit_group):
        if self.rect.x < -self.width:
            self.kill()
            return
            
        if self.is_colliding_with(player):
            rm = ResourceManager.get_instance()
            settings = rm.load_config("config/settings.json")["player"]
            player.hurt(settings["damage_taken"]["banana"])
            self.hit()
            return
        
        self.location[0] -= 5
        self.rect.x = self.location[0]

        if self.images_index == 40:
            self.image = self.raw_image
            self.images_index = 0
        else:
            self.image = self.roalingImages[self.images_index // 5]
            self.images_index += 1
    
    def hit(self):
        self.hit_group.add(BananaHit(self.rect.topleft))
        self.kill()

