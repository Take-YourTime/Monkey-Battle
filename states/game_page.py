import pygame
import random
from states.base import StateBase
from function import BLACK, VIRTUAL_HEIGHT, VIRTUAL_WIDTH

from entities.player import Player, PlayerHUD
from entities.projectiles import Pencil, Book, Motorcycle
from entities.obstacles import DeskObstacle
from entities.magician import Magician
from entities.monkey_king import MonkeyKing
from entities.monkey import Monkey
from entities.angel_monkey import AngelMonkey
from entities.big_white_monkey import BigWhiteMonkey
from core.resource_manager import ResourceManager, resource_path

LEFT = 1  # left mouse button


class GameState(StateBase):
    def __init__(self, engine):
        super().__init__(engine)

    def enter(self):
        # load BGM
        rm = ResourceManager.get_instance()
        pygame.mixer.music.load(resource_path("BGM/Motivation.mp3"))
        pygame.mixer.music.set_volume(0.4 * rm.global_volume)

        # load raw background
        self.background = rm.get_image("school.png", alpha=False)
        self.player = Player(70, self.engine.virtual_height - 273)

        # ── HUD ──────────────────────────────────────────────────
        self.hud = PlayerHUD(self.engine.virtual_width, self.engine.virtual_height)

        # ── Sprite groups ─────────────────────────────────────────
        # Player skills
        self.pencil_group      = pygame.sprite.Group()
        self.pencilFolded_group = pygame.sprite.Group()
        self.book_group        = pygame.sprite.Group()
        self.bookHit_group     = pygame.sprite.Group()
        self.desk_group        = pygame.sprite.Group()
        self.motorcycle_group  = pygame.sprite.Group()
        self.explosion_group   = pygame.sprite.Group()
        self.heal_text_group   = pygame.sprite.Group()  # 休息回血浮動文字

        # Monsters
        self.magician_group    = pygame.sprite.Group()
        self.stone_group       = pygame.sprite.Group()

        self.monkeyKing_group  = pygame.sprite.Group()
        self.banana_group      = pygame.sprite.Group()
        self.bananaHit_group   = pygame.sprite.Group()

        self.bigWhiteMonkey_group = pygame.sprite.Group()
        self.seed_group        = pygame.sprite.Group()
        self.seedHit_group     = pygame.sprite.Group()
        self.dust_group        = pygame.sprite.Group()

        self.monkey_group      = pygame.sprite.Group()
        self.angelMonkey_group = pygame.sprite.Group()
        self.monkey_BananaHit_group = pygame.sprite.Group()
        self.moneyShowUpSound  = rm.get_sound("monkey\\show_up.wav", 0.35)

        # ── Wave config ───────────────────────────────────────────
        self.wave  = rm.load_config("config/waves.json")["waves"]
        self.index = 0

        # ── Stats ─────────────────────────────────────────────────
        self.elapsed_time      = 0.0
        self.kill_count        = 0
        self._prev_enemy_count = 0

        # ── Death overlay ─────────────────────────────────────────
        self._death_overlay_alpha  = 0.0
        self._death_overlay_active = False
        self._death_waiting_click  = False
        self._overlay_surface = pygame.Surface(
            (self.engine.virtual_width, self.engine.virtual_height), pygame.SRCALPHA
        )
        self._hint_font = pygame.font.Font(
            resource_path("menu/Wordefta.otf"), 36
        )

        # game start
        self.spawn_wave()
        pygame.mixer.music.play(-1)

    # ─────────────────────────────────────────────────────────────
    def spawn_wave(self):
        self.moneyShowUpSound.play()
        for _ in range(self.wave[self.index][0]):
            x = random.randint(self.engine.virtual_width, self.engine.virtual_width + 150)
            self.monkey_group.add(Monkey(x, self.engine.virtual_height - 176))
        for _ in range(self.wave[self.index][1]):
            self.magician_group.add(Magician(100, 100))
        for _ in range(self.wave[self.index][2]):
            x = random.randint(self.engine.virtual_width, self.engine.virtual_width + 150)
            self.monkeyKing_group.add(MonkeyKing(x, self.engine.virtual_height - 373))
        for _ in range(self.wave[self.index][3]):
            x = random.randint(self.engine.virtual_width, self.engine.virtual_width + 150)
            self.angelMonkey_group.add(AngelMonkey(x, self.engine.virtual_height - 185))
        for _ in range(self.wave[self.index][4]):
            x = random.randint(self.engine.virtual_width, self.engine.virtual_width + 150)
            self.bigWhiteMonkey_group.add(BigWhiteMonkey(x, self.engine.virtual_height - 191))

    # ─────────────────────────────────────────────────────────────
    def exit(self):
        pygame.mixer.music.fadeout(500)
        self.player.kill()

        groups_to_clear = [
            self.pencil_group, self.pencilFolded_group,
            self.book_group, self.bookHit_group,
            self.desk_group, self.motorcycle_group, self.explosion_group,
            self.heal_text_group,
            self.magician_group, self.stone_group,
            self.monkeyKing_group, self.banana_group, self.bananaHit_group,
            self.bigWhiteMonkey_group, self.seed_group, self.seedHit_group,
            self.dust_group, self.monkey_group, self.angelMonkey_group,
            self.monkey_BananaHit_group,
        ]
        for grp in groups_to_clear:
            for sprite in grp:
                sprite.kill()
            grp.empty()

    # ─────────────────────────────────────────────────────────────
    def handle_events(self, events):
        rm  = ResourceManager.get_instance()
        cfg = rm.load_config("config/settings.json")["player"]

        for event in events:
            # ── 切換技能（鍵盤 1~5）──
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_1:
                    self.player.active_skill = 1
                elif event.key == pygame.K_2:
                    self.player.active_skill = 2
                elif event.key == pygame.K_3:
                    self.player.active_skill = 3
                elif event.key == pygame.K_4:
                    self.player.active_skill = 4
                elif event.key == pygame.K_5:
                    self.player.active_skill = 5

            # ── 左鍵施放當前技能 ──
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == LEFT:
                # 死亡黑幕完成後點擊切換
                if self._death_waiting_click:
                    pygame.mixer.music.fadeout(500)
                    self.engine.state_machine.change_state("END")
                    return

                # 休息期間無法施放任何技能
                if self.player.is_resting:
                    return

                skill = self.player.active_skill
                mouse_pos = self.engine.get_mouse_pos()
                player_center = (
                    self.player.rect.centerx + 3,
                    self.player.rect.centery - 10,
                )

                # ── 技能 1：鉛筆射擊 ──
                if skill == 1:
                    if self.player.ap >= cfg["skills"]["pencil"]["ap_cost"]:
                        self.player.attack()
                        self.pencil_group.add(
                            Pencil(45, 5, player_center, mouse_pos)
                        )

                # ── 技能 2：丟書 ──
                elif skill == 2:
                    if self.player.throw_book():
                        self.book_group.add(Book(player_center, mouse_pos))

                # ── 技能 3：課桌椅障礙物 ──
                elif skill == 3:
                    if self.player.use_desk():
                        desk_x    = self.player.rect.right + 60
                        ground_y  = self.engine.virtual_height - 273  # 與玩家同高
                        self.desk_group.add(
                            DeskObstacle(desk_x, ground_y)
                        )

                # ── 技能 4：休息時刻 ──
                elif skill == 4:
                    self.player.use_rest()

                # ── 技能 5：機車衝擊 ──
                elif skill == 5:
                    if self.player.use_motorcycle():
                        moto_start = (
                            self.player.rect.left,
                            self.player.rect.centery-17,
                        )
                        self.motorcycle_group.add(Motorcycle(moto_start))

    # ─────────────────────────────────────────────────────────────
    def _total_enemies(self):
        return (
            len(self.magician_group) + len(self.monkey_group) +
            len(self.monkeyKing_group) + len(self.angelMonkey_group) +
            len(self.bigWhiteMonkey_group)
        )

    def _go_to_end(self, is_win):
        self.engine.end_result = {
            "is_win":      is_win,
            "kill_count":  self.kill_count,
            "elapsed_time": self.elapsed_time,
        }
        if is_win:
            pygame.mixer.music.fadeout(500)
            self.engine.state_machine.change_state("END")
        else:
            self._death_overlay_active = True

    # ─────────────────────────────────────────────────────────────
    def update(self, delta_time):
        # ── 黑幕淡入中 ──
        if self._death_overlay_active or self._death_waiting_click:
            if self._death_overlay_active:
                self._death_overlay_alpha = min(
                    180.0, self._death_overlay_alpha + 180 * delta_time * 1.5
                )
                if self._death_overlay_alpha >= 180.0:
                    self._death_overlay_active = False
                    self._death_waiting_click  = True
            return

        self.elapsed_time += delta_time

        # ── 擊殺計數 & 給玩家經驗 ──────────────────────────────
        current_count = self._total_enemies()
        killed_this_frame = max(0, self._prev_enemy_count - current_count)
        if killed_this_frame > 0:
            self.kill_count += killed_this_frame
            rm  = ResourceManager.get_instance()
            cfg = rm.load_config("config/settings.json")["player"]
            self.player.gain_exp(killed_this_frame * cfg["exp_per_kill"])

        # ── 玩家死亡 ──────────────────────────────────────────
        if self.player.life <= 0:
            self._go_to_end(is_win=False)
            return

        # ── 波次清空 → 下一波或勝利 ──────────────────────────
        if self._total_enemies() == 0:
            self.index += 1
            if self.index == len(self.wave):
                self._go_to_end(is_win=True)
                return
            else:
                self.spawn_wave()

        self._prev_enemy_count = self._total_enemies()

        # ────────────────────────────────────────────────────────
        # 決定近戰目標：如果有課桌椅障礙物，猴子優先攻擊它
        # ────────────────────────────────────────────────────────
        # 近戰猴子需要知道是否有障礙物在場，讓其攻擊障礙物
        # 用特化的 update 傳參方式處理

        # ── 更新玩家技能拋射物 ──────────────────────────────
        self.pencil_group.update(
            delta_time,
            [self.magician_group, self.monkeyKing_group,
             self.monkey_group, self.angelMonkey_group, self.bigWhiteMonkey_group],
            [self.stone_group, self.banana_group, self.seed_group],  # 鉛筆不被課桌椅阻擋
            self.pencilFolded_group,
        )
        self.pencilFolded_group.update(delta_time)

        # 丟書：消除敵方子彈，對所有敵人造成傷害（MonkeyKing 無 stun 方法，自動免疫重擊）
        _book_enemy_groups  = [self.monkey_group, self.angelMonkey_group,
                                self.magician_group, self.bigWhiteMonkey_group,
                                self.monkeyKing_group]
        _book_bullet_groups = [self.stone_group, self.banana_group, self.seed_group]
        for book in list(self.book_group):
            book.update(delta_time, _book_enemy_groups, _book_bullet_groups, self.bookHit_group)

        self.bookHit_group.update(delta_time)

        # 課桌椅：落下時對所有敵人造成傷害
        cfg_desk = ResourceManager.get_instance().load_config(
            "config/settings.json"
        )["player"]["skills"]["desk"]
        for desk in self.desk_group:
            desk.update(
                delta_time,
                [self.monkey_group, self.angelMonkey_group,
                 self.monkeyKing_group, self.bigWhiteMonkey_group,
                 self.magician_group],
                cfg_desk["damage"],
            )

        # 課桌椅阻擋子彈（石頭、香蕉、種子）
        for desk in self.desk_group:
            for proj_grp in [self.stone_group, self.banana_group, self.seed_group]:
                hits = pygame.sprite.spritecollide(desk, proj_grp, False)
                for proj in hits:
                    proj.kill()      # 子彈消除
                    desk.hit()       # 障礙物不受傷（hit() 為空）

        # 機車衝擊：對所有敵人有效
        _moto_enemy_groups = [
            self.monkey_group, self.angelMonkey_group,
            self.monkeyKing_group, self.bigWhiteMonkey_group,
            self.magician_group,
        ]
        for moto in list(self.motorcycle_group):
            moto.update(delta_time, _moto_enemy_groups, self.explosion_group)
        self.explosion_group.update(delta_time)

        # ── 更新怪物 ──────────────────────────────────────────
        for magician in self.magician_group:
            magician.update(delta_time, self.stone_group)

        self.monkeyKing_group.update(delta_time, self.banana_group, self.bananaHit_group)

        # 近戰猴子：若有障礙物優先攻擊障礙物
        for monkey in self.monkey_group:
            if len(self.desk_group) > 0:
                # 簡化：讓猴子的攻擊落點導向最近的障礙物
                desk_list = list(self.desk_group)
                nearest   = min(desk_list, key=lambda d: abs(d.rect.centerx - monkey.rect.centerx))
                # 若猴子已停下且不在攻擊，讓其攻擊障礙物
                if not monkey.keepWalking and not monkey.isATK and monkey.energy >= 300:
                    nearest.hurt(1)
                    monkey.energy = 0.0
                monkey.update(delta_time, self.player, self.monkey_BananaHit_group)
            else:
                monkey.update(delta_time, self.player, self.monkey_BananaHit_group)

        for angel in self.angelMonkey_group:
            if len(self.desk_group) > 0:
                desk_list = list(self.desk_group)
                nearest   = min(desk_list, key=lambda d: abs(d.rect.centerx - angel.rect.centerx))
                if not angel.keepWalking and not angel.isATK and angel.energy >= 300:
                    nearest.hurt(1)
                    angel.energy = 0.0
                angel.update(delta_time, self.player, self.monkey_BananaHit_group)
            else:
                angel.update(delta_time, self.player, self.monkey_BananaHit_group)

        self.bigWhiteMonkey_group.update(
            delta_time, self.player,
            self.seed_group, self.seedHit_group, self.dust_group,
        )

        # ── 更新玩家 ──────────────────────────────────────────
        self.player.update(delta_time)

        # ── 更新怪物攻擊拋射物 ──────────────────────────────
        self.stone_group.update(delta_time, self.player)
        self.banana_group.update(delta_time, self.player, self.bananaHit_group)
        self.seed_group.update(delta_time, self.player, self.seedHit_group)
        self.bananaHit_group.update(delta_time)
        self.seedHit_group.update(delta_time)
        self.dust_group.update(delta_time)
        self.monkey_BananaHit_group.update(delta_time)

        # ── 休息回血浮動文字 ──────────────────────────────
        if self.player.pending_heal_amount > 0:
            from effects.animations import HealText
            self.heal_text_group.add(
                HealText(self.player.rect.midtop, self.player.pending_heal_amount)
            )
            self.player.pending_heal_amount = 0   # 清除，避免重複觸發
        self.heal_text_group.update(delta_time)

    # ─────────────────────────────────────────────────────────────
    def draw(self, surface):
        surface.fill(BLACK)
        surface.blit(self.background, (0, 0))

        # 課桌椅障礙物（在怪物之後、玩家之前）
        self.desk_group.draw(surface)

        self.pencil_group.draw(surface)
        self.book_group.draw(surface)
        self.monkeyKing_group.draw(surface)
        self.bigWhiteMonkey_group.draw(surface)
        self.monkey_group.draw(surface)
        self.angelMonkey_group.draw(surface)
        self.magician_group.draw(surface)
        self.banana_group.draw(surface)
        self.stone_group.draw(surface)
        self.seed_group.draw(surface)

        # 機車
        self.motorcycle_group.draw(surface)

        # 玩家
        surface.blit(self.player.image, self.player.rect.topleft)

        # 命中特效
        self.monkey_BananaHit_group.draw(surface)
        self.bananaHit_group.draw(surface)
        self.seedHit_group.draw(surface)
        self.dust_group.draw(surface)
        self.pencilFolded_group.draw(surface)
        self.bookHit_group.draw(surface)
        self.explosion_group.draw(surface)

        # ── HUD ──────────────────────────────────────────────
        self.hud.draw(surface, self.player)

        # 休息浮動文字（絕對 HUD 之上）
        self.heal_text_group.draw(surface)

        # ── 死亡黑幕 ──────────────────────────────────────────
        if self._death_overlay_active or self._death_waiting_click:
            vw = self.engine.virtual_width
            vh = self.engine.virtual_height
            self._overlay_surface.fill((0, 0, 0, int(self._death_overlay_alpha)))
            surface.blit(self._overlay_surface, (0, 0))
            if self._death_waiting_click:
                hint_surf = self._hint_font.render("Click to continue...", True, (220, 220, 220))
                hint_rect = hint_surf.get_rect(center=(vw // 2, vh // 2))
                surface.blit(hint_surf, hint_rect)
