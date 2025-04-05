import pygame
from src.entities.config import * # Import constants
vec = pygame.math.Vector2

#@jit(nopython=True)
class Obstacle(pygame.sprite.Sprite):
    def __init__(self, x, y, width, height):
        super().__init__()
        self.pos = vec(x, y)
        self.image = pygame.Surface((width, height))
        self.image.fill(OBSTACLE_COLOR)
        self.rect = self.image.get_rect(center=self.pos)
        # Obstacles are static, but need pos for distance calculations