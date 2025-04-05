import pygame
import random
import sys
from src.graph import GraphGenerator
from src.entities.config import *
from src.entities.entity import Entity
from src.entities.healthy import Healthy
from src.entities.predator import Predator
from src.obstacles import Obstacle

pygame.init()
SCREEN = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Bio-Simulation")
clock = pygame.time.Clock()

graph = GraphGenerator(width=200, height=100)

all_sprites = pygame.sprite.Group()
healthy_blobs = pygame.sprite.Group()
predator_blobs = pygame.sprite.Group()
obstacle_sprites = pygame.sprite.Group()

for _ in range(NUM_HEALTHY_START):
    x, y = random.uniform(DEFAULT_RADIUS, SCREEN_WIDTH - DEFAULT_RADIUS), random.uniform(DEFAULT_RADIUS, SCREEN_HEIGHT - DEFAULT_RADIUS)
    blob = Healthy(x, y)
    all_sprites.add(blob)
    healthy_blobs.add(blob)

for _ in range(NUM_PREDATOR_START):
    x, y = random.uniform(DEFAULT_RADIUS, SCREEN_WIDTH - DEFAULT_RADIUS), random.uniform(DEFAULT_RADIUS, SCREEN_HEIGHT - DEFAULT_RADIUS)
    predator = Predator(x, y)
    all_sprites.add(predator)
    predator_blobs.add(predator)

for _ in range(NUM_OBSTACLES):
    w = random.uniform(20, 50)
    h = random.uniform(20, 50)
    x = random.uniform(w/2, SCREEN_WIDTH - w/2)
    y = random.uniform(h/2, SCREEN_HEIGHT - h/2)
    obs = Obstacle(x, y, w, h)
    all_sprites.add(obs)
    obstacle_sprites.add(obs)

running = True

while running:
    dt = clock.tick(FPS) / 1000.0

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                running = False

    for blob in healthy_blobs:
        blob.update(predator_blobs, obstacle_sprites, all_sprites, healthy_blobs)

    for predator in predator_blobs:
        predator.update(healthy_blobs, obstacle_sprites, all_sprites, predator_blobs)

    predator_prey_collisions = pygame.sprite.groupcollide(predator_blobs, healthy_blobs, False, False)

    for predator, eaten_prey_list in predator_prey_collisions.items():
        for prey in eaten_prey_list:
             if hasattr(predator, 'eat'):
                 predator.eat(prey)

    entity_obstacle_collisions = pygame.sprite.groupcollide(all_sprites, obstacle_sprites, False, False)
    for entity, hit_obstacles in entity_obstacle_collisions.items():
         if isinstance(entity, Entity) and not isinstance(entity, Obstacle):
            obstacle = hit_obstacles[0]
            if hasattr(entity, 'pos') and hasattr(entity, 'vel') and hasattr(obstacle, 'pos'):
                obstacle_pos_vec = pygame.math.Vector2(obstacle.pos) if not isinstance(obstacle.pos, pygame.math.Vector2) else obstacle.pos
                push_vector = (entity.pos - obstacle_pos_vec)
                if push_vector.length() > 0:
                    push_vector.normalize_ip()
                    push_vector *= 3
                    entity.pos += push_vector
                entity.vel *= -0.8

    all_mobile_entities = pygame.sprite.Group()
    all_mobile_entities.add(healthy_blobs.sprites())
    all_mobile_entities.add(predator_blobs.sprites())


    SCREEN.fill(BACKGROUND_COLOR)
    all_sprites.draw(SCREEN)

    try:
        font = pygame.font.SysFont(None, 24)
        healthy_count_text = font.render(f"Healthy: {len(healthy_blobs)}", True, HEALTHY_COLOR)
        predator_count_text = font.render(f"Predators: {len(predator_blobs)}", True, PREDATOR_COLOR)
        SCREEN.blit(healthy_count_text, (10, 10))
        SCREEN.blit(predator_count_text, (10, 30))
    except Exception as e:
        print(f"Error displaying info text: {e}")

    graph.update(len(healthy_blobs), len(predator_blobs))

    graph_surface = graph.draw()
    SCREEN.blit(graph_surface, (SCREEN_WIDTH - 220, 20))

    font = pygame.font.SysFont(None, 20)
    labels = [
        ("Healthy", HEALTHY_COLOR),
        ("Predators", PREDATOR_COLOR),
    ]

    for i, (text, color) in enumerate(labels):
        label = font.render(text, True, color)
        SCREEN.blit(label, (SCREEN_WIDTH - 220, 130 + i * 20))

    pygame.display.flip()

pygame.quit()
sys.exit()