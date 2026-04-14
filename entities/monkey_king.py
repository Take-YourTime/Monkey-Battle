import pygame
from core.resource_manager import ResourceManager
from function import WINDOW_WIDTH
from entities.base import Entity
from entities.projectiles import Banana

class MonkeyKing(Entity):
    
    def __init__(self, location_x, location_y) -> None:
        super().__init__()
        rm = ResourceManager.get_instance()
        settings = rm.load_config("config/settings.json")["monkey_king"]

        self.raw_image = rm.get_image("monkeyKing\\monkeyKing.png")
        self.skill_sound = rm.get_sound("monkeyKing\\light_saber.wav", 0.9)
        self.throw_sound = rm.get_sound("monkeyKing\\throw.wav", 0.6)

        self.image = self.raw_image
        self.index = 0
        self.ATKimages = [
            rm.get_image("monkeyKing\\monkey_boss_attack0.png"), rm.get_image("monkeyKing\\monkey_boss_attack1.png"), 
            rm.get_image("monkeyKing\\monkey_boss_attack2.png"), rm.get_image("monkeyKing\\monkey_boss_attack3.png"),
            rm.get_image("monkeyKing\\monkey_boss_attack4.png"), rm.get_image("monkeyKing\\monkey_boss_attack5.png"),
            rm.get_image("monkeyKing\\monkey_boss_attack6.png"), rm.get_image("monkeyKing\\monkey_boss_attack7.png"),
            rm.get_image("monkeyKing\\monkey_boss_attack8.png"), rm.get_image("monkeyKing\\monkey_boss_attack9.png")
        ]
        self.isATK = False
        self.energy = 300
        self.walkingImages = [  
            rm.get_image("monkeyKing\\walking1.png"), rm.get_image("monkeyKing\\walking2.png"),
            rm.get_image("monkeyKing\\walking3.png"), rm.get_image("monkeyKing\\walking4.png"),
            rm.get_image("monkeyKing\\walking5.png"), rm.get_image("monkeyKing\\walking6.png") 
        ]
        self.keepWalking = True
        self.rect = self.image.get_rect()
        self.rect.topleft = (location_x, location_y)
        self.mask = pygame.mask.from_surface(self.raw_image)
        self.width = self.raw_image.get_width()
        self.height = self.raw_image.get_height()
        self.life = settings["life"]
        self.energy_limit = settings["energy_limit"]

    def update(self, banana_group) -> None:
        THROW_BANANA_FRAME = 80
        FINAL_FRAME = 100
        if self.keepWalking:
            self.walking()
        elif self.isATK:
            if self.index == 0:
                self.skill_sound.play()
                self.index += 1
            elif self.index < THROW_BANANA_FRAME :
                self.image = self.ATKimages[self.index // 10]
                self.index += 1
            elif self.index == THROW_BANANA_FRAME: 
                self.throw_sound.play()
                banana_group.add( Banana( (self.rect.center[0], (self.rect.top + self.height // 2)) ) )
                banana_group.add( Banana( (self.rect.center[0], (self.rect.top + self.height // 2 + 20)) ) )
                banana_group.add( Banana( (self.rect.center[0], (self.rect.top + self.height // 2 - 20)) ) )
                self.image = self.ATKimages[8]
                self.index += 1
            elif self.index < FINAL_FRAME:
                self.image = self.ATKimages[9]
                self.index += 1
            else:
                self.image = self.raw_image
                self.isATK = False
                self.index = 0
        elif self.energy >= self.energy_limit:
            self.attack()
            self.energy = 0
        else:
            self.energy += 1
    
    def attack(self):
        self.isATK = True

    def walking(self):
        if self.rect.left > WINDOW_WIDTH * (700.0 / 1280.0):
            self.rect.left -= 1
            self.index += 1

            if self.index == 107:
                self.index = 0
            else:
                self.image = self.walkingImages[self.index // 18]
        else:
            self.index = 0
            self.keepWalking = False
            self.image = self.raw_image
