import pygame
import random
from states.base import StateBase
from function import BLACK

from entities.player import Player, AP
from entities.projectiles import Pencil
from entities.magician import Magician
from entities.monkey_king import MonkeyKing
from entities.monkey import Monkey
from core.resource_manager import ResourceManager, resource_path

LEFT = 1

def blit_alpha(target, source, location, opacity): # window 圖片 位置 透明度
    x = location[0]
    y = location[1]
    temp = pygame.Surface((source.get_width(), source.get_height())).convert()
    temp.blit(target, ( -x, - y ))
    temp.blit(source, (0, 0))
    temp.set_alpha(opacity)        
    target.blit(temp, location)

class GameState(StateBase):
    def __init__(self, engine):
        super().__init__(engine)

    def enter(self):
        # sound
        self.shoot_sound = pygame.mixer.Sound(resource_path("shoot.wav"))

        # load BGM
        pygame.mixer.music.load(resource_path("Motivation.mp3"))
        pygame.mixer.music.set_volume(0.4)

        # load background
        self.background = pygame.image.load(resource_path("school.png")).convert_alpha()
        
        self.player = Player(70, self.engine.window_height-273)
        self.playerAP = AP((100, 200))

        # sprites group
        self.pencil_group = pygame.sprite.Group()
        self.pencilFolded_group = pygame.sprite.Group()

        self.magician_group = pygame.sprite.Group()
        self.stone_group = pygame.sprite.Group()

        self.monkeyKing_group = pygame.sprite.Group()
        self.banana_group = pygame.sprite.Group()
        self.bananaHit_group = pygame.sprite.Group()

        self.monkey_group = pygame.sprite.Group()
        self.monkey_BananaHit_group = pygame.sprite.Group()
        self.moneyShowUpSound = ResourceManager.get_instance().get_sound("monkey\\show_up.wav", 0.35)

        # monkey magician monkeyKing
        self.wave = [[2, 1, 0],
                     [3, 0, 1],
                     [4, 2, 1],
                     [5, 3, 2]]
        self.index = 0
        
        # game start setting
        self.spawn_wave()
        
        pygame.mixer.music.play(-1)

    def spawn_wave(self):

        self.moneyShowUpSound.play() # play monkey show up sound

        for _ in range( self.wave[self.index][0] ):
            x = random.randint(self.engine.window_width, self.engine.window_width + 150)
            self.monkey_group.add( Monkey(x, self.engine.window_height - 176) )
        for _ in range( self.wave[self.index][1] ):
            new_magician = Magician(100, 100)
            self.magician_group.add( new_magician )
        for _ in range( self.wave[self.index][2] ):
            x = random.randint(self.engine.window_width, self.engine.window_width + 150)
            self.monkeyKing_group.add( MonkeyKing(x, self.engine.window_height - 373) )

    def exit(self):
        # Stop background music or fade out
        pygame.mixer.music.fadeout(500)

    def handle_events(self, events):
        for event in events:
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == LEFT:
                if(self.player.power >= 30):
                    self.playerAP.isAPchange = True
                    self.shoot_sound.play()
                    self.pencil_group.add( Pencil(45, 5, (self.player.rect.centerx + 3, self.player.rect.centery - 10), (pygame.mouse.get_pos())) )
                    self.player.attack()

    def update(self):
        if len(self.magician_group) == 0 and len(self.monkey_group) == 0 and len(self.monkeyKing_group) == 0:
            self.index += 1
            if self.index == len(self.wave):
                pygame.mixer.music.fadeout(500)
                self.engine.state_machine.change_state("END")
                return
            else:
                self.spawn_wave()

        # Update
        self.pencil_group.update([self.magician_group, self.monkeyKing_group, self.monkey_group], [self.stone_group, self.banana_group], self.pencilFolded_group)
        for magician in self.magician_group:
            magician.update(self.stone_group)
        self.monkeyKing_group.update(self.banana_group)
        self.monkey_group.update(self.player, self.monkey_BananaHit_group)
        self.banana_group.update(self.player, self.bananaHit_group)
        self.stone_group.update(self.player)
        self.player.update()
        self.playerAP.update(self.player.power)
        self.bananaHit_group.update()
        self.monkey_BananaHit_group.update()
        self.pencilFolded_group.update()

    def draw(self, surface):
        surface.fill(BLACK)
        surface.blit(self.background, (0, 0))
        self.pencil_group.draw(surface)
        self.magician_group.draw(surface)
        self.monkeyKing_group.draw(surface)
        self.monkey_group.draw(surface)
        self.banana_group.draw(surface)
        self.stone_group.draw(surface)
        
        # Draw player
        surface.blit(self.player.image, (self.player.rect.topleft))
        
        # Draw 命中特效
        self.monkey_BananaHit_group.draw(surface)
        self.bananaHit_group.draw(surface)
        for pencilFolded in self.pencilFolded_group:
            blit_alpha(surface, pencilFolded.image, pencilFolded.rect.topleft, pencilFolded.opacity)

        # Draw Life point
        surface.blit(self.playerAP.image, (self.playerAP.rect.topleft))
        surface.blit(self.player.life_text_surface, (50, 50))
