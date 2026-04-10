import pygame
from function import numberFollowTarget, WHITE
from core.resource_manager import ResourceManager
from entities.base import Entity

class Player(Entity):
    def __init__(self, location_x, location_y):
        super().__init__()
        rm = ResourceManager.get_instance()
        settings = rm.load_config("config/settings.json")["player"]
        
        self.raw_image = rm.get_image("player/stand1_1.png")
        self.image = self.raw_image
        self.ATKimages = [  
            [rm.get_image("player//swingO1_0.png"), rm.get_image("player//swingO1_1.png"), rm.get_image("player//swingO1_2.png")],
            [rm.get_image("player//swingO2_0.png"), rm.get_image("player//swingO2_1.png"), rm.get_image("player//swingO2_2.png")],
            [rm.get_image("player//swingO1_0.png"), rm.get_image("player//swingO3_1.png"), rm.get_image("player//swingO3_2.png")] 
        ]
        self.ATKseries_index = 0
        self.ATKseries_photo_index = 0
        self.isATK = False
        self.rect = self.raw_image.get_rect()
        self.rect.topleft = (location_x, location_y)
        self.mask = pygame.mask.from_surface(self.image)
        self.width = self.raw_image.get_width()
        self.height = self.raw_image.get_height()
        self.life = settings["life"]
        self.power = settings["max_power"]
        
        # font
        self.life_font = pygame.font.SysFont(None, 40)
        self.life_text_surface = self.life_font.render(f"Life: {self.life}", True, WHITE)
    
    def update(self):
        if self.power < 100:
            self.power += 1
        
        if self.isATK:
            self.image = self.ATKimages[self.ATKseries_index][self.ATKseries_photo_index // 11]

            ATKSERIES_FINAL_INDEX = 2
            ATKSERIES_PHOTO_FINAL_INDEX = 32

            if self.ATKseries_photo_index == ATKSERIES_PHOTO_FINAL_INDEX:
                self.ATKseries_photo_index = 0
                self.isATK = False
                if self.ATKseries_index == ATKSERIES_FINAL_INDEX:
                    self.ATKseries_index = 0
                else:
                    self.ATKseries_index += 1
            else:
                self.ATKseries_photo_index += 1
        else:
            self.image = self.raw_image
        
    def attack(self):
        if self.power > 0:
            self.isATK = True
            rm = ResourceManager.get_instance()
            settings = rm.load_config("config/settings.json")["player"]
            self.power -= settings["attack_cost"]

    def hurt(self, damage=1):
        super().hurt(damage)
        self.life_text_surface = self.life_font.render(f"Life: {self.life}", True, WHITE)


class AP(pygame.sprite.Sprite):
    def __init__(self, location) -> None:
        super().__init__()
        rm = ResourceManager.get_instance()
        raw_image = rm.get_image("player//APline.png")
        self.raw_image = pygame.transform.scale(raw_image, (100, 20))
        self.image = self.raw_image
        self.rect = self.image.get_rect()
        self.rect.topleft = location
        self.width = self.image.get_width()
        self.height = self.image.get_height()
        self.isAPchange = False
    
    def update(self, player_AP) -> None:
        if self.isAPchange and player_AP > 0:
            newWidth = numberFollowTarget(self.width, player_AP, 0.5)
            if self.width - newWidth <= 1:
                self.isAPchange = False
            else:
                self.image = pygame.transform.scale(self.raw_image, (newWidth, self.height))
                self.width = newWidth
        if 0 < player_AP < 100:
            self.image = pygame.transform.scale(self.raw_image, (player_AP, self.height))
