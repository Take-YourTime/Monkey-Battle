import pygame
import random
from function import WINDOW_WIDTH, WINDOW_HEIGHT
from core.resource_manager import ResourceManager
from entities.base import Entity
from entities.projectiles import Stone

class Magician(Entity):

    def __init__(self, width, height) -> None:
        super().__init__()
        rm = ResourceManager.get_instance()
        settings = rm.load_config("config/settings.json")["magician"]
        
        raw_image = rm.get_image("magicion.png")
        self.image = pygame.transform.scale(raw_image, (width, height))
        self.rect = self.image.get_rect()
        self.rect.topleft = (WINDOW_WIDTH + 10, random.randint(0, 150))
        self.mask = pygame.mask.from_surface(self.image)
        self.width = width
        self.height = height
        self.life = settings["life"]
        self.skill_energy = 0
        self.skill_consume = random.randint(settings["skill_consume_min"], settings["skill_consume_max"])
        self.move_times = random.randint(settings["move_times_min"], settings["move_times_max"])
    
    def update(self, stone_group):
        # Movement logic
        if self.move_times > 0:
            self.rect.left -= 1
            self.move_times -= 1
            
        # Attack logic
        if self.skill_energy >= self.skill_consume:
            self.skill_energy = 0
            stone_group.add( Stone(29, 26, (self.rect.left + 10, self.rect.top + 30), (random.randint(20, 100), random.randint(WINDOW_HEIGHT - 230, WINDOW_HEIGHT -80))) )
        else:
            self.skill_energy += 1

