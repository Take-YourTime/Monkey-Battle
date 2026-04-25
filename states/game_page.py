import pygame
import random
from states.base import StateBase
from function import BLACK

from entities.player import Player, AP
from entities.projectiles import Pencil
from entities.magician import Magician
from entities.monkey_king import MonkeyKing
from entities.monkey import Monkey
from entities.angel_monkey import AngelMonkey
from entities.big_white_monkey import BigWhiteMonkey
from core.resource_manager import ResourceManager, resource_path

LEFT = 1 # left mouse button

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
        self.player = Player(70, self.engine.virtual_height-273)
        self.playerAP = AP((100, 200))

        # sprites group
        self.pencil_group = pygame.sprite.Group()
        self.pencilFolded_group = pygame.sprite.Group()

        self.magician_group = pygame.sprite.Group()
        self.stone_group = pygame.sprite.Group()

        self.monkeyKing_group = pygame.sprite.Group()
        self.banana_group = pygame.sprite.Group()
        self.bananaHit_group = pygame.sprite.Group()

        self.bigWhiteMonkey_group = pygame.sprite.Group()
        self.seed_group = pygame.sprite.Group()
        self.seedHit_group = pygame.sprite.Group()
        self.dust_group = pygame.sprite.Group()

        self.monkey_group = pygame.sprite.Group()
        self.angelMonkey_group = pygame.sprite.Group()
        self.monkey_BananaHit_group = pygame.sprite.Group()
        self.moneyShowUpSound = ResourceManager.get_instance().get_sound("monkey\\show_up.wav", 0.35)

        # monkey magician monkeyKing
        self.wave = ResourceManager.get_instance().load_config("config/waves.json")["waves"]
        self.index = 0
        
        # stats
        self.elapsed_time = 0.0
        self.kill_count = 0
        self._prev_enemy_count = 0

        # death overlay
        self._death_overlay_alpha = 0.0   # 0~180，半透明黑幕
        self._death_overlay_active = False # 是否正在淡入黑幕
        self._death_waiting_click = False  # 黑幕完成，等待點擊
        self._overlay_surface = pygame.Surface(
            (self.engine.virtual_width, self.engine.virtual_height), pygame.SRCALPHA
        )
        self._hint_font = pygame.font.Font(
            resource_path("menu/Wordefta.otf"), 36
        )

        # game start setting
        self.spawn_wave()
        
        pygame.mixer.music.play(-1)

    def spawn_wave(self):

        self.moneyShowUpSound.play() # play monkey show up sound

        # monkey
        for _ in range( self.wave[self.index][0] ):
            x = random.randint(self.engine.virtual_width, self.engine.virtual_width + 150)
            self.monkey_group.add( Monkey(x, self.engine.virtual_height - 176) )
        # magician
        for _ in range( self.wave[self.index][1] ):
            new_magician = Magician(100, 100)
            self.magician_group.add( new_magician )
        # monkeyKing
        for _ in range( self.wave[self.index][2] ):
            x = random.randint(self.engine.virtual_width, self.engine.virtual_width + 150)
            self.monkeyKing_group.add( MonkeyKing(x, self.engine.virtual_height - 373) )
        # angelMonkey
        for _ in range( self.wave[self.index][3] ):
            x = random.randint(self.engine.virtual_width, self.engine.virtual_width + 150)
            self.angelMonkey_group.add( AngelMonkey(x, self.engine.virtual_height - 185) )
        # bigWhiteMonkey
        for _ in range( self.wave[self.index][4] ):
            x = random.randint(self.engine.virtual_width, self.engine.virtual_width + 150)
            self.bigWhiteMonkey_group.add( BigWhiteMonkey(x, self.engine.virtual_height - 191) )

    def exit(self):
        # Stop background music or fade out
        pygame.mixer.music.fadeout(500)
        
        self.player.kill()
        self.playerAP.kill()

        # kill all sprites
        for spite in self.pencil_group:
            spite.kill()
        for spite in self.pencilFolded_group:
            spite.kill()
        for spite in self.magician_group:
            spite.kill()
        for spite in self.stone_group:
            spite.kill()
        for spite in self.monkeyKing_group:
            spite.kill()
        for spite in self.banana_group:
            spite.kill()
        for spite in self.bananaHit_group:
            spite.kill()
        for spite in self.bigWhiteMonkey_group:
            spite.kill()
        for spite in self.seed_group:
            spite.kill()
        for spite in self.seedHit_group:
            spite.kill()
        for spite in self.dust_group:
            spite.kill()
        for spite in self.monkey_group:
            spite.kill()
        for spite in self.angelMonkey_group:
            spite.kill()
        for spite in self.monkey_BananaHit_group:
            spite.kill()

        # clear sprites group
        self.pencil_group.empty()
        self.pencilFolded_group.empty()
        
        self.magician_group.empty()
        self.stone_group.empty()

        self.monkeyKing_group.empty()
        self.banana_group.empty()
        self.bananaHit_group.empty()

        self.bigWhiteMonkey_group.empty()
        self.seed_group.empty()
        self.seedHit_group.empty()
        self.dust_group.empty()

        self.monkey_group.empty()
        self.angelMonkey_group.empty()
        self.monkey_BananaHit_group.empty()

    def handle_events(self, events):
        for event in events:
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == LEFT:
                # 死亡黑幕完成後，點擊才切換
                if self._death_waiting_click:
                    pygame.mixer.music.fadeout(500)
                    self.engine.state_machine.change_state("END")
                    return
                if(self.player.power >= 30):
                    self.playerAP.isAPchange = True
                    self.pencil_group.add( Pencil(45, 5, (self.player.rect.centerx + 3, self.player.rect.centery - 10), self.engine.get_mouse_pos()) )
                    self.player.attack()



    def _total_enemies(self):
        return (len(self.magician_group) + len(self.monkey_group) +
                len(self.monkeyKing_group) + len(self.angelMonkey_group) +
                len(self.bigWhiteMonkey_group))

    def _go_to_end(self, is_win):
        """收集結算資料並切換至 END 頁面"""
        self.engine.end_result = {
            "is_win":    is_win,
            "kill_count": self.kill_count,
            "elapsed_time": self.elapsed_time,
        }
        if is_win:
            # 勝利：直接切換
            pygame.mixer.music.fadeout(500)
            self.engine.state_machine.change_state("END")
        else:
            # 失敗：啟動黑幕淡入，等待玩家點擊
            self._death_overlay_active = True

    def update(self, delta_time):
        # ── 黑幕淡入中：只更新黑幕，其他邏輯暫停 ──
        if self._death_overlay_active or self._death_waiting_click:
            if self._death_overlay_active:
                self._death_overlay_alpha = min(180.0, self._death_overlay_alpha + 180 * delta_time * 1.5)
                if self._death_overlay_alpha >= 180.0:
                    self._death_overlay_active = False
                    self._death_waiting_click = True
            return

        self.elapsed_time += delta_time

        # ── 擊殺計數：用前後敵群總數差推算 ──
        current_count = self._total_enemies()
        killed_this_frame = max(0, self._prev_enemy_count - current_count)
        self.kill_count += killed_this_frame

        # ── 玩家死亡 → 失敗（啟動黑幕）──
        if self.player.life <= 0:
            self._go_to_end(is_win=False)
            return

        # ── 全波次清空 → 勝利 ──
        if self._total_enemies() == 0:
            self.index += 1
            if self.index == len(self.wave):
                self._go_to_end(is_win=True)
                return
            else:
                self.spawn_wave()

        self._prev_enemy_count = self._total_enemies()

        # Update
        self.pencil_group.update(delta_time, [self.magician_group, self.monkeyKing_group, self.monkey_group, self.angelMonkey_group, self.bigWhiteMonkey_group],
                                 [self.stone_group, self.banana_group, self.seed_group],
                                 self.pencilFolded_group)
        self.pencilFolded_group.update(delta_time)

        # update monsters
        for magician in self.magician_group:
            magician.update(delta_time, self.stone_group)
        self.monkeyKing_group.update(delta_time, self.banana_group, self.bananaHit_group)
        self.monkey_group.update(delta_time, self.player, self.monkey_BananaHit_group)
        self.angelMonkey_group.update(delta_time, self.player, self.monkey_BananaHit_group)
        self.bigWhiteMonkey_group.update(delta_time, self.player, self.seed_group, self.seedHit_group, self.dust_group)
        
        # update player
        self.player.update(delta_time)
        self.playerAP.update(delta_time, self.player.power)

        # update monsters' attack
        self.stone_group.update(delta_time, self.player)
        self.banana_group.update(delta_time, self.player, self.bananaHit_group)
        self.seed_group.update(delta_time, self.player, self.seedHit_group)
        self.bananaHit_group.update(delta_time)
        self.seedHit_group.update(delta_time)
        self.dust_group.update(delta_time)
        self.monkey_BananaHit_group.update(delta_time)
        

    def draw(self, surface):
        surface.fill(BLACK)
        surface.blit(self.background, (0, 0))
        self.pencil_group.draw(surface)
        self.monkeyKing_group.draw(surface)
        self.bigWhiteMonkey_group.draw(surface)
        self.monkey_group.draw(surface)
        self.angelMonkey_group.draw(surface)
        self.magician_group.draw(surface)
        self.banana_group.draw(surface)
        self.stone_group.draw(surface)
        self.seed_group.draw(surface)
        
        # Draw player
        surface.blit(self.player.image, (self.player.rect.topleft))
        
        # Draw 命中特效
        self.monkey_BananaHit_group.draw(surface)
        self.bananaHit_group.draw(surface)
        self.seedHit_group.draw(surface)
        self.dust_group.draw(surface)
        self.pencilFolded_group.draw(surface)

        # Draw Life point
        surface.blit(self.playerAP.image, (self.playerAP.rect.topleft))
        surface.blit(self.player.life_text_surface, (50, 50))

        # ── 死亡黑幕疊加 ──
        if self._death_overlay_active or self._death_waiting_click:
            vw = self.engine.virtual_width
            vh = self.engine.virtual_height
            self._overlay_surface.fill((0, 0, 0, int(self._death_overlay_alpha)))
            surface.blit(self._overlay_surface, (0, 0))

            if self._death_waiting_click:
                hint_surf = self._hint_font.render("Click to continue...", True, (220, 220, 220))
                hint_rect = hint_surf.get_rect(center=(vw // 2, vh // 2))
                surface.blit(hint_surf, hint_rect)
