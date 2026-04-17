import pygame
from states.base import StateBase
from entities.menu_objects import Button, Title, Star, OptionSelector
from core.resource_manager import ResourceManager, resource_path
from function import BLACK, REFERENCE_FPS

LEFT = 1

class SettingState(StateBase):
    """
    設定頁面。共用 MenuState 的背景與 star_group，
    並在上方疊加半透明黑色面板。可擴充架構。
    """

    def __init__(self, engine):
        super().__init__(engine)

    def enter(self):
        vw = self.engine.virtual_width
        vh = self.engine.virtual_height

        # ── 共用 MenuState 的背景與星星 ──
        menu_state = self.engine.state_machine.states["MENU"]
        self.menu_image = menu_state.menu_image
        self.star_group = menu_state.star_group  # 共享引用！
        self.star_timer = menu_state.star_timer

        # ── 半透明黑色面板（圓角矩形）──
        panel_margin_x = 120
        panel_margin_top = 35
        panel_margin_bottom = 25
        panel_w = vw - panel_margin_x * 2
        panel_h = vh - panel_margin_top - panel_margin_bottom
        self.panel_rect = pygame.Rect(panel_margin_x, panel_margin_top, panel_w, panel_h)
        # 預渲染面板（僅一次，不需每幀繪製）
        self.panel_surface = pygame.Surface((panel_w, panel_h), pygame.SRCALPHA)
        pygame.draw.rect(
            self.panel_surface,
            (0, 0, 0, 150),  # 黑色，alpha=150
            self.panel_surface.get_rect(),
            border_radius=25
        )

        # ── 標題 ──
        self.title = Title((int(vw * 0.5) - 180, int(vh * 0.08)), "Settings", 100)

        # ── BACK 按鈕 ──
        self.back_button = Button(
            (int(vw * 0.5) - 114, int(vh * 0.82)),
            228, 58, "BACK", 50
        )
        self.button_group = pygame.sprite.Group()
        self.button_group.add(self.back_button)

        # ── 可擴充設定列表 ──
        self.settings = self._build_settings(vw, vh)

    def _build_settings(self, vw, vh):
        """
        建立設定項目列表。未來新增設定只需在此加一個 dict。
        每個 dict 包含:
            label:    顯示名稱 (str)
            selector: OptionSelector 實例
            callback: 選項變更時的回呼函式
        """
        label_x = int(vw * 0.25)
        selector_x = int(vw * 0.45)
        row_start_y = int(vh * 0.35)
        row_gap = 80

        # FPS 選項
        fps_options = ["30", "60", "90"]
        current_fps = str(self.engine.fps)
        default_idx = fps_options.index(current_fps) if current_fps in fps_options else 1

        settings = [
            {
                "label": "FPS",
                "font": pygame.font.Font(resource_path("menu\\Wordefta.otf"), 40),
                "y": row_start_y,
                "label_x": label_x,
                "selector": OptionSelector(
                    (selector_x, row_start_y),
                    fps_options,
                    default_index=default_idx,
                    btn_width=80,
                    btn_height=50,
                    text_size=36
                ),
                "callback": self._on_fps_change
            },
            # ── 未來新增設定範例 ──
            # {
            #     "label": "DIFFICULTY",
            #     "font": pygame.font.Font(resource_path("menu\\Wordefta.otf"), 40),
            #     "y": row_start_y + row_gap,
            #     "label_x": label_x,
            #     "selector": OptionSelector(
            #         (selector_x, row_start_y + row_gap),
            #         ["EASY", "NORMAL", "HARD"],
            #         default_index=1
            #     ),
            #     "callback": self._on_difficulty_change
            # },
        ]

        # 預渲染 label 文字
        for item in settings:
            item["_label_surface"] = item["font"].render(item["label"], True, (255, 255, 255))
            item["_label_rect"] = item["_label_surface"].get_rect(
                midleft=(item["label_x"], item["y"] + 25)
            )

        return settings

    # ── Callbacks ──

    def _on_fps_change(self, value):
        """FPS 設定變更回呼"""
        self.engine.fps = int(value)
        self.engine.delta_time = 1.0 / self.engine.fps

    # ── State lifecycle ──

    def exit(self):
        # 將 star_timer 同步回 MenuState
        menu_state = self.engine.state_machine.states["MENU"]
        menu_state.star_timer = self.star_timer

        # 只清理自己的 UI，不觸碰共享的 star_group
        self.back_button.kill()
        self.button_group.empty()

    def handle_events(self, events):
        mouse_pos = self.engine.get_mouse_pos()
        for event in events:
            for item in self.settings:
                if item["selector"].handle_event(event, mouse_pos):
                    item["callback"](item["selector"].get_value())

            if event.type == pygame.MOUSEBUTTONDOWN and event.button == LEFT:
                if self.back_button.isCollideMouse:
                    self.engine.state_machine.change_state("MENU")

    def update(self, delta_time):
        mouse_pos = self.engine.get_mouse_pos()

        # 持續生成星星（共享的 star_group）
        self.star_timer += delta_time
        if self.star_timer >= 100.0 / REFERENCE_FPS:
            self.star_group.add(Star((self.engine.virtual_width, 0)))
            self.star_timer = 0.0

        self.star_group.update(delta_time)
        self.button_group.update(delta_time, mouse_pos)

        for item in self.settings:
            item["selector"].update(delta_time, mouse_pos)

    def draw(self, surface):
        surface.fill(BLACK)

        # 直接繪製背景（無淡入，與 Menu 共享）
        surface.blit(self.menu_image, (0, 0))

        # 共享星星
        self.star_group.draw(surface)

        # 半透明黑色面板
        surface.blit(self.panel_surface, self.panel_rect.topleft)

        # 標題
        self.title.draw(255, surface)

        # 設定列
        for item in self.settings:
            surface.blit(item["_label_surface"], item["_label_rect"])
            item["selector"].draw(surface)

        # BACK 按鈕
        for button in self.button_group:
            button.draw(surface)
