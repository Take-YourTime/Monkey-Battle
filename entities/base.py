import pygame
from function import WINDOW_WIDTH, WINDOW_HEIGHT

class Entity(pygame.sprite.Sprite):
    """
    Base class for any character or enemy that has life and can take damage.
    """
    def __init__(self):
        super().__init__()
        self.life = 1
        
    def hurt(self, damage=1):
        if self.life > damage:
            self.life -= damage
        else:
            self.life = 0
            self.kill()

class Projectile(pygame.sprite.Sprite):
    """
    Base class for projectiles like Pencil, Stone, Banana.
    """
    def __init__(self):
        super().__init__()
        self.width = 0
        self.height = 0
        self.location = (0, 0)
        self.vector_x = 0
        self.vector_y = 0
        self.multiple = 1
    
    def check_out_of_bounds(self):
        """
        Kill the projectile if it leaves the screen bounds.
        Returns True if killed.
        """
        if (self.location[0] > WINDOW_WIDTH + self.width or 
            self.location[0] < -self.width or 
            self.location[1] > WINDOW_HEIGHT + self.height or 
            self.location[1] < -self.height):
            self.kill()
            return True
        return False

    def is_colliding_with(self, target: pygame.sprite.Sprite):
        """
        Helper method to check mask-based pixel-perfect collision.
        """
        if self.rect.colliderect(target.rect):
            offset = (self.rect.left - target.rect.left, self.rect.top - target.rect.top)
            # Both self and target must have a `mask` attribute defined
            if getattr(target, 'mask', None) and getattr(self, 'mask', None):
                if target.mask.overlap(self.mask, offset):
                    return True
        return False
