import pygame
from function import REFERENCE_FPS
from core.resource_manager import ResourceManager


class DeskObstacle(pygame.sprite.Sprite):
    """
    課桌椅障礙物：
    - 從畫面上方落下到玩家正前方
    - 落下時對範圍內的猴子造成傷害
    - 靜態後擁有 HP，每秒衰減，HP 歸零消失
    - 阻擋子彈（stone, banana, seed）
    - 近戰攻擊（monkey, angel_monkey）優先攻擊此障礙物
    """

    WIDTH  = 80
    HEIGHT = 50
    FALL_SPEED = 18.0    # 每基準幀下落像素

    def __init__(self, x: int, ground_y: int):
        """
        x         : 障礙物中心 x 座標
        ground_y  : 落地後的 top y 座標（玩家前方地面位置）
        """
        super().__init__()
        rm  = ResourceManager.get_instance()
        cfg = rm.load_config("config/settings.json")["player"]["skills"]["desk"]

        self.hp            = float(cfg["hp"])
        self.hp_decay      = float(cfg["hp_decay_per_sec"])
        self.max_hp        = float(cfg["hp"])
        self._ground_y     = ground_y
        self._is_falling   = True

        # ── 建立佔位矩形 surface（黃棕色，代替真實 sprite）──
        self.image = pygame.Surface((self.WIDTH, self.HEIGHT), pygame.SRCALPHA)
        self._redraw()

        self.rect = self.image.get_rect()
        self.rect.centerx = x
        self.rect.top      = -self.HEIGHT        # 從畫面上方開始落下

        self.mask = pygame.mask.from_surface(self.image)

        # ── 字型（顯示 HP）──
        self._font = pygame.font.SysFont(None, 20)

    # ─────────────────────────────────────────────────────────
    def _redraw(self):
        """重繪障礙物矩形（HP 條）。"""
        self.image.fill((0, 0, 0, 0))
        # 桌子本體
        pygame.draw.rect(self.image, (160, 110, 40),
                         (0, 0, self.WIDTH, self.HEIGHT), border_radius=4)
        pygame.draw.rect(self.image, (200, 150, 60),
                         (0, 0, self.WIDTH, self.HEIGHT), 2, border_radius=4)
        # HP 條（紅色）
        hp_ratio = max(0.0, self.hp / self.max_hp)
        hp_bar_w = int((self.WIDTH - 6) * hp_ratio)
        pygame.draw.rect(self.image, (80, 20, 20), (3, 3, self.WIDTH - 6, 7), border_radius=2)
        if hp_bar_w > 0:
            pygame.draw.rect(self.image, (220, 50, 50), (3, 3, hp_bar_w, 7), border_radius=2)

    # ─────────────────────────────────────────────────────────
    def update(self, delta_time, enemy_groups_to_damage, damage: int):
        """
        delta_time         : 幀間隔秒數
        enemy_groups_to_damage : 落下時造成傷害的群組列表（第一幀著地時）
        damage             : 落下傷害
        """
        time_step = delta_time * REFERENCE_FPS
        if self._is_falling:
            self.rect.top += int(self.FALL_SPEED * time_step)
            if self.rect.top >= self._ground_y:
                rm = ResourceManager.get_instance()

                self.rect.top    = self._ground_y
                self._is_falling = False
                
                # 落地音效
                rm.get_sound("player/skill_icon/desk_fall.wav", 0.7).play()
                # 落地時對範圍內敵人造成傷害
                for grp in enemy_groups_to_damage:
                    hits = pygame.sprite.spritecollide(self, grp, False)
                    for enemy in hits:
                        enemy.hurt(damage)
                self.mask = pygame.mask.from_surface(self.image)
        else:
            # 每秒 HP 衰減
            self.hp -= self.hp_decay * delta_time
            if self.hp <= 0:
                self.kill()
                return
            self._redraw()

    def hurt(self, damage: int = 1):
        """供近戰攻擊呼叫（monkey / angel_monkey 優先打障礙物）。"""
        self.hp -= damage
        if self.hp <= 0:
            self.kill()

    def hit(self):
        """供子彈碰撞呼叫（子彈被消除，障礙物不受傷）。"""
        pass   # 阻擋子彈但不掉 HP（僅作為碰撞面）
