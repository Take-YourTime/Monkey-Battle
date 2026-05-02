import pygame
from function import REFERENCE_FPS
from core.resource_manager import ResourceManager


class DeskObstacle(pygame.sprite.Sprite):
    """
    課桌椅障礙物：
    - 在玩家前方依序播放 desk_drop1~6 動畫（圖片本身已含落下視覺效果）
    - 動畫結束後維持 desk_drop6 靜止狀態（疊加 HP 條）
    - 靜態後 HP 受子彈/近戰攻擊而減少，歸零後消失
    - 近戰怪物優先攻擊此障礙物
    """

    # 動畫速度（每秒播放幾張）
    ANIM_FPS    = 10
    # HP 條高度
    HP_BAR_H    = 10

    def __init__(self, location: tuple):
        """
        location: 障礙物 rect 的目標位置
        """
        super().__init__()
        rm  = ResourceManager.get_instance()
        cfg = rm.load_config("config/settings.json")["player"]["skills"]["desk"]

        self.hp       = float(cfg["hp"])
        self.hp_decay = float(cfg["hp_decay_per_sec"])
        self.max_hp   = float(cfg["hp"])

        self._location = location
        self._anim_index = 0.0   # 動畫幀計數（float，透過 ANIM_FPS 推進）
        self._anim_done  = False  # 動畫是否播放完畢

        # ── 載入 6 張圖 ────────
        self._frames = []
        for i in range(1, 7):
            raw = rm.get_image(f"player/attack/desk_drop/desk_drop{i}.png")
            self._frames.append(raw)

        # ── 初始 image / rect（第 1 幀，固定位置）────────────────
        self.image = self._frames[0]
        self.rect  = self.image.get_rect()
        self.rect.centerx = self._location[0]
        self.rect.bottom = self._location[1]
        self.mask = pygame.mask.from_surface(self.image)

        rm.get_sound("player/sound/desk_drop.wav", 0.7).play()

    # ─────────────────────────────────────────────────────────
    def _make_static_image(self) -> pygame.Surface:
        """複製 frame6（索引 5）並在底部疊加 HP 條。"""
        surf = self._frames[5].copy()
        w, h = surf.get_size()
        bar_y = h - self.HP_BAR_H - 4
        bar_w = w - 8
        # 背景（深色）
        pygame.draw.rect(surf, (60, 20, 20),
                         (4, bar_y, bar_w, self.HP_BAR_H), border_radius=3)
        # 前景（依血量 紅→綠）
        hp_ratio  = max(0.0, self.hp / self.max_hp)
        fill_w    = max(0, int(bar_w * hp_ratio))
        r = int(220 * (1 - hp_ratio) + 50  * hp_ratio)
        g = int(50  * (1 - hp_ratio) + 210 * hp_ratio)
        if fill_w > 0:
            pygame.draw.rect(surf, (r, g, 50),
                             (4, bar_y, fill_w, self.HP_BAR_H), border_radius=3)
        return surf

    # ─────────────────────────────────────────────────────────
    def _apply_image(self, new_image: pygame.Surface):
        """更新 image 並保持 bottom/centerx 位置不變。"""
        cx = self.rect.centerx
        bt = self.rect.bottom
        self.image = new_image
        self.rect  = self.image.get_rect()
        self.rect.centerx = cx
        self.rect.bottom  = bt

    # ─────────────────────────────────────────────────────────
    def update(self, delta_time, enemy_groups_to_damage, damage: int):
        """
        delta_time             : 幀間隔秒數
        enemy_groups_to_damage : 動畫結束瞬間造成傷害的群組列表
        damage                 : 落下傷害值
        """
        rm = ResourceManager.get_instance()
        n  = len(self._frames)   # = 6

        if not self._anim_done:
            # ── 動畫播放中 ──────────────────────────────────────
            self._anim_index += delta_time * self.ANIM_FPS
            img_idx = int(self._anim_index)

            if img_idx >= n:
                # ── 動畫播放完畢，切換為靜止狀態 ──────────────
                self._anim_done = True

                # 靜止圖（含 HP 條）
                self._apply_image(self._make_static_image())
                self.mask = pygame.mask.from_surface(self.image)

                # 對範圍內敵人造成傷害
                for grp in enemy_groups_to_damage:
                    hits = pygame.sprite.spritecollide(self, grp, False)
                    for enemy in hits:
                        enemy.hurt(damage)
            elif img_idx == 1:
                self.image = self._frames[img_idx]
            else:
                # ── 切換當前動畫幀 ──────────────────────────────
                self.image = self._frames[img_idx]
        else:
            # ── 靜止狀態：HP 每秒衰減 ──────────────────────────
            self.hp -= self.hp_decay * delta_time
            if self.hp <= 0:
                self.kill()
                return
            # 重繪 HP 條
            self._apply_image(self._make_static_image())

    # ─────────────────────────────────────────────────────────
    def hurt(self, damage: int = 1):
        """供近戰攻擊或子彈命中呼叫，扣除 HP。"""
        self.hp -= damage
        if self.hp <= 0:
            self.kill()

    def hit(self):
        """子彈命中時呼叫（子彈在 game_page 中已被消除）：扣 1 HP。"""
        self.hurt(1)
