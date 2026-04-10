import pygame
import sys
from states.base import StateBase
from entities.menu_objects import Button, Title, Star
from function import BLACK
from core.resource_manager import resource_path

LEFT = 1

def blit_alpha(target, source, location, opacity): # window 圖片 位置 透明度
    x = location[0]
    y = location[1]
    temp = pygame.Surface((source.get_width(), source.get_height())).convert()
    temp.blit(target, ( -x, - y ))
    temp.blit(source, (0, 0))
    temp.set_alpha(opacity)        
    target.blit(temp, location)

class MenuState(StateBase):
    def __init__(self, engine):
        super().__init__(engine)

    def enter(self):
        # load pictures
        self.menu_RAWimage = pygame.image.load(resource_path("sunset.jpg")).convert()
        self.menu_image = pygame.transform.scale(self.menu_RAWimage, (self.engine.window_width, self.engine.window_height))

        # load BGM and sound
        pygame.mixer.music.load(resource_path("menu\\JustAnotherMapleLeaf.mp3"))
        pygame.mixer.music.set_volume(0.5)

        # setting variable
        self.opacity = 0
        self.frame = 0

        # color changing
        self.battleText_color = 255
        self.battleText_color_detect = True

        # button
        self.start_button = Button((800, 220), 238, 75, "START", 90)
        self.setting_button = Button((800, 330), 228, 58, "SETTING", 66)
        self.exit_button = Button((800, 420), 120, 58, "EXIT", 66)

        # Title
        self.tilte_monkey = Title((150, 200), "Monkey", 120)
        self.tilte_battle = Title((250, 350), "Battle", 120)

        # group
        self.button_group = pygame.sprite.Group()
        self.button_group.add(self.start_button)
        self.button_group.add(self.setting_button)
        self.button_group.add(self.exit_button)
        self.star_group = pygame.sprite.Group()
        self.star_group.add(Star((self.engine.window_width, 0)))

        # play menu BGM
        pygame.mixer.music.play(-1)

    def exit(self):
        self.tilte_battle.kill()
        self.tilte_monkey.kill()
        for star in self.star_group:
            star.kill()
        for button in self.button_group:
            button.kill()

    def handle_events(self, events):
        for event in events:
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == LEFT:
                if self.start_button.isCollideMouse == True:
                    self.engine.state_machine.change_state("GAME")
                elif self.exit_button.isCollideMouse == True:
                    pygame.quit()
                    sys.exit()
                else:
                    self.star_group.add(Star((self.engine.window_width, 0)))
            elif event.type == pygame.VIDEORESIZE:
                self.menu_image = pygame.transform.scale(self.menu_RAWimage, (self.engine.window_width, self.engine.window_height))

    def update(self):
        if self.frame == 100:
            self.star_group.add(Star((self.engine.window_width, 0)))
            self.star_group.add(Star((self.engine.window_width, 0)))
            self.frame = 0
        else:
            self.frame += 1

        if self.battleText_color_detect == True:
            self.battleText_color -= 2
            if self.battleText_color < 3:
                self.battleText_color_detect = False
        else:
            self.battleText_color += 1
            if self.battleText_color >= 255:
                self.battleText_color_detect = True

        self.star_group.update()
        self.button_group.update()

    def draw(self, surface):
        surface.fill(BLACK)

        if self.opacity <= 255:
            blit_alpha(surface, self.menu_image, (0, 0), self.opacity)
            self.opacity += 1
        else:
            surface.blit(self.menu_image, (0, 0))

        for button in self.button_group:
            button.draw(surface)

        for star in self.star_group:
            blit_alpha(surface, star.image, star.rect.topleft, star.opacity)
        
        self.tilte_monkey.draw(255, surface)
        self.tilte_battle.draw(self.battleText_color, surface)
