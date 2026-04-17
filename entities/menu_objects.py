from typing import Any
import pygame
import function
import random
import math
from function import WHITE, get_normalize_vector, get_random_position, WINDOW_WIDTH, WINDOW_HEIGHT, REFERENCE_FPS
from core.resource_manager import ResourceManager, resource_path

'''
class Menu(pygame.sprite.Sprite):
    images = [pygame.image.load(resource_path("menu\\thread1.jpg")).convert_alpha(),
              pygame.image.load(resource_path("menu\\thread2.jpg")).convert_alpha(),
              pygame.image.load(resource_path("menu\\thread3.jpg")).convert_alpha(),
              pygame.image.load(resource_path("menu\\thread4.jpg")).convert_alpha()]
    imageLocation = [(0, 0),
                     (500, 0),
                     (300, 0),
                     (950, 0)]
    
    def __init__(self) -> None:
        super().__init__()
        self.image = Menu.images[0]
        # images index
        self.index = 0
        
        self.rect = Menu.images[0].get_rect()
        self.rect.topleft = Menu.imageLocation[0]
        self.opacity = 10
        self.isExponentiation = True
    
    def update(self, delta_time):
        if self.isExponentiation == True:
            if self.opacity <= 255:
                self.opacity += 2
            else:
                self.isExponentiation = False
        else:
            if self.opacity >= 10:
                self.opacity -= 3
            else:
                self.opacity = 10
                self.isExponentiation = True
                self.index = (self.index + 1) % 4
                self.image = Menu.images[self.index]
                self.rect.topleft = Menu.imageLocation[self.index]
'''

class Button(pygame.sprite.Sprite):
    def __init__(self, location, width, height, buttonText, textSize) -> None:
        super().__init__()
        self.x = float(location[0])
        self.y = float(location[1])
        self.width = width
        self.height = height
        self.text = buttonText
        self.font = pygame.font.Font(resource_path("menu\\Wordefta.otf"), textSize)
        self.rect = pygame.Rect(self.x, self.y, width, height)
        self.isCollideMouse = False

        # hover animation 0.0 ~ 1.0
        self.hover_progress = 0.0

        # Pre-render text surfaces for normal and hover states (cached)
        self._text_normal = self.font.render(buttonText, True, WHITE)
        self._text_hover = self.font.render(buttonText, True, (230, 255, 230))
        self.text_surface = self._text_normal
        self._text_center = (self.x + self.width // 2, self.y + self.height // 2 + self.height // 10)

    def update(self, delta_time, mouse_pos) -> None:
        time_step = delta_time * REFERENCE_FPS
        if self.rect.collidepoint( mouse_pos ):
            self.isCollideMouse = True
            self.hover_progress = min(1.0, self.hover_progress + 0.1 * time_step)
        else:
            self.isCollideMouse = False
            self.hover_progress = max(0.0, self.hover_progress - 0.1 * time_step)

    def draw(self, surface):
        alpha = int(20 + 80 * self.hover_progress)
        bg_surface = pygame.Surface((self.width, self.height), pygame.SRCALPHA)
        # 繪製圓角透明底色
        pygame.draw.rect(bg_surface, (255, 255, 255, alpha), bg_surface.get_rect(), border_radius=15)
        # 繪製圓角邊框
        pygame.draw.rect(bg_surface, (255, 255, 255, 200), bg_surface.get_rect(), width=2, border_radius=15)

        surface.blit(bg_surface, (self.x, self.y))
        
        # Use pre-rendered cached text surface based on hover state
        self.text_surface = self._text_hover if self.hover_progress > 0.5 else self._text_normal
        # 中心對齊
        text_rect = self.text_surface.get_rect(center = self._text_center)
        surface.blit(self.text_surface, text_rect)

class VolumeSlider(pygame.sprite.Sprite):
    def __init__(self, location, width, height) -> None:
        super().__init__()
        self.x, self.y = location
        self.width = width
        self.height = height
        self.rect = pygame.Rect(self.x, self.y, width, height)
        self.volume = 1.0
        self.is_dragging = False

        # Cache font and text surface to avoid re-creating every frame
        self._font = pygame.font.Font(resource_path("menu\\Wordefta.otf"), 24)
        self._last_vol_pct = -1
        self._vol_text_surface = None

    def handle_event(self, event, mouse_pos):
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if self.rect.collidepoint(mouse_pos):
                self.is_dragging = True
                return self.update_volume(mouse_pos[0])
        elif event.type == pygame.MOUSEBUTTONUP and event.button == 1:
            self.is_dragging = False
        elif event.type == pygame.MOUSEMOTION:
            if self.is_dragging:
                return self.update_volume(mouse_pos[0])
        return False

    def update_volume(self, mouse_x):
        rel_x = max(0, min(self.width, mouse_x - self.x))
        self.volume = rel_x / self.width
        return True

    def draw(self, surface):
        # 繪製底部文字（僅在音量變化時重新渲染）
        vol_pct = int(self.volume * 100)
        if vol_pct != self._last_vol_pct:
            self._vol_text_surface = self._font.render(f"MUSIC VOL: {vol_pct}%", True, WHITE)
            self._last_vol_pct = vol_pct
        surface.blit(self._vol_text_surface, (self.x, self.y - 30))

        # 繪製灰色軌道
        track_rect = pygame.Rect(self.x, self.y + self.height // 2 - 2, self.width, 4)
        pygame.draw.rect(surface, (255, 255, 255, 100), track_rect, border_radius=2)
        
        # 繪製白色已填滿軌道
        fill_rect = pygame.Rect(self.x, self.y + self.height // 2 - 2, int(self.width * self.volume), 4)
        pygame.draw.rect(surface, (255, 255, 255), fill_rect, border_radius=2)
        
        # 繪製可視把手 (Knob)
        knob_x = self.x + int(self.width * self.volume)
        knob_y = self.y + self.height // 2
        
        knob_rad = 8 if not self.is_dragging else 12
        pygame.draw.circle(surface, (255, 255, 255), (knob_x, knob_y), knob_rad)


class Title(pygame.sprite.Sprite):
    def __init__(self, location, titleText, textSize) -> None:
        super().__init__()
        self.x = location[0]
        self.y = location[1]
        self.text = titleText
        self.font = pygame.font.Font(resource_path("menu\\Tightones.otf"), textSize)
        self.text_surface = self.font.render(self.text, True, (WHITE))
        self._last_color = None  # Cache: only re-render text when color changes
    
    def draw(self, color, surface):
        if color != self._last_color:
            self.text_surface = self.font.render(self.text, True, (255, color, color))
            self._last_color = color
        surface.blit(self.text_surface, (self.x, self.y))


class Star(pygame.sprite.Sprite):

    def __init__(self, location) -> None:
        super().__init__()
        rm = ResourceManager.get_instance()
        self.raw_image = rm.get_image("menu\\star.png")
        self.images = [rm.get_image("menu\\star0.png"),
                       rm.get_image("menu\\star1.png"),
                       rm.get_image("menu\\star2.png"),
                       rm.get_image("menu\\star3.png"),
                       rm.get_image("menu\\star4.png"),
                       rm.get_image("menu\\star5.png"),
                       rm.get_image("menu\\star6.png"),
                       rm.get_image("menu\\star7.png")]

        self.image = self.raw_image.copy()  # Copy so set_alpha won't affect RM cache
        # images index
        self.index = 0.0
        self.opacity = 20.0
        self.angle = random.randint(0, 90)
        self.isOpacityAscending = True
        self.width = self.image.get_width()
        self.height = self.image.get_height()
        self.rect = self.image.get_rect()
        self.rect.topleft = (location[0], location[1])
        self.destination = get_random_position(WINDOW_WIDTH, WINDOW_HEIGHT, self.width, self.height)
        self.vector = get_normalize_vector(location[0], location[1], self.destination[0], self.destination[1])
        self.x = float(location[0])
        self.y = float(location[1])

    def update(self, delta_time) -> None:
        time_step = delta_time * REFERENCE_FPS
        # out of map
        if (self.x > WINDOW_WIDTH + self.width or self.x < -(self.width) or self.y > WINDOW_HEIGHT + self.height or self.y < -(self.height) ):
            self.kill()
        else:
            if self.isOpacityAscending == True:
                self.opacity += 2 * time_step
                if self.opacity >= 253:
                    self.isOpacityAscending = False
            else:
                self.opacity -= 2 * time_step
                if self.opacity <= 20:
                    self.isOpacityAscending = True
            
            self.image.set_alpha(int(max(0, min(255, self.opacity))))  # Apply alpha directly on owned copy
            self.index += time_step
            self.x += self.vector[0] * time_step
            self.y += self.vector[1] * time_step
            self.rect.topleft = (int(self.x), int(self.y))


class OptionSelector:
    """
    可複用的水平選項選擇器（radio group 風格）。
    用於設定頁面中具有離散選項的設定項目。
    
    Usage:
        selector = OptionSelector((x, y), ["30", "60", "90"], default_index=1)
        selector.handle_event(event, mouse_pos)  # 處理點擊
        selector.update(delta_time, mouse_pos)            # 更新 hover 動畫
        selector.draw(surface)                    # 繪製
        current_value = selector.get_value()      # 取得目前選中的值
    """
    def __init__(self, location, options, default_index=0, btn_width=80, btn_height=50, text_size=36, gap=15):
        self.x, self.y = location
        self.options = options
        self.selected_index = default_index
        self.btn_width = btn_width
        self.btn_height = btn_height
        self.gap = gap
        self.font = pygame.font.Font(resource_path("menu\\Wordefta.otf"), text_size)
        
        # Build rects and pre-render text for each option
        self._rects = []
        self._text_surfaces = []
        self._text_selected_surfaces = []
        self._hover_progress = []
        for i, opt in enumerate(options):
            rx = self.x + i * (btn_width + gap)
            rect = pygame.Rect(rx, self.y, btn_width, btn_height)
            self._rects.append(rect)
            self._text_surfaces.append(self.font.render(str(opt), True, WHITE))
            self._text_selected_surfaces.append(self.font.render(str(opt), True, (30, 30, 30)))
            self._hover_progress.append(0.0)
    
    def handle_event(self, event, mouse_pos):
        """處理滑鼠點擊事件，回傳是否有變更選項"""
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            for i, rect in enumerate(self._rects):
                if rect.collidepoint(mouse_pos):
                    if i != self.selected_index:
                        self.selected_index = i
                        return True
        return False
    
    def update(self, delta_time, mouse_pos):
        time_step = delta_time * REFERENCE_FPS
        for i, rect in enumerate(self._rects):
            if rect.collidepoint(mouse_pos):
                self._hover_progress[i] = min(1.0, self._hover_progress[i] + 0.1 * time_step)
            else:
                self._hover_progress[i] = max(0.0, self._hover_progress[i] - 0.1 * time_step)
    
    def draw(self, surface):
        for i, rect in enumerate(self._rects):
            is_selected = (i == self.selected_index)
            hover = self._hover_progress[i]
            
            bg = pygame.Surface((self.btn_width, self.btn_height), pygame.SRCALPHA)
            
            if is_selected:
                # 選中：白色填滿背景 + 深色文字
                pygame.draw.rect(bg, (255, 255, 255, 220), bg.get_rect(), border_radius=12)
                pygame.draw.rect(bg, (255, 255, 255, 255), bg.get_rect(), width=2, border_radius=12)
            else:
                # 未選中：半透明 + hover 效果
                alpha = int(20 + 60 * hover)
                pygame.draw.rect(bg, (255, 255, 255, alpha), bg.get_rect(), border_radius=12)
                pygame.draw.rect(bg, (255, 255, 255, 150), bg.get_rect(), width=2, border_radius=12)
            
            surface.blit(bg, rect.topleft)
            
            # 文字置中
            text = self._text_selected_surfaces[i] if is_selected else self._text_surfaces[i]
            text_rect = text.get_rect(center=rect.center)
            surface.blit(text, text_rect)
    
    def get_value(self):
        """回傳目前選中的選項值（字串）"""
        return self.options[self.selected_index]
    
    def get_index(self):
        """回傳目前選中的索引"""
        return self.selected_index