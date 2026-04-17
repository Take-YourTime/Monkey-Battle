import pygame
from random import randint
from core.resource_manager import ResourceManager
from function import REFERENCE_FPS

class AnimatedEffect(pygame.sprite.Sprite):
    """
    Base class for short-lived visual effects.
    """
    def __init__(self):
        super().__init__()
        self.images = []   
        self.image = None
        self.index = 0.0
        self.rect = None
        
    def update_animation(self, time_step, frames_per_image, final_frame):
        if self.index < final_frame:
            img_idx = min(int(self.index) // frames_per_image, len(self.images) - 1)
            self.image = self.images[img_idx]
            self.index += time_step
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
    
    def update(self, delta_time):
        time_step = delta_time * REFERENCE_FPS
        FINAL_FRAME = 30
        self.update_animation(time_step, 10, FINAL_FRAME)


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

    def update(self, delta_time) -> None:
        time_step = delta_time * REFERENCE_FPS
        if self.index < 50:
            img_idx = min(int(self.index) // 10, len(self.images) - 1)
            self.image = self.images[img_idx]
            self.index += time_step
            self.rect.x -= int(1 * time_step)
            self.y -= 0.5 * time_step
            self.rect.y = int(self.y)
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
        self.opacity = 255.0
        
    def update(self, delta_time) -> None:
        time_step = delta_time * REFERENCE_FPS
        self.opacity -= 5 * time_step
        if self.opacity <= 0:
            self.kill()
        else:
            self.image.set_alpha(int(self.opacity))

class SeedHit(AnimatedEffect):
    def __init__(self, location):
        super().__init__()
        rm = ResourceManager.get_instance()
        self.images = [
            rm.get_image("bigWhiteMonkey/shootAttack/seed/seedHit0.png"),
            rm.get_image("bigWhiteMonkey/shootAttack/seed/seedHit1.png"),
            rm.get_image("bigWhiteMonkey/shootAttack/seed/seedHit2.png"),
            rm.get_image("bigWhiteMonkey/shootAttack/seed/seedHit3.png")
        ]
        self.image = self.images[0]
        self.rect = self.image.get_rect()
        self.rect.center = location

    def update(self, delta_time):
        time_step = delta_time * REFERENCE_FPS
        FINAL_FRAME = 20
        if self.index < FINAL_FRAME:
            center = self.rect.center
            img_idx = min(int(self.index) // 5, len(self.images) - 1)
            self.image = self.images[img_idx]
            self.rect = self.image.get_rect()
            self.rect.center = center
            self.index += time_step
            return True
        else:
            self.kill()
            return False


class DustEffect(AnimatedEffect):
    def __init__(self, location):
        super().__init__()
        rm = ResourceManager.get_instance()
        self.images = [
            rm.get_image("bigWhiteMonkey/jumpAttack/dust/dust_0001.png"),
            rm.get_image("bigWhiteMonkey/jumpAttack/dust/dust_0002.png"),
            rm.get_image("bigWhiteMonkey/jumpAttack/dust/dust_0003.png"),
            rm.get_image("bigWhiteMonkey/jumpAttack/dust/dust_0004.png")
        ]
        self.image = self.images[0]
        self.rect = self.image.get_rect()
        self.rect.center = location

    def update(self, delta_time):
        time_step = delta_time * REFERENCE_FPS
        FINAL_FRAME = 20
        if self.index < FINAL_FRAME:
            center = self.rect.center
            img_idx = min(int(self.index) // 5, len(self.images) - 1)
            self.image = self.images[img_idx]
            self.rect = self.image.get_rect()
            self.rect.center = center
            self.index += time_step
            return True
        else:
            self.kill()
            return False

