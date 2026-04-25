import pygame
from states.base import StateBase
from entities.menu_objects import Button
from core.resource_manager import ResourceManager, resource_path
from function import BLACK, WHITE, blit_alpha

LEFT = 1

class EndState(StateBase):
    def __init__(self, engine):
        super().__init__(engine)

    def enter(self):
        vw = self.engine.virtual_width
        vh = self.engine.virtual_height
        rm = ResourceManager.get_instance()

        # ── 讀取遊戲結算資料 ──
        result = getattr(self.engine, "end_result", {})
        self.is_win      = result.get("is_win", False)
        self.kill_count  = result.get("kill_count", 0)
        self.elapsed_sec = result.get("elapsed_time", 0.0)

        # ── BGM ──
        if self.is_win:
            pygame.mixer.music.load(resource_path("BGM/Elfwood.mp3")) # win BGM
            pygame.mixer.music.set_volume(0.95 * rm.global_volume)
        else:
            pygame.mixer.music.load(resource_path("BGM/Dunas.mp3")) # loss BGM
            pygame.mixer.music.set_volume(0.45 * rm.global_volume)
        pygame.mixer.music.play(-1)

        # ── 背景 ──
        raw_img = pygame.image.load(resource_path("menu/sunset.jpg")).convert()
        self.bg_image = pygame.transform.scale(raw_img, (vw, vh))
        self.opacity = 0.0


        # ── 字體 ──
        self.font_result = pygame.font.Font(resource_path("menu/Tightones.otf"), 110)
        self.font_stats  = pygame.font.Font(resource_path("menu/Wordefta.otf"),  46)

        # ── 返回主選單按鈕──
        btn_w = 228
        btn_x = (vw - btn_w) // 2 # 水平置中
        btn_y = int(vh * (520 / 720))
        self.menu_button = Button((btn_x, btn_y), btn_w, 58, "MENU", 50)
        self.button_group = pygame.sprite.Group()
        self.button_group.add(self.menu_button)

    def exit(self):
        pygame.mixer.music.fadeout(500)
        self.menu_button.kill()
        self.button_group.empty()

    # ── 可擴充的統計項目（未來加欄位只需在此 list 新增）──
    def _build_stat_lines(self):
        m, s = divmod(int(self.elapsed_sec), 60)
        return [
            f"Kills  :  {self.kill_count}",
            f"Time   :  {m:02d}:{s:02d}",
        ]

    def handle_events(self, events):
        for event in events:
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == LEFT:
                if self.menu_button.isCollideMouse:
                    # 讓 MenuState 重新淡入（清除已初始化標記）
                    menu_state = self.engine.state_machine.states.get("MENU")
                    if menu_state:
                        menu_state._shared_initialized = False
                    self.engine.state_machine.change_state("MENU")

    def update(self, delta_time):
        self.button_group.update(delta_time, self.engine.get_mouse_pos())

    def draw(self, surface):
        vw = self.engine.virtual_width
        vh = self.engine.virtual_height

        surface.fill(BLACK)

        # 背景淡入
        if self.opacity <= 255:
            blit_alpha(surface, self.bg_image, (0, 0), int(self.opacity))
            self.opacity += 120 * self.engine.delta_time
        else:
            surface.blit(self.bg_image, (0, 0))

        # ── WIN / LOSS 標題 ──
        result_text  = "WIN" if self.is_win else "LOSS"
        result_color = (100, 255, 150) if self.is_win else (255, 80, 80)
        result_surf  = self.font_result.render(result_text, True, result_color)
        result_rect  = result_surf.get_rect(center=(vw // 2, int(vh * 0.22)))
        surface.blit(result_surf, result_rect)

        # ── 統計資訊 ──
        stat_lines = self._build_stat_lines()
        for i, line in enumerate(stat_lines):
            stat_surf = self.font_stats.render(line, True, WHITE)
            stat_rect = stat_surf.get_rect(center=(vw // 2, int(vh * 0.42) + i * 64))
            surface.blit(stat_surf, stat_rect)

        # ── 返回按鈕 ──
        for btn in self.button_group:
            btn.draw(surface)
