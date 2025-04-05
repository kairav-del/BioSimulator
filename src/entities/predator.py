from .entity import Entity
from .config import *
import random
import pygame
vec = pygame.math.Vector2


class Predator(Entity):
    def __init__(self, x, y):
        super().__init__(x, y, DEFAULT_RADIUS + 2, PREDATOR_COLOR, 
                         PREDATOR_VISION, PREDATOR_SPEED, PREDATOR_MAX_FORCE)
        self.energy = random.uniform(DEFAULT_ENERGY, DEFAULT_ENERGY * 1.5)
        self.is_diseased = False
        self.disease_timer = 0


    def calculate_steering(self, prey_group, obstacles):
        """Calculate steering force based on nearest prey and obstacles"""
        steer_force = vec(0, 0)
        
        # Find nearest prey
        nearest_prey = None
        min_prey_dist = float('inf')
        for prey in prey_group:
            dist = self.pos.distance_to(prey.pos)
            if dist < self.vision_range and dist < min_prey_dist:
                nearest_prey = prey
                min_prey_dist = dist
        
        # Find nearest obstacle
        nearest_obstacle = None
        min_obs_dist = float('inf')
        for obs in obstacles:
            dist = self.pos.distance_to(vec(obs.rect.center))
            if dist < self.vision_range and dist < min_obs_dist:
                nearest_obstacle = obs
                min_obs_dist = dist
        
        if nearest_obstacle and min_obs_dist < self.vision_range * 0.5:
            steer_force = self.flee(vec(nearest_obstacle.rect.center)) * 1.4
        elif nearest_prey:
            steer_force = self.seek(nearest_prey.pos)
        else:
            steer_force = self.wander() 
            
        if steer_force.length() > self.max_force:
            steer_force.scale_to_length(self.max_force)
            
        return steer_force

    def eat(self, prey_entity):
        """Consume prey, gain energy and fitness."""
        prey_entity.kill() # Remove prey from all groups
        self.energy += PREDATOR_EAT_ENERGY_GAIN

    def check_reproduction(self, all_sprites_group, predator_group):
        """Check if energy allows reproduction and spawn a new predator."""
        if self.energy >= PREDATOR_REPRO_THRESHOLD:
            self.energy *= 0.5 # Cost to reproduce
            spawn_pos = self.pos + vec(random.uniform(-10, 10), random.uniform(-10, 10))
            new_predator = Predator(spawn_pos.x, spawn_pos.y)
            all_sprites_group.add(new_predator)
            predator_group.add(new_predator)
            return True
        return False

    def update(self, prey_group, obstacles, all_sprites_group, predator_group):
        """Calculate steering, apply force, update physics, handle eating/reproduction."""
        # Decide steering force
        steering_force = self.calculate_steering(prey_group, obstacles)
        self.apply_force(steering_force)

        # Decrease energy over time (hunger)
        self.energy -= PREDATOR_HUNGERRATE

        # Call base class update for physics and boundary checks
        self.base_update()

        # --- Check for eating ---
        # More efficient collision check in main loop is often better
        hits = pygame.sprite.spritecollide(self, prey_group, False) # Don't kill prey here, let the eat() method do it
        for victim in hits:
            self.eat(victim)

        # Check for reproduction
        self.check_reproduction(all_sprites_group, predator_group)

