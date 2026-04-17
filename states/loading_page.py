import pygame
from states.base import StateBase
from function import BLACK

class LoadingState(StateBase):
    def __init__(self, engine):
        super().__init__(engine)
        self.start_font = pygame.font.SysFont(None, 60)
        self.start_color = 255
        self.start_color_detect = True

    def enter(self):
        pass

    def update(self, delta):
        speed = 240 * delta # 2 per frame at 120fps = 240/s
        if self.start_color_detect == True:
            self.start_color -= speed
            if self.start_color < 100:
                self.start_color_detect = False
        else:
            self.start_color += speed
            if self.start_color >= 255:
                self.start_color = 255
                self.start_color_detect = True

    def handle_events(self, events):
        for event in events:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    self.engine.state_machine.change_state("MENU")

    def draw(self, surface):
        start_text_surface = self.start_font.render("Press space to start the game!", True, (self.start_color, self.start_color, self.start_color))
        surface.fill(BLACK)
        surface.blit(start_text_surface, (100, self.engine.virtual_height / 2))
