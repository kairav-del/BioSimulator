import pygame
import random
import numpy as np
from .config import * 

vec = pygame.math.Vector2



class Entity(pygame.sprite.Sprite):
    def __init__(self, x, y, radius, color, vision_range, max_speed, max_force):
        super().__init__()
        self.pos = vec(x, y)
        self.vel = vec(random.uniform(-1, 1), random.uniform(-1, 1)).normalize() * random.uniform(0, max_speed) # Velocity vector
        self.acc = vec(0, 0)
        self.radius = radius
        self.color = color
        self.vision_range = vision_range
        self.max_speed = max_speed
        self.max_force = max_force

        self.health = DEFAULT_HEALTH
        self.energy = DEFAULT_ENERGY

        self.image = pygame.Surface((self.radius * 2, self.radius * 2), pygame.SRCALPHA)
        pygame.draw.circle(self.image, self.color, (self.radius, self.radius), self.radius)
        self.rect = self.image.get_rect(center=self.pos)
        self.original_image = self.image 
        self.orignal_max_speed = self.max_speed


    def apply_force(self, force):
        """Adds a force vector to the acceleration."""
        self.acc += force

    def seek(self, target_pos):
        """Calculates steering force towards a target position."""
        desired = (target_pos - self.pos)
        if desired.length() == 0: return vec(0,0) 
        desired.scale_to_length(self.max_speed)
        steer = (desired - self.vel)
        if steer.length() > self.max_force:
            steer.scale_to_length(self.max_force)
        return steer

    def flee(self, target_pos):
        """Calculates steering force away from a target position."""
        return -self.seek(target_pos) 

    def wander(self):
        """Calculates a small random steering force."""

        steer = vec(random.uniform(-1, 1), random.uniform(-1, 1))
        steer.scale_to_length(self.max_force * 2.5)
        return steer

    def get_nearby_entities(self, entity_group):
        """Find entities within vision range."""
        nearby = []
        for entity in entity_group:
            if entity != self:
                dist_sq = (self.pos - entity.pos).length_squared()
                if dist_sq < self.vision_range**2:
                    nearby.append(entity)
        return nearby

    def get_nearest_entity(self, entity_group):
       """Find the closest entity in a group within vision range."""
       nearest = None
       min_dist_sq = self.vision_range**2
       for entity in entity_group:
           if entity != self:
               dist_sq = (self.pos - entity.pos).length_squared()
               if dist_sq < min_dist_sq:
                   min_dist_sq = dist_sq
                   nearest = entity
       return nearest

    def base_update(self, dt=1):
        """Core physics update, boundary handling, and status checks. dt is delta time (optional)."""

        self.vel += self.acc
        self.vel *= FRICTION
        if self.vel.length() > self.max_speed:
            self.vel.scale_to_length(self.max_speed)

        self.pos += self.vel * dt

        self.acc *= 0

        if self.pos.x > SCREEN_WIDTH + self.radius:
            self.pos.x = -self.radius
        elif self.pos.x < -self.radius:
            self.pos.x = SCREEN_WIDTH + self.radius
        if self.pos.y > SCREEN_HEIGHT + self.radius:
            self.pos.y = -self.radius
        elif self.pos.y < -self.radius:
            self.pos.y = SCREEN_HEIGHT + self.radius

        self.rect.center = (int(self.pos.x), int(self.pos.y))

        if self.energy <= 0 or self.health <= 0:
             self.kill()


    def decide_action(self, **kwargs):
        raise NotImplementedError

    def update(self, **kwargs):
         raise NotImplementedError