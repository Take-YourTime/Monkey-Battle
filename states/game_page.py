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
                if(self.player.power >= 30):
                    self.playerAP.isAPchange = True
                    self.pencil_group.add( Pencil(45, 5, (self.player.rect.centerx + 3, self.player.rect.centery - 10), self.engine.get_mouse_pos()) )
                    self.player.attack()



    def update(self, delta_time):
        if len(self.magician_group) == 0 and len(self.monkey_group) == 0 and len(self.monkeyKing_group) == 0 and len(self.angelMonkey_group) == 0 and len(self.bigWhiteMonkey_group) == 0:
            self.index += 1
            if self.index == len(self.wave):
                pygame.mixer.music.fadeout(500)
                self.engine.state_machine.change_state("END")
                return
            else:
                self.spawn_wave()

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
