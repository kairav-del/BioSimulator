from .entity import Entity
from .config import *
import random
import pygame
vec = pygame.math.Vector2


class Healthy(Entity):
    def __init__(self, x, y):
        super().__init__(x, y, DEFAULT_RADIUS, HEALTHY_COLOR, 
                        HEALTHY_VISION, HEALTHY_SPEED, HEALTHY_MAX_FORCE)
        self.energy = random.uniform(DEFAULT_ENERGY * 0.8, DEFAULT_ENERGY * 1.7)

    # MODIFIED: Accepts only NEARBY predators/obstacles
    def calculate_steering(self, nearby_predators, nearby_obstacles):
        """Calculate steering force based on nearby predators and obstacles"""
        steer_force = vec(0, 0)

        # Find nearest predator from the NEARBY list
        nearest_predator = None
        min_pred_dist_sq = self.vision_range ** 2  # Use squared distance
        for pred in nearby_predators:  # Iterate only through nearby ones
            dist_sq = self.pos.distance_squared_to(pred.pos)
            if dist_sq < min_pred_dist_sq:
                nearest_predator = pred
                min_pred_dist_sq = dist_sq

        # Find nearest obstacle from the NEARBY list
        nearest_obstacle = None
        min_obs_dist_sq = self.vision_range ** 2
        for obs in nearby_obstacles:  # Iterate only through nearby ones
            # Ensure obstacle has a center; might need adjustment if obs pos is top-left
            obs_center = vec(obs.rect.center)
            dist_sq = self.pos.distance_squared_to(obs_center)
            if dist_sq < min_obs_dist_sq:
                nearest_obstacle = obs
                min_obs_dist_sq = dist_sq

        # --- Steering Logic (using squared distances for comparison) ---
        min_pred_dist = min_pred_dist_sq ** 0.5 if nearest_predator else float('inf')
        min_obs_dist = min_obs_dist_sq ** 0.5 if nearest_obstacle else float('inf')

        # Prioritize responses
        # Tweak vision range factors based on testing
        if nearest_predator and min_pred_dist < self.vision_range * 0.9:
            flee_force = self.flee(nearest_predator.pos)
            # Panic mode threshold - adjust as needed
            if min_pred_dist < self.vision_range * 0.3:
                flee_force *= 6.5
            steer_force = flee_force
        elif nearest_obstacle and min_obs_dist < self.vision_range * 0.8:
            # Obstacle avoidance priority - adjust multiplier and range
            steer_force = self.flee(vec(nearest_obstacle.rect.center)) * 3.5
        else:
            steer_force = self.wander()

        # Limit force
        if steer_force.length_squared() > self.max_force ** 2:  # Compare squared lengths
            steer_force.scale_to_length(self.max_force)

        return steer_force

    def check_reproduction(self, all_sprites_group, healthy_group):
        """Check if energy allows reproduction and spawn a new blob."""
        if self.energy >= HEALTHY_REPRO_THRESHOLD:
            self.energy *= 0.5  # Cost to reproduce
            spawn_pos = self.pos + vec(random.uniform(-10, 10), random.uniform(-10, 10))
            new_blob = Healthy(spawn_pos.x, spawn_pos.y)
            all_sprites_group.add(new_blob)
            healthy_group.add(new_blob)
            return True
        return False

    def update(self, predators, obstacles, all_sprites_group, healthy_group):
        """Update healthy blob state"""
        # Calculate and apply steering force
        steering_force = self.calculate_steering(predators, obstacles)
        self.apply_force(steering_force)

        # Update position and handle boundaries
        self.base_update()

        # Energy management
        self.energy += HEALTHY_ENERGY_GAIN_RATE

        # Reproduction check
        self.check_reproduction(all_sprites_group, healthy_group)