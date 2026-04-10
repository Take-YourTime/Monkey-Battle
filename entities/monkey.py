import pygame
from random import randint
from core.resource_manager import ResourceManager
from entities.base import Entity
from effects.animations import Monkey_BananaHit

class Monkey(Entity):


    def __init__(self, location_x, location_y) -> None:
        super().__init__()
        rm = ResourceManager.get_instance()
        settings = rm.load_config("config/settings.json")["monkey"]

        self.raw_image = rm.get_image("monkey\\monkey.png")
        self.ATKimages = [
            rm.get_image("monkey\\attack1_0.png"), rm.get_image("monkey\\attack1_1.png"), rm.get_image("monkey\\attack1_2.png"),
            rm.get_image("monkey\\attack1_3.png"), rm.get_image("monkey\\attack1_4.png"), rm.get_image("monkey\\attack1_5.png"),
            rm.get_image("monkey\\attack1_6.png"), rm.get_image("monkey\\attack1_7.png"), rm.get_image("monkey\\attack1_8.png")
        ]
        self.walkingImages = [
            rm.get_image("monkey\\move_1.png"), rm.get_image("monkey\\move_2.png"), rm.get_image("monkey\\move_3.png")
        ]
        # dieImages are loaded but were never actually used in the original monkey update loop.
        
        self.mask = pygame.mask.from_surface(self.raw_image)

        self.image = self.raw_image
        self.index = 0
        self.x_moving_destination = randint(settings["moving_range_min"], settings["moving_range_max"])
        self.isATK = False
        self.keepWalking = True
        self.energy = settings["energy_limit"]
        
        self.rect = self.image.get_rect()
        self.rect.topleft = (location_x, location_y)
        self.x = float(location_x)
        self.width = self.raw_image.get_width()
        self.height = self.raw_image.get_height()
        self.life = settings["life"]
        
    def update(self, player, monkey_BananaHit_group):
        THROW_BANANA_FRAME = 119
        FINAL_FRAME = 180

        if self.keepWalking:
            self.moving()
        elif self.isATK:
            if self.index < THROW_BANANA_FRAME:
                self.image = self.ATKimages[self.index // 20]
                self.index += 1
            elif self.index == THROW_BANANA_FRAME:
                rm = ResourceManager.get_instance()
                hit_face_sound = rm.get_sound("monkey\\banana\\banana_hit_face.wav", 0.5)
                hit_face_sound.play()
                monkey_BananaHit_group.add( Monkey_BananaHit(player.rect.centerx - 30, player.rect.top + 60) )
                player.hurt(1)
                self.index += 1
            elif self.index < FINAL_FRAME:
                self.image = self.ATKimages[self.index // 20]
                self.index += 1
            else:
                self.image = self.raw_image
                self.isATK = False
                self.index = 0
        elif self.energy >= 300: 
            self.attack()
            self.energy = 0
        else:
            self.energy += 1
    
    def attack(self):
        self.isATK = True

    def moving(self):
        if self.rect.left > self.x_moving_destination:
            self.index += 1
            if self.index == 90:
                self.index = 0
                self.image = self.raw_image
            elif self.index >= 70:
                self.x -= 1.5
                self.image = self.walkingImages[2]
            elif self.index >= 45:
                self.x -= 1.5
                self.image = self.walkingImages[1]
            elif self.index >= 15:
                self.x -= 2
                self.image = self.walkingImages[0]
            else:
                self.x -= 0.5
                self.image = self.raw_image
            
            self.rect.left = self.x
        else:
            self.index = 0
            self.keepWalking = False
            self.image = self.raw_image
