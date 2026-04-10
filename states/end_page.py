import pygame
import sys
from states.base import StateBase
from function import BLACK

class EndState(StateBase):
    def __init__(self, engine):
        super().__init__(engine)

    def draw(self, surface):
        surface.fill(BLACK)
