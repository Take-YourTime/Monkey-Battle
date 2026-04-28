import pygame
from random import randint
from core.resource_manager import ResourceManager
from entities.base import Entity
from effects.animations import Monkey_BananaHit
from function import REFERENCE_FPS

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
        self.dieImages = [
            rm.get_image("angelMonkey\\die0.png"), rm.get_image("angelMonkey\\die1.png"), rm.get_image("angelMonkey\\die2.png")
        ]
        
        self.mask = pygame.mask.from_surface(self.raw_image)

        self.image = self.raw_image
        self.index = 0.0 # frame index (float for delta time)
        self.x_moving_destination = randint(settings["moving_range_min"], settings["moving_range_max"])
        self.isATK = False
        self.keepWalking = True
        self.isDying = False
        self.die_index = 0.0
        self.energy = float(settings["energy_limit"]) # need energy to attack or use skills
        self._banana_thrown = False  # flag for banana throw trigger
        self.stun_timer = 0.0        # 重擊剩餘時間（秒）
        
        self.rect = self.image.get_rect()
        self.rect.topleft = (location_x, location_y)
        self.x = float(location_x)
        self.width = self.raw_image.get_width()
        self.height = self.raw_image.get_height()
        self.life = settings["life"]
        
    def stun(self, duration: float):
        """施加重擊，強制取消攻擊動畫並停止行動。"""
        if self.isDying:
            return
        self.stun_timer = duration
        self.isATK = False
        self.index = 0.0
        self._banana_thrown = False
        self.image = self.raw_image

    def update(self, delta_time, player, monkey_BananaHit_group):
        time_step = delta_time * REFERENCE_FPS

        # ── 重擊狀態：停止所有行動 ──
        if self.stun_timer > 0:
            self.stun_timer -= delta_time
            self.image = self.raw_image
            return

        if self.isDying:
            final = len(self.dieImages) * 15
            if self.die_index < final:
                img_idx = min(int(self.die_index) // 15, len(self.dieImages) - 1)
                self.image = self.dieImages[img_idx]
                self.die_index += time_step
            else:
                self.kill()
            return

        if self.keepWalking:
            self.moving(time_step)
            return

        # Using 176 frames to cleanly divide 11 images (16 frames each)
        THROW_BANANA_FRAME = 119 # Keep banana throw frame same or scale.
        FINAL_FRAME = 176

        if self.isATK:
            if self.index < THROW_BANANA_FRAME:
                img_idx = min(int(self.index) // 16, len(self.ATKimages) - 1)
                self.image = self.ATKimages[img_idx]
                self.index += time_step

            elif not self._banana_thrown:
                self._banana_thrown = True
                rm = ResourceManager.get_instance()
                # Angel monkey uses the same banana hit sound with monkey
                hit_face_sound = rm.get_sound("monkey\\banana\\banana_hit_face.wav", 0.5)
                monkey_BananaHit_group.add( Monkey_BananaHit(player.rect.centerx - 30, player.rect.top + 60) )
                player.hurt(1) # throw banana at player (always hit)
                hit_face_sound.play()
                self.index += time_step

            elif self.index < FINAL_FRAME:
                img_idx = min(int(self.index) // 16, len(self.ATKimages) - 1)
                self.image = self.ATKimages[img_idx]
                self.index += time_step

            else:
                self.image = self.raw_image
                self.isATK = False
                self.index = 0.0
        elif self.energy >= 300:
            self.attack()
            self.energy = 0.0
        else:
            self.energy += time_step
    
    def hurt(self, damage=1):
        if self.isDying: return
        if self.life > damage:
            self.life -= damage
        else:
            self.life = 0
            self.isDying = True
            self.stun_timer = 0.0
            # Clear mask to prevent further projectile collisions while dying
            self.mask = pygame.Mask(self.mask.get_size())

    # monkey attack
    def attack(self):
        self.isATK = True
        self._banana_thrown = False

    # monkey moving to the left
    def moving(self, time_step):
        if self.rect.left > self.x_moving_destination:
            self.index += time_step
            if self.index >= 90:
                self.index = 0.0
                self.image = self.raw_image
            elif self.index >= 70:
                self.x -= 1.5 * time_step
                self.image = self.walkingImages[3]
            elif self.index >= 45:
                self.x -= 1.5 * time_step
                self.image = self.walkingImages[2]
            elif self.index >= 15:
                self.x -= 2 * time_step
                self.image = self.walkingImages[1]
            elif self.index >= 5:
                self.x -= 0.5 * time_step
                self.image = self.walkingImages[0]
            else:
                self.x -= 0.5 * time_step
                self.image = self.raw_image
            
            self.rect.left = int(self.x)
        else:
            self.index = 0.0
            self.keepWalking = False
            self.image = self.raw_image

