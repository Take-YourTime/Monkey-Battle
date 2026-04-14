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
    # image
    def __init__(self, location, width, height, buttonText, textSize) -> None:
        super().__init__()
        # 建立一個surface
        self.x = location[0]
        self.y = location[1]
        #self.font = pygame.sysfont.Font(None, textSize)
        self.font = pygame.font.Font(resource_path("menu\\Wordefta.otf"), textSize)
        self.text_surface = self.font.render(buttonText, True, (WHITE))
        
        self.surface = pygame.Surface((width, height), pygame.SRCALPHA)
        # 將一個透明的舉行畫在這個surface上
        pygame.draw.rect(self.surface, (0, 0, 0, 20), self.surface.get_rect())
        self.text = buttonText
        self.rect = pygame.Rect(self.x, self.y, width, height)
        self.isCollideMouse = False
        


    def update(self, mouse_pos) -> None:
        if self.rect.collidepoint( mouse_pos ):
            if self.isCollideMouse == False:
                self.isCollideMouse = True
                #self.font.set_italic(True)
                self.font.set_bold(True)
                self.text_surface = self.font.render(self.text, True, (WHITE))
        else:
            if self.isCollideMouse == True:
                self.isCollideMouse = False
                #self.font.set_italic(False)
                self.font.set_bold(False)
                self.text_surface = self.font.render(self.text, True, (WHITE))

    def draw(self, surface):
        surface.blit(self.surface, (self.x, self.y))
        surface.blit(self.text_surface, (self.x, self.y))


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
        #self.vector = ((-1) * math.cos(self.angle / 180 * math.pi), (1) * math.sin(self.angle / 180 * math.pi))
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