import pygame
import sys
from states.base import StateBase
from entities.menu_objects import Button, Title, Star, VolumeSlider
from core.resource_manager import ResourceManager, resource_path
from function import BLACK, blit_alpha, REFERENCE_FPS

LEFT = 1

class MenuState(StateBase):
    def __init__(self, engine):
        super().__init__(engine)
        # Shared state (persists between MENU ↔ SETTING transitions)
        self._shared_initialized = False
        self.star_group = pygame.sprite.Group()
        self.star_timer = 0.0
        self.menu_image = None
        self.opacity = 0.0

    def enter(self):
        vw = self.engine.virtual_width
        vh = self.engine.virtual_height

        # ── 共用資源（只建立一次，MENU ↔ SETTING 間保留）──
        if not self._shared_initialized:
            self._shared_initialized = True
            raw_img = pygame.image.load(resource_path("menu/sunset.jpg")).convert()
            self.menu_image = pygame.transform.scale(raw_img, (vw, vh))
            self.star_group.add(Star((vw, 0)))
            self.opacity = 0.0

            # BGM
            rm = ResourceManager.get_instance()
            pygame.mixer.music.load(resource_path("BGM/JustAnotherMapleLeaf.mp3"))
            pygame.mixer.music.set_volume(0.5 * rm.global_volume)
            pygame.mixer.music.play(-1)
        else:
            # Skip fade-in when returning from SETTING
            self.opacity = 255.0

        # ── 每次進入時重建的 UI 元件 ──
        self.battleText_color = 255.0
        self.battleText_color_detect = True

        # button
        self.start_button = Button((int(vw * (800 / 1280)), int(vh * (220 / 720))), 228, 75, "START", 65)
        self.setting_button = Button((int(vw * (800 / 1280)), int(vh * (330 / 720))), 228, 58, "SETTING", 50)
        self.exit_button = Button((int(vw * (800 / 1280)), int(vh * (420 / 720))), 228, 58, "EXIT", 50)

        # Slider
        self.volume_slider = VolumeSlider((vw - 250, vh - 60), 200, 20)
        self.volume_slider.volume = ResourceManager.get_instance().global_volume

        # Title
        self.tilte_monkey = Title((int(vw * (150 / 1280)), int(vh * (200 / 720))), "Monkey", 120)
        self.tilte_battle = Title((int(vw * (250 / 1280)), int(vh * (350 / 720))), "Battle", 120)

        # group
        self.button_group = pygame.sprite.Group()
        self.button_group.add(self.start_button)
        self.button_group.add(self.setting_button)
        self.button_group.add(self.exit_button)

    def exit(self):
        # 只清理 per-enter 的 UI 元件，不觸碰共用的 star_group 與背景
        self.start_button.kill()
        self.setting_button.kill()
        self.exit_button.kill()
        self.volume_slider.kill()
        self.tilte_battle.kill()
        self.tilte_monkey.kill()
        for button in self.button_group:
            button.kill()
        self.button_group.empty()

    def handle_events(self, events):
        for event in events:
            # Volume slider event handling
            if self.volume_slider.handle_event(event, self.engine.get_mouse_pos()):
                rm = ResourceManager.get_instance()
                rm.set_global_volume(self.volume_slider.volume)
                pygame.mixer.music.set_volume(0.5 * self.volume_slider.volume)

            if event.type == pygame.MOUSEBUTTONDOWN and event.button == LEFT:
                if self.start_button.isCollideMouse == True:
                    self.engine.state_machine.change_state("GAME")
                elif self.setting_button.isCollideMouse == True:
                    self.engine.state_machine.change_state("SETTING")
                elif self.exit_button.isCollideMouse == True:
                    pygame.quit()
                    sys.exit()
                elif not self.volume_slider.is_dragging:
                    self.star_group.add(Star((self.engine.virtual_width, 0)))

    def update(self, delta_time):
        time_step = delta_time * REFERENCE_FPS
        # Star spawn timer
        self.star_timer += delta_time
        if self.star_timer >= 100.0 / REFERENCE_FPS:
            self.star_group.add(Star((self.engine.virtual_width, 0)))
            self.star_group.add(Star((self.engine.virtual_width, 0)))
            self.star_timer = 0.0

        if self.battleText_color_detect == True:
            self.battleText_color -= 2 * time_step
            if self.battleText_color < 3:
                self.battleText_color_detect = False
        else:
            self.battleText_color += 1 * time_step
            if self.battleText_color >= 255:
                self.battleText_color = 255.0
                self.battleText_color_detect = True

        self.star_group.update(delta_time)
        self.button_group.update(delta_time, self.engine.get_mouse_pos())

    def draw(self, surface):
        surface.fill(BLACK)

        if self.opacity <= 255:
            blit_alpha(surface, self.menu_image, (0, 0), int(self.opacity))
            self.opacity += 120 * self.engine.delta_time  # 1 per frame at 120fps = 120/s
        else:
            surface.blit(self.menu_image, (0, 0))

        for button in self.button_group:
            button.draw(surface)

        self.star_group.draw(surface)
        
        self.tilte_monkey.draw(255, surface)
        self.tilte_battle.draw(int(max(0, min(255, self.battleText_color))), surface)
        self.volume_slider.draw(surface)
