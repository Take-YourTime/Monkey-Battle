import pygame
import sys
from core.state_machine import StateMachine

class GameEngine:
    def __init__(self):
        # 初始化
        pygame.init()
        pygame.mixer.init()
        pygame.font.init()

        self.window_width = 1280
        self.window_height = 720
        self.fps = 120

        # load window surface
        self.window_surface = pygame.display.set_mode((self.window_width, self.window_height), pygame.RESIZABLE)
        pygame.display.set_caption('Monkey VS Student')

        self.main_clock = pygame.time.Clock()
        self.running = True

        self.state_machine = StateMachine()

    def run(self):
        while self.running:
            events = pygame.event.get()
            for event in events:
                if event.type == pygame.QUIT:
                    self.running = False
                elif event.type == pygame.VIDEORESIZE:
                    self.window_width, self.window_height = self.window_surface.get_size()

            self.state_machine.handle_events(events)
            self.state_machine.update()
            
            self.state_machine.draw(self.window_surface)

            pygame.display.update()
            self.main_clock.tick(self.fps)

        pygame.quit()
        sys.exit()
