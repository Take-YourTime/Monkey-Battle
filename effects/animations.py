import pygame
from random import randint
from core.resource_manager import ResourceManager

class AnimatedEffect(pygame.sprite.Sprite):
    """
    Base class for short-lived visual effects.
    """
    def __init__(self):
        super().__init__()
        self.images = []   
        self.image = None
        self.index = 0
        self.rect = None
        
    def update_animation(self, frames_per_image, final_frame):
        if self.index < final_frame:
            self.image = self.images[self.index // frames_per_image]
            self.index += 1
            return True
        else:
            self.kill()
            return False

class BananaHit(AnimatedEffect):
    
    def __init__(self, location):
        super().__init__()
        rm = ResourceManager.get_instance()
        self.images = [  
            rm.get_image("monkeyKing/banana/hit0.png"),
            rm.get_image("monkeyKing/banana/hit1.png"),
            rm.get_image("monkeyKing/banana/hit2.png")
        ]
        self.image = self.images[0]
        self.rect = self.image.get_rect()
        self.rect.topleft = location
    
    def update(self):
        FINAL_FRAME = 30
        self.update_animation(10, FINAL_FRAME)


class Monkey_BananaHit(AnimatedEffect):

    def __init__(self, location_x, location_y) -> None:
        super().__init__()
        rm = ResourceManager.get_instance()
        self.images = [
            rm.get_image("monkey\\banana\\banana1.png"),
            rm.get_image("monkey\\banana\\banana2.png"),
            rm.get_image("monkey\\banana\\banana3.png"),
            rm.get_image("monkey\\banana\\banana4.png"),
            rm.get_image("monkey\\banana\\banana5.png")
        ]
        self.image = self.images[0]
        self.rect = self.image.get_rect()
        self.rect.topleft = (location_x, location_y)
        self.y = float(location_y)

    def update(self) -> None:
        if self.index < 50:
            self.image = self.images[self.index // 10]
            self.index += 1
            self.rect.x -= 1
            self.y -= 0.5
            self.rect.y = self.y
        else:
            self.kill()


class PencilFolded(pygame.sprite.Sprite):

    def __init__(self, location, angle) -> None:
        super().__init__()
        rm = ResourceManager.get_instance()
        self.raw_images = [
            rm.get_image("player/attack/pencil_fold1.png"),
            rm.get_image("player/attack/pencil_fold2.png")
        ]
        self.image = pygame.transform.rotate(self.raw_images[randint(0, 1)], angle)
        self.rect = self.image.get_rect()
        self.rect.x = location[0]
        self.rect.centery = location[1]
        self.opacity = 255
        
    def update(self) -> None:
        self.opacity -= 5
        if self.opacity <= 0:
            self.kill()
