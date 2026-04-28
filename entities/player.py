import pygame
from function import REFERENCE_FPS, WHITE
from core.resource_manager import ResourceManager
from entities.base import Entity


class Player(Entity):
    def __init__(self, location_x, location_y):
        super().__init__()
        rm = ResourceManager.get_instance()
        cfg = rm.load_config("config/settings.json")["player"]

        # ── Sprite ──────────────────────────────────────────────
        self.raw_image   = rm.get_image("player/stand1_1.png")
        self.sleep_image = rm.get_image("player/sleep.png")
        self.ATKimages = [
            [rm.get_image("player//swingO1_0.png"), rm.get_image("player//swingO1_1.png"), rm.get_image("player//swingO1_2.png")],
            [rm.get_image("player//swingO2_0.png"), rm.get_image("player//swingO2_1.png"), rm.get_image("player//swingO2_2.png")],
            [rm.get_image("player//swingO1_0.png"), rm.get_image("player//swingO3_1.png"), rm.get_image("player//swingO3_2.png")]
        ]
        self.ATKseries_index = 0
        self.ATKseries_photo_index = 0.0
        self.isATK = False

        self.image = self.raw_image
        self.rect  = self.raw_image.get_rect()
        self.rect.topleft = (location_x, location_y)
        self.mask  = pygame.mask.from_surface(self.image)
        self.width  = self.raw_image.get_width()
        self.height = self.raw_image.get_height()

        # ── Sound ────────────────────────────────────────────────
        self.shoot_sound = rm.get_sound("player/attack/shoot.wav", 0.5)

        # ── Level / Stat system ──────────────────────────────────
        self.level     = 1
        self.exp       = 0
        self.max_level = cfg["max_level"]
        self._exp_to_level_up = cfg["exp_to_level_up"]
        self._recalc_stats()       # 計算初始 max_ap / max_mp / max_life
        self.life = self.max_life  # 初始化為滿血
        self.ap = float(self.max_ap)
        self.mp = float(self.max_mp)

        # ── Skill selection ──────────────────────────────────────
        self.active_skill = 1      # 當前選擇的技能（1~5）

        # ── Skill cooldowns (seconds remaining) ──────────────────
        self.skill_cooldowns = {3: 0.0, 4: 0.0, 5: 0.0}

        # ── Skill 4 – Rest ───────────────────────────────────────
        self.is_resting      = False
        self._rest_timer     = 0.0
        self._rest_duration  = cfg["skills"]["rest"]["duration"]
        self.pending_heal_amount = 0   # 供 game_page 讀取以顯示浮動文字

        # ── Font ─────────────────────────────────────────────────
        self.life_font = pygame.font.SysFont(None, 40)
        self._update_life_surface()

    # ────────────────────────────────────────────────────────────
    # Internal helpers
    # ────────────────────────────────────────────────────────────
    def _recalc_stats(self):
        """依等級重新計算最大屬性值上限（不修改當前 life）。"""
        rm  = ResourceManager.get_instance()
        cfg = rm.load_config("config/settings.json")["player"]
        lv  = self.level
        self.max_ap   = cfg["base_ap"] + lv * cfg["ap_per_level"]
        self.max_mp   = cfg["base_mp"] + lv * cfg["mp_per_level"]
        self.max_life = cfg["base_life"] + lv   # 僅計算上限，不直接設定 life

    def _update_life_surface(self):
        self.life_text_surface = self.life_font.render(
            f"Life: {self.life}", True, WHITE
        )

    # ────────────────────────────────────────────────────────────
    # Public API
    # ────────────────────────────────────────────────────────────
    def gain_exp(self, amount: int):
        """獲得經驗値，必要時升等。升等後維持當前生命値，僅回復滿 AP/MP。"""
        if self.level >= self.max_level:
            return
        self.exp += amount
        while self.exp >= self._exp_to_level_up and self.level < self.max_level:
            self.exp -= self._exp_to_level_up
            self.level += 1
            self._recalc_stats()                        # 更新上限
            self.life = min(self.life, self.max_life)   # 維持當前血量，超過新上限則 cap
            self.ap = float(self.max_ap)
            self.mp = float(self.max_mp)
            self._update_life_surface()

    def hurt(self, damage=1):
        """受傷；休息期間免疫。"""
        if self.is_resting:
            return
        super().hurt(damage)
        self._update_life_surface()

    # ── Skill: Pencil (1) ────────────────────────────────────────
    def attack(self):
        """鉛筆射擊，消耗 AP，播放動畫與音效。"""
        rm  = ResourceManager.get_instance()
        cfg = rm.load_config("config/settings.json")["player"]["skills"]["pencil"]
        cost = cfg["ap_cost"]
        if self.ap < cost:
            return False
        self.ap  -= cost
        self.isATK = True
        self.shoot_sound.play()
        return True

    # ── Skill: Book (2) ─────────────────────────────────────────
    def throw_book(self):
        """丟書，消耗 MP，使用 swing 動畫。"""
        rm  = ResourceManager.get_instance()
        cfg = rm.load_config("config/settings.json")["player"]["skills"]["book"]
        if self.level < cfg["unlock_level"] or self.mp < cfg["mp_cost"]:
            return False
        if self.isATK:
            return False
        self.mp   -= cfg["mp_cost"]
        self.isATK = True
        self.shoot_sound.play()
        return True

    # ── Skill: Desk (3) ─────────────────────────────────────────
    def use_desk(self):
        rm  = ResourceManager.get_instance()
        cfg = rm.load_config("config/settings.json")["player"]["skills"]["desk"]
        if (self.level < cfg["unlock_level"] or
                self.mp < cfg["mp_cost"] or
                self.skill_cooldowns[3] > 0):
            return False
        self.mp -= cfg["mp_cost"]
        self.skill_cooldowns[3] = cfg["cooldown"]
        return True

    # ── Skill: Rest (4) ─────────────────────────────────────────
    def use_rest(self):
        rm  = ResourceManager.get_instance()
        cfg = rm.load_config("config/settings.json")["player"]["skills"]["rest"]
        if (self.level < cfg["unlock_level"] or
                self.skill_cooldowns[4] > 0 or
                self.is_resting):
            return False
        self.is_resting  = True
        self._rest_timer = self._rest_duration
        self.skill_cooldowns[4] = cfg["cooldown"]
        return True

    # ── Skill: Motorcycle (5) ───────────────────────────────────
    def use_motorcycle(self):
        rm  = ResourceManager.get_instance()
        cfg = rm.load_config("config/settings.json")["player"]["skills"]["motorcycle"]
        if (self.level < cfg["unlock_level"] or
                self.skill_cooldowns[5] > 0):
            return False
        ap_cost = self.max_ap * cfg["ap_cost_ratio"]
        mp_cost = self.max_mp * cfg["mp_cost_ratio"]
        if self.ap < ap_cost or self.mp < mp_cost:
            return False
        self.ap -= ap_cost
        self.mp -= mp_cost
        self.skill_cooldowns[5] = cfg["cooldown"]
        rm.get_sound("player/skill_icon/motorcycle.wav", 0.7).play()
        return True

    # ────────────────────────────────────────────────────────────
    # Update
    # ────────────────────────────────────────────────────────────
    def update(self, delta_time):
        time_step = delta_time * REFERENCE_FPS
        rm  = ResourceManager.get_instance()
        cfg = rm.load_config("config/settings.json")["player"]

        # ── AP / MP 自然回復 ──────────────────────────────────
        ap_regen = (cfg["ap_regen_base"] + self.level / 30.0) * time_step / REFERENCE_FPS
        mp_regen = (cfg["mp_regen_base"] + self.level / 45.0) * time_step / REFERENCE_FPS
        self.ap = min(self.ap + ap_regen * REFERENCE_FPS, float(self.max_ap))
        self.mp = min(self.mp + mp_regen * REFERENCE_FPS, float(self.max_mp))

        # ── 技能冷卻倒計時 ───────────────────────────────────
        for k in self.skill_cooldowns:
            if self.skill_cooldowns[k] > 0:
                self.skill_cooldowns[k] = max(0.0, self.skill_cooldowns[k] - delta_time)

        # ── 休息狀態 ─────────────────────────────────────────
        if self.is_resting:
            self._rest_timer -= delta_time
            self.image = self.sleep_image
            if self._rest_timer <= 0:
                self.is_resting = False
                heal = cfg["skills"]["rest"]["heal_base"] + self.level
                self.life = min(self.life + heal, self.max_life)
                self._update_life_surface()
                self.image = self.raw_image
                self.pending_heal_amount = heal   # 觸發浮動文字
            return

        # ── 攻擊動畫 ─────────────────────────────────────────
        if self.isATK:
            img_idx = min(int(self.ATKseries_photo_index) // 11, 2)
            self.image = self.ATKimages[self.ATKseries_index][img_idx]

            ATKSERIES_FINAL_INDEX       = 2
            ATKSERIES_PHOTO_FINAL_INDEX = 32

            if self.ATKseries_photo_index >= ATKSERIES_PHOTO_FINAL_INDEX:
                self.ATKseries_photo_index = 0.0
                self.isATK = False
                if self.ATKseries_index == ATKSERIES_FINAL_INDEX:
                    self.ATKseries_index = 0
                else:
                    self.ATKseries_index += 1
            else:
                self.ATKseries_photo_index += time_step
        else:
            self.image = self.raw_image


# ────────────────────────────────────────────────────────────────────
# HUD Components
# ────────────────────────────────────────────────────────────────────

class PlayerHUD:
    """
    統一管理玩家的所有 HUD 繪製：
      - 頂部左側：生命值條 / AP 條 / MP 條 / 等級 / EXP
      - 底部中央：技能 icon 欄（5 格，含冷卻遮罩與解鎖灰化）
    """

    SKILL_ICON_SIZE  = 56          # icon 顯示大小
    SKILL_ICON_GAP   = 8           # icon 間距
    BAR_WIDTH        = 150
    BAR_HEIGHT       = 14
    ICON_PATHS = [
        "player/skill_icon/pencil.png",
        "player/skill_icon/book.png",
        "player/skill_icon/desk.png",
        "player/skill_icon/rest.png",
        "player/skill_icon/motorcycle.png",
    ]
    UNLOCK_LEVELS = [1, 3, 6, 10, 15]
    COOLDOWN_SKILL_IDX = {3: 2, 4: 3, 5: 4}   # skill_id → icon index

    def __init__(self, screen_w: int, screen_h: int):
        rm = ResourceManager.get_instance()
        sz = self.SKILL_ICON_SIZE

        # ── Load & scale icons ───────────────────────────────
        self._icons      = [pygame.transform.scale(rm.get_image(p), (sz, sz))
                            for p in self.ICON_PATHS]
        # greyed-out version（Alpha 混合）
        self._icons_grey = []
        for icon in self._icons:
            grey = icon.copy()
            grey.fill((80, 80, 80, 180), special_flags=pygame.BLEND_RGBA_MULT)
            self._icons_grey.append(grey)

        # ── Bottom bar position ──────────────────────────────
        total_w  = 5 * sz + 4 * self.SKILL_ICON_GAP
        self._bar_x = (screen_w - total_w) // 2
        self._bar_y = screen_h - sz - 12

        # ── Font ─────────────────────────────────────────────
        self._font_sm  = pygame.font.SysFont(None, 22)
        self._font_cd  = pygame.font.SysFont(None, 26)
        self._font_lv  = pygame.font.SysFont(None, 28)

        # ── Semi-transparent surfaces ─────────────────────────
        self._cd_overlay = pygame.Surface((sz, sz), pygame.SRCALPHA)
        self._cd_overlay.fill((0, 0, 0, 160))

        self._screen_h = screen_h
        self._screen_w = screen_w

    # ─── Drawing helpers ────────────────────────────────────────
    @staticmethod
    def _draw_bar(surface, x, y, w, h, ratio, fill_color, bg_color=(60, 60, 60)):
        pygame.draw.rect(surface, bg_color, (x, y, w, h), border_radius=4)
        fill_w = max(0, int(w * ratio))
        if fill_w:
            pygame.draw.rect(surface, fill_color, (x, y, fill_w, h), border_radius=4)
        pygame.draw.rect(surface, (200, 200, 200), (x, y, w, h), 1, border_radius=4)

    def draw(self, surface, player):
        rm  = ResourceManager.get_instance()
        cfg = rm.load_config("config/settings.json")["player"]
        lv  = player.level

        # ════════════════════════════════════════════════════════
        # TOP-LEFT HUD
        # ════════════════════════════════════════════════════════
        sx, sy = 18, 18
        bw, bh = self.BAR_WIDTH, self.BAR_HEIGHT
        gap = 6

        max_life = player.max_life
        self._draw_bar(surface, sx, sy,      bw, bh, player.life / max_life,    (220, 60, 60))
        self._draw_bar(surface, sx, sy+bh+gap, bw, bh, player.ap  / player.max_ap,  (240, 200, 40))
        self._draw_bar(surface, sx, sy+(bh+gap)*2, bw, bh, player.mp / player.max_mp,  (60, 150, 240))

        # Labels
        hp_txt = self._font_sm.render(f"HP {player.life}/{max_life}", True, (255,255,255))
        ap_txt = self._font_sm.render(f"AP {int(player.ap)}/{player.max_ap}", True, (255,255,255))
        mp_txt = self._font_sm.render(f"MP {int(player.mp)}/{player.max_mp}", True, (255,255,255))
        surface.blit(hp_txt, (sx + bw + 6, sy - 1))
        surface.blit(ap_txt, (sx + bw + 6, sy + bh + gap - 1))
        surface.blit(mp_txt, (sx + bw + 6, sy + (bh+gap)*2 - 1))

        # Level & EXP
        exp_needed = cfg["exp_to_level_up"]
        lv_txt = self._font_lv.render(f"Lv.{lv}", True, (255, 230, 100))
        surface.blit(lv_txt, (sx, sy + (bh+gap)*3 + 2))
        exp_bar_y = sy + (bh+gap)*3 + 26
        self._draw_bar(surface, sx, exp_bar_y, bw, 8,
                       min(player.exp / exp_needed, 1.0), (100, 230, 100))
        exp_txt = self._font_sm.render(f"EXP {player.exp}/{exp_needed}", True, (180,255,180))
        surface.blit(exp_txt, (sx + bw + 6, exp_bar_y - 1))

        # ════════════════════════════════════════════════════════
        # BOTTOM SKILL BAR
        # ════════════════════════════════════════════════════════
        sz   = self.SKILL_ICON_SIZE
        gap2 = self.SKILL_ICON_GAP
        bx   = self._bar_x
        by   = self._bar_y

        # 技能解鎖等級映射
        unlock = self.UNLOCK_LEVELS

        for i in range(5):
            ix = bx + i * (sz + gap2)
            skill_num = i + 1         # 1-based

            # 對應冷卻（只有 3、4、5 有冷卻）
            cd_left = player.skill_cooldowns.get(skill_num, 0.0)
            cd_max  = {3: cfg["skills"]["desk"]["cooldown"],
                       4: cfg["skills"]["rest"]["cooldown"],
                       5: cfg["skills"]["motorcycle"]["cooldown"]}.get(skill_num, 0.0)

            is_unlocked = lv >= unlock[i]

            # ── Icon 背景框 ──
            frame_color = (255, 220, 80) if player.active_skill == skill_num else (80, 80, 80)
            pygame.draw.rect(surface, frame_color, (ix - 3, by - 3, sz + 6, sz + 6), border_radius=6)

            # ── Icon 本體 ──
            if is_unlocked:
                surface.blit(self._icons[i], (ix, by))
            else:
                surface.blit(self._icons_grey[i], (ix, by))

            # ── 冷卻遮罩 ──
            if cd_left > 0 and cd_max > 0:
                surface.blit(self._cd_overlay, (ix, by))
                cd_txt = self._font_cd.render(f"{cd_left:.0f}", True, (255, 255, 255))
                ctr    = cd_txt.get_rect(center=(ix + sz // 2, by + sz // 2))
                surface.blit(cd_txt, ctr)

            # ── 技能編號標籤 ──
            num_txt = self._font_sm.render(str(skill_num), True, (200, 200, 200))
            surface.blit(num_txt, (ix + 2, by + sz - 16))

            # ── 未解鎖等級提示 ──
            if not is_unlocked:
                lk_txt = self._font_sm.render(f"Lv{unlock[i]}", True, (255, 200, 80))
                lk_rect = lk_txt.get_rect(center=(ix + sz // 2, by + sz // 2))
                surface.blit(lk_txt, lk_rect)


# ────────────────────────────────────────────────────────────────────
# Legacy AP bar (kept for backward compat, can be removed later)
# ────────────────────────────────────────────────────────────────────
class AP(pygame.sprite.Sprite):
    def __init__(self, location) -> None:
        super().__init__()
        rm = ResourceManager.get_instance()
        raw_image = rm.get_image("player//APline.png")
        self.raw_image = pygame.transform.scale(raw_image, (100, 20))
        self.image = self.raw_image
        self.rect  = self.image.get_rect()
        self.rect.topleft = location
        self.width  = float(self.image.get_width())
        self.height = self.image.get_height()
        self.isAPchange = False

    def update(self, delta_time, player_AP) -> None:
        if 0 < player_AP < 100:
            APwidth = max(1, min(int(player_AP), 100))
            self.image = self.raw_image.subsurface((0, 0, APwidth, self.height))
