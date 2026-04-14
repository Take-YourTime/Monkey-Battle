import pygame
import sys
from core.state_machine import StateMachine
from function import WINDOW_WIDTH, WINDOW_HEIGHT, VIRTUAL_WIDTH, VIRTUAL_HEIGHT

class GameEngine:
    def __init__(self):
        # 初始化
        pygame.init()
        pygame.mixer.init()
        pygame.font.init()

        # original window size
        self.window_width = WINDOW_WIDTH
        self.window_height = WINDOW_HEIGHT

        # game fps
        self.fps = 120

        # load window surface
        self.window_surface = pygame.display.set_mode((self.window_width, self.window_height), pygame.RESIZABLE)
        pygame.display.set_caption('Monkey VS Student')

        self.main_clock = pygame.time.Clock()
        self.running = True

        # use to change state(page), e.g. menu -> game -> end
        self.state_machine = StateMachine()

        # Virtual Canvas
        self.virtual_width = VIRTUAL_WIDTH
        self.virtual_height = VIRTUAL_HEIGHT
        self.canvas = pygame.Surface((self.virtual_width, self.virtual_height))

        # the real game screen (not window) display size
        self.view_rect = pygame.Rect(0, 0, self.window_width, self.window_height)

        self.update_view_rect()

    ''' to get the appropriate game screen display size, which is still in ratio 16:9 '''
    def update_view_rect(self):
        # Calculate the maximum 16:9 inner rect
        target_ratio = 16 / 9
        current_ratio = self.window_width / self.window_height

        if current_ratio > target_ratio:
            # Window is wider, so height goes up to max, width is constrained
            new_height = self.window_height
            new_width = int(new_height * target_ratio)
        else:
            # Window is taller, so width goes up to max, height is constrained
            new_width = self.window_width
            new_height = int(new_width / target_ratio)

        # get topleft position of new screen
        x_offset = (self.window_width - new_width) // 2
        y_offset = (self.window_height - new_height) // 2
        self.view_rect = pygame.Rect(x_offset, y_offset, new_width, new_height)

    '''get the mouse position accroading to displaying screen'''
    def get_mouse_pos(self):
        physical_x, physical_y = pygame.mouse.get_pos()
        
        # Protect from outside of view_rect
        relative_x = physical_x - self.view_rect.x
        relative_y = physical_y - self.view_rect.y
        
        virtual_x = relative_x / self.view_rect.w * self.virtual_width
        virtual_y = relative_y / self.view_rect.h * self.virtual_height
        return (virtual_x, virtual_y)

    ''' main game loop '''
    def run(self):
        while self.running:
            events = pygame.event.get()
            for event in events:
                if event.type == pygame.QUIT:
                    self.running = False
                elif event.type == pygame.VIDEORESIZE:
                    self.window_width, self.window_height = self.window_surface.get_size()
                    self.update_view_rect()

            self.state_machine.handle_events(events)
            self.state_machine.update()
            
            # draw game screen
            self.state_machine.draw(self.canvas)
            
            self.window_surface.fill((0, 0, 0)) # BLACK border
            scaled_canvas = pygame.transform.smoothscale(self.canvas, self.view_rect.size)
            self.window_surface.blit(scaled_canvas, self.view_rect.topleft)

            pygame.display.update()
            self.main_clock.tick(self.fps)

        pygame.quit()
        sys.exit()
