from function import VIRTUAL_WIDTH, VIRTUAL_HEIGHT, REFERENCE_FPS
import pygame
import math
from core.resource_manager import ResourceManager
from function import get_normalize_vector

from entities.base import Projectile
from effects.animations import PencilFolded, BananaHit, SeedHit


class Pencil(Projectile):
    def __init__(self, width, height, location, destination):
        super().__init__()
        rm = ResourceManager.get_instance()
        self.raw_image = rm.get_image("player/attack/pencil.png")
        self.hit_sound = rm.get_sound("player/sound/pencil_hit.wav", 0.5)
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
        self.time = 0.0
        
    def update(self, delta_time, enemies_groups, obstacles_groups, pencilFolded_group):
        time_step = delta_time * REFERENCE_FPS
        if self.time > 35:
            self.multiple = 15
        elif self.time > 25:
            self.multiple = 3
            self.time += time_step
        elif self.time > 20:
            self.multiple = 4
            self.time += time_step
        elif self.time > 15:
            self.multiple = 5
            self.time += time_step
        else:
            self.time += time_step
            
        self.location = (self.location[0] + self.vector_x * self.multiple * time_step, self.location[1] + self.vector_y * self.multiple * time_step)
        self.rect.topleft = self.location

        # Kill the projectile if it leaves the screen bounds.
        if (self.location[0] > VIRTUAL_WIDTH + self.width or 
            self.location[0] < -self.width or 
            self.location[1] > VIRTUAL_HEIGHT + self.height or 
            self.location[1] < -self.height):
            self.kill()
            return
            
        # Optimized collision: use spritecollide for C-level rect pre-filtering,
        # then mask-check only the few rect-overlapping sprites.
        for enemy_group in enemies_groups:
            rect_hits = pygame.sprite.spritecollide(self, enemy_group, False)
            for enemy in rect_hits:
                if self.is_colliding_with(enemy):
                    self.hit_sound.play()
                    pencilFolded_group.add(PencilFolded(self.rect.topleft, self.angle))
                    self.kill()
                    enemy.hurt() # Using standard hurt() interface
                    return
        
        for obstacle_group in obstacles_groups:
            rect_hits = pygame.sprite.spritecollide(self, obstacle_group, False)
            for obstacle in rect_hits:
                if self.is_colliding_with(obstacle):
                    pencilFolded_group.add(PencilFolded(self.rect.topleft, self.angle))
                    self.kill()
                    obstacle.hit()
                    return


class Book(Projectile):
    """
    丟書技能拋射物：
    - 飛向滑鼠方向
    - 碰到敵方子彈（stone, banana, seed）→ 消除子彈
    - 碰到猴子（除 MonkeyKing）→ 造成傷害 + 重擊 0.5 秒
    """
    SPEED = 10.0

    def __init__(self, location, destination):
        super().__init__()
        rm = ResourceManager.get_instance()
        cfg = rm.load_config("config/settings.json")["player"]["skills"]["book"]

        raw = rm.get_image("player/attack/book.png")
        # 縮放到合理的遊戲大小
        self.raw_image = pygame.transform.scale(raw, (70, 70))

        # 計算旋轉角度
        if destination[0] - location[0] == 0:
            self.angle = 90
        else:
            self.angle = math.atan(
                (destination[1] - location[1]) / (destination[0] - location[0])
            ) * (-180) / math.pi

        self.image = pygame.transform.rotate(self.raw_image, self.angle)
        self.rect  = self.image.get_rect()
        self.rect.center = location
        self.mask  = pygame.mask.from_surface(self.image)

        self.location  = list(location)
        self.vector_x, self.vector_y = get_normalize_vector(
            location[0], location[1], destination[0], destination[1]
        )
        self.multiple  = self.SPEED
        self.damage    = cfg["damage"]
        self.stun_dur  = cfg["stun_duration"]

        # ── 旋轉屬性 ──
        self._spin_angle = float(self.angle)      # 目前旋轉角度（度）
        self._spin_speed = 8.0                    # 每基準幀旋轉度數

        self._hit_sound = rm.get_sound("player/sound/book_hit.wav", 0.7)

    def update(self, delta_time, enemy_groups, bullet_groups, book_hit_group):
        """
        enemy_groups  : 可被重擊的敵人群組列表（不含 MonkeyKing）
        bullet_groups : 可被消除的子彈群組列表（stone, banana, seed）
        book_hit_group: BookHit 特效群組
        """
        from effects.animations import BookHit
        time_step = delta_time * REFERENCE_FPS

        # ── 移動 ──
        self.location[0] += self.vector_x * self.multiple * time_step
        self.location[1] += self.vector_y * self.multiple * time_step
        center = (int(self.location[0]), int(self.location[1]))

        # ── 旋轉：每幀旋轉 _spin_speed 度 ──
        self._spin_angle += self._spin_speed * time_step
        self.image = pygame.transform.rotate(self.raw_image, self._spin_angle)
        self.rect  = self.image.get_rect(center=center)
        self.mask  = pygame.mask.from_surface(self.image)

        # 出界消除
        if (self.location[0] > VIRTUAL_WIDTH + 50 or
                self.location[0] < -50 or
                self.location[1] > VIRTUAL_HEIGHT + 50 or
                self.location[1] < -50):
            self.kill()
            return

        # 碰到敵方子彈 → 消除子彈
        for bgrp in bullet_groups:
            hits = pygame.sprite.spritecollide(self, bgrp, False)
            for bullet in hits:
                if self.is_colliding_with(bullet):
                    bullet.hit()
                    # 書繼續飛（不自毀）

        # 碰到敵人 → 傷害 + 重擊
        for egrp in enemy_groups:
            rect_hits = pygame.sprite.spritecollide(self, egrp, False)
            for enemy in rect_hits:
                if self.is_colliding_with(enemy):
                    self._hit_sound.play()
                    book_hit_group.add(BookHit(self.rect.center))
                    enemy.hurt(self.damage)
                    if hasattr(enemy, "stun"):
                        enemy.stun(self.stun_dur)
                    self.kill()
                    return


class Motorcycle(Projectile):
    """
    機車衝擊技能：
    - 從玩家位置出發，向右方高速衝鋒
    - 碰到猴子 → 爆炸（爆炸特效）+ 造成大量傷害
    - 衝出畫面右側後消失
    - 玩家本身不移動
    """
    SPEED = 0.1

    def __init__(self, location):
        super().__init__()
        rm  = ResourceManager.get_instance()
        cfg = rm.load_config("config/settings.json")["player"]["skills"]["motorcycle"]

        raw = rm.get_image("player/attack/motorcycle.png")
        self.raw_image = pygame.transform.scale(raw, (175, 175))
        self.image = self.raw_image
        self.rect  = self.image.get_rect()
        self.rect.midleft = location
        self.mask  = pygame.mask.from_surface(self.image)

        self.location = list(self.rect.topleft)
        self.vector_x  = 0.05
        self.vector_y  = 0.01
        self.multiple  = self.SPEED
        self.damage    = cfg["damage"]

    def update(self, delta_time, all_enemy_groups, explosion_group):
        from effects.animations import MotorcycleExplosion
        time_step = delta_time * REFERENCE_FPS

        self.location[0] += self.multiple * time_step
        self.rect.topleft = (int(self.location[0]), int(self.location[1]))

        # 出界消除
        if self.rect.left > VIRTUAL_WIDTH + 100:
            self.kill()
            return

        # motrocycle speed up
        if self.multiple < 10:
            self.multiple *= 1.3

        # 碰到任何敵人 → 爆炸
        for egrp in all_enemy_groups:
            rect_hits = pygame.sprite.spritecollide(self, egrp, False)
            for enemy in rect_hits:
                if self.is_colliding_with(enemy):
                    explosion_group.add(MotorcycleExplosion(self.rect.center))
                    enemy.hurt(self.damage)
                    rm = ResourceManager.get_instance()
                    rm.get_sound("player/sound/motorcycle_bomb.wav", 0.8).play()
                    self.kill()
                    return


# ─────────────────────────────────────────────────────────────────────
# Existing projectiles (unchanged)
# ─────────────────────────────────────────────────────────────────────

class Stone(Projectile):
    _scaled_cache = {}  # class-level cache: {(w,h): (image, mask)}

    def __init__(self, width, height, location, destination):
        super().__init__()
        cache_key = (width, height)
        if cache_key not in Stone._scaled_cache:
            rm = ResourceManager.get_instance()
            raw_image = rm.get_image("magician/stone.png")
            scaled = pygame.transform.scale(raw_image, (width, height))
            mask = pygame.mask.from_surface(scaled)
            Stone._scaled_cache[cache_key] = (scaled, mask)
        self.image, self.mask = Stone._scaled_cache[cache_key]
        self.rect = self.image.get_rect()
        self.rect.topleft = location
        self.width = width
        self.height = height
        self.location = list(location)
        self.vector_x, self.vector_y = get_normalize_vector(location[0], location[1], destination[0], destination[1])
        self.multiple = 12

    def update(self, delta_time, player):
        time_step = delta_time * REFERENCE_FPS
        self.location[0] += self.vector_x * self.multiple * time_step
        self.location[1] += self.vector_y * self.multiple * time_step
        self.rect.topleft = (int(self.location[0]), int(self.location[1]))

        # Kill if it leaves the screen bounds.
        if self.rect.centerx < -self.width:
            self.kill()
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
        self.images_index = 0.0
        self.width = self.raw_image.get_width()
        self.rect = self.image.get_rect()
        self.rect.topleft = location
        self.location = list(location)
        self.hit_group = hit_group
    
    def update(self, delta_time, player, bananaHit_group):
        time_step = delta_time * REFERENCE_FPS
        if self.rect.x < -self.width:
            self.kill()
            return
            
        if self.is_colliding_with(player):
            rm = ResourceManager.get_instance()
            settings = rm.load_config("config/settings.json")["player"]
            player.hurt(settings["damage_taken"]["banana"])
            self.hit()
            return
        
        self.location[0] -= 5 * time_step
        self.rect.x = int(self.location[0])

        self.images_index += time_step
        if self.images_index >= 40:
            self.image = self.raw_image
            self.images_index = 0.0
        else:
            idx = min(int(self.images_index) // 5, len(self.roalingImages) - 1)
            self.image = self.roalingImages[idx]
    
    def hit(self):
        self.hit_group.add(BananaHit(self.rect.topleft))
        self.kill()

class Seed(Projectile):
    def __init__(self, location, vx, vy, angle, hit_group):
        super().__init__()
        rm = ResourceManager.get_instance()
        self.raw_image = rm.get_image("bigWhiteMonkey/shootAttack/seed/seed.png")
        
        self.image = pygame.transform.rotate(self.raw_image, angle)
        self.mask = pygame.mask.from_surface(self.image)
        self.width = self.raw_image.get_width()
        self.rect = self.image.get_rect()
        self.rect.midright = location
        self.location = list(self.rect.center)
        
        self.vector_x = vx
        self.vector_y = vy
        
        self.hit_group = hit_group
        
    def update(self, delta_time, player, seedHit_group):
        time_step = delta_time * REFERENCE_FPS
        # Check if the seed is out of bounds
        if self.rect.centerx < -self.width:
            self.kill()
            return
            
        if self.is_colliding_with(player):
            rm = ResourceManager.get_instance()
            settings = rm.load_config("config/settings.json")["player"]
            player.hurt(settings["damage_taken"]["seed"])
            self.hit()
            return
            
        self.location[0] += self.vector_x * time_step
        self.location[1] += self.vector_y * time_step
        self.rect.center = (int(self.location[0]), int(self.location[1]))

    def hit(self):
        self.hit_group.add(SeedHit(self.rect.center))
        self.kill()
