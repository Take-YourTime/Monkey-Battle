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


class BookHit(pygame.sprite.Sprite):
    """書本命中特效：使用 bookHit.png 圖片，快速淡出。"""

    def __init__(self, location):
        super().__init__()
        rm  = ResourceManager.get_instance()
        raw = rm.get_image("player/attack/bookHit.png")
        self.raw_image = pygame.transform.smoothscale(raw, (80, 80))
        self.image     = self.raw_image.copy()
        self.rect      = self.image.get_rect(center=location)
        self.opacity   = 255.0

    def update(self, delta_time):
        time_step      = delta_time * REFERENCE_FPS
        self.opacity  -= 8 * time_step
        if self.opacity <= 0:
            self.kill()
        else:
            self.image = self.raw_image.copy()
            self.image.set_alpha(int(self.opacity))


class HealText(pygame.sprite.Sprite):
    """
    浮動治療數字特效：顯示綠色 +X HP 並向上浮動淡出。
    在技能四（休息時刻）結束後觸發。
    """

    def __init__(self, location, amount: int):
        super().__init__()
        font       = pygame.font.SysFont(None, 42)
        text_surf  = font.render(f"+{amount} HP", True, (60, 230, 100))
        # 加一層深色描邊增加可讀性
        outline    = font.render(f"+{amount} HP", True, (20, 80, 30))
        w, h       = text_surf.get_size()
        self.image = pygame.Surface((w + 2, h + 2), pygame.SRCALPHA)
        self.image.blit(outline, (1, 1))
        self.image.blit(text_surf, (0, 0))
        self.rect    = self.image.get_rect(center=location)
        self.y       = float(self.rect.y)
        self.opacity = 255.0

    def update(self, delta_time):
        time_step     = delta_time * REFERENCE_FPS
        self.y       -= 0.8 * time_step      # 每幀向上浮動
        self.rect.y   = int(self.y)
        self.opacity -= 3.5 * time_step      # 約 1.5 秒淡出
        if self.opacity <= 0:
            self.kill()
        else:
            self.image.set_alpha(int(self.opacity))


class MotorcycleExplosion(AnimatedEffect):
    """
    機車命中爆炸特效：使用 AI 生成的爆炸 sprite（或程式碼繪製備用）。
    """
    _cached_frames = None   # 類別快取，避免重複縮放

    def __init__(self, location):
        super().__init__()
        rm = ResourceManager.get_instance()

        if MotorcycleExplosion._cached_frames is None:
            raw = rm.get_image("effects/explosion.png")
            # 縮放成 4 幀漸大的爆炸效果
            sizes = [150, 175, 230, 165]
            MotorcycleExplosion._cached_frames = [
                pygame.transform.scale(raw, (s, s)) for s in sizes
            ]

        self.images = MotorcycleExplosion._cached_frames
        self.image  = self.images[0]
        self.rect   = self.image.get_rect(center=location)
        self._center = location
        self.opacity = 255.0

    def update(self, delta_time):
        time_step   = delta_time * REFERENCE_FPS
        FINAL_FRAME = 32
        if self.index < FINAL_FRAME:
            img_idx     = min(int(self.index) // 8, len(self.images) - 1)
            self.image  = self.images[img_idx].copy()
            alpha       = int(255 * (1.0 - self.index / FINAL_FRAME))
            self.image.set_alpha(alpha)
            self.rect   = self.image.get_rect(center=self._center)
            self.index += time_step
        else:
            self.kill()
