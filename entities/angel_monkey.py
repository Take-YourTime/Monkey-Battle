import pygame
from random import randint
from core.resource_manager import ResourceManager
from entities.base import Entity
from effects.animations import Monkey_BananaHit

class AngelMonkey(Entity):
    def __init__(self, location_x, location_y) -> None:
        super().__init__()
        rm = ResourceManager.get_instance()
        settings = rm.load_config("config/settings.json")["angel_monkey"]

        self.raw_image = rm.get_image("angelMonkey\\angelMonkey.png")
        self.ATKimages = [
            rm.get_image("angelMonkey\\attack0.png"), rm.get_image("angelMonkey\\attack1.png"), rm.get_image("angelMonkey\\attack2.png"),
            rm.get_image("angelMonkey\\attack3.png"), rm.get_image("angelMonkey\\attack4.png"), rm.get_image("angelMonkey\\attack5.png"),
            rm.get_image("angelMonkey\\attack6.png"), rm.get_image("angelMonkey\\attack7.png"), rm.get_image("angelMonkey\\attack8.png"),
            rm.get_image("angelMonkey\\attack9.png"), rm.get_image("angelMonkey\\attack10.png")
        ]
        self.walkingImages = [
            rm.get_image("angelMonkey\\move_0.png"), rm.get_image("angelMonkey\\move_1.png"), 
            rm.get_image("angelMonkey\\move_2.png"), rm.get_image("angelMonkey\\move_3.png")
        ]
        
        self.mask = pygame.mask.from_surface(self.raw_image)

        self.image = self.raw_image
        self.index = 0 # frame index
        self.x_moving_destination = randint(settings["moving_range_min"], settings["moving_range_max"])
        self.isATK = False
        self.keepWalking = True
        self.energy = settings["energy_limit"] # need energy to attack or use skills
        
        self.rect = self.image.get_rect()
        self.rect.topleft = (location_x, location_y)
        self.x = float(location_x)
        self.width = self.raw_image.get_width()
        self.height = self.raw_image.get_height()
        self.life = settings["life"]
        
    def update(self, player, monkey_BananaHit_group):
        # Using 176 frames to cleanly divide 11 images (16 frames each)
        THROW_BANANA_FRAME = 119 # Keep banana throw frame same or scale.
        FINAL_FRAME = 176

        if self.keepWalking:
            self.moving()
        elif self.isATK:
            if self.index < THROW_BANANA_FRAME:
                img_idx = min(len(self.ATKimages) - 1, self.index // 16)
                self.image = self.ATKimages[img_idx]
                self.index += 1

            elif self.index == THROW_BANANA_FRAME:
                rm = ResourceManager.get_instance()
                # Angel monkey uses the same banana sound for now
                hit_face_sound = rm.get_sound("monkey\\banana\\banana_hit_face.wav", 0.5)
                monkey_BananaHit_group.add( Monkey_BananaHit(player.rect.centerx - 30, player.rect.top + 60) )
                player.hurt(1) # throw banana at player (always hit)
                hit_face_sound.play()
                self.index += 1

            elif self.index < FINAL_FRAME:
                img_idx = min(len(self.ATKimages) - 1, self.index // 16)
                self.image = self.ATKimages[img_idx]
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
    
    # monkey attack
    def attack(self):
        self.isATK = True

    # monkey moving to the left
    def moving(self):
        if self.rect.left > self.x_moving_destination:
            self.index += 1
            if self.index >= 90:
                self.index = 0
                self.image = self.raw_image
            elif self.index >= 70:
                self.x -= 1.5
                self.image = self.walkingImages[3]
            elif self.index >= 45:
                self.x -= 1.5
                self.image = self.walkingImages[2]
            elif self.index >= 15:
                self.x -= 2
                self.image = self.walkingImages[1]
            elif self.index >= 5:
                self.x -= 0.5
                self.image = self.walkingImages[0]
            else:
                self.x -= 0.5
                self.image = self.raw_image
            
            self.rect.left = self.x
        else:
            self.index = 0
            self.keepWalking = False
            self.image = self.raw_image
