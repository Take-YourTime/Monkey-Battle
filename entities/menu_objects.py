from typing import Any
import pygame
import function
import random
import math
from function import WHITE, get_normalize_vector, get_random_position, WINDOW_WIDTH, WINDOW_HEIGHT
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
    
    def update(self):
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
        self.text_surface = self.font.render(buttonText, True, WHITE)
        self.rect = pygame.Rect(self.x, self.y, width, height)
        self.isCollideMouse = False

        # hover animation 0.0 ~ 1.0
        self.hover_progress = 0.0

    def update(self, mouse_pos) -> None:
        if self.rect.collidepoint( mouse_pos ):
            self.isCollideMouse = True
            self.hover_progress = min(1.0, self.hover_progress + 0.1)
        else:
            self.isCollideMouse = False
            self.hover_progress = max(0.0, self.hover_progress - 0.1)

    def draw(self, surface):
        alpha = int(20 + 80 * self.hover_progress)
        bg_surface = pygame.Surface((self.width, self.height), pygame.SRCALPHA)
        # 繪製圓角透明底色
        pygame.draw.rect(bg_surface, (255, 255, 255, alpha), bg_surface.get_rect(), border_radius=15)
        # 繪製圓角邊框
        pygame.draw.rect(bg_surface, (255, 255, 255, 200), bg_surface.get_rect(), width=2, border_radius=15)

        surface.blit(bg_surface, (self.x, self.y))
        
        # 變色或純白
        color = (255, 255, 255)
        if self.hover_progress > 0.5:
            color = (230, 255, 230)
        
        self.text_surface = self.font.render(self.text, True, color)
        # 中心對齊
        # center = (self.x + self.width // 2, self.y + self.height // 2 + 5)
        text_rect = self.text_surface.get_rect(center = (self.x + self.width // 2, self.y + self.height // 2 + self.height // 10))
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
        # 繪製底部文字
        font = pygame.font.Font(resource_path("menu\\Wordefta.otf"), 24)
        vol_text = font.render(f"MUSIC VOL: {int(self.volume * 100)}%", True, WHITE)
        surface.blit(vol_text, (self.x, self.y - 30))

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
    
    def draw(self, color, surface):
        self.text_surface = self.font.render(self.text, True, (255, color, color))
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

        self.image = self.raw_image
        # images index
        self.index = 0
        self.opacity = 20
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

    def update(self) -> None:
        # out of map
        if (self.x > WINDOW_WIDTH + self.width or self.x < -(self.width) or self.y > WINDOW_HEIGHT + self.height or self.y < -(self.height) ):
            self.kill()
        else:
            if self.isOpacityAscending == True:
                self.opacity += 2
                if self.opacity >= 253:
                    self.isOpacityAscending = False
            else:
                self.opacity -= 2
                if self.opacity <= 20:
                    self.isOpacityAscending = True
            
            self.index += 1
            #self.image = Star.images[(self.index // 40) % 8]
            self.x += self.vector[0]
            self.y += self.vector[1]
            self.rect.topleft = (self.x, self.y)