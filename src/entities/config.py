

# Screen settings
SCREEN_WIDTH = 900
SCREEN_HEIGHT = 600
FPS = 60 # Higher FPS for smoother visuals

# Colors
BACKGROUND_COLOR = (30, 30, 30)
HEALTHY_COLOR = (0, 255, 0)
PREDATOR_COLOR = (255, 0, 0)
OBSTACLE_COLOR = (128, 128, 128)
DISEASED_COLOR_TINT = (100, 100, 0) # Tint color for diseased

# Entity Base Properties
DEFAULT_RADIUS = 5
MAX_SPEED = 4
MAX_FORCE = 0.2 # Steering force limit
DEFAULT_HEALTH = 100
DEFAULT_ENERGY = 50
FRICTION = 0.98 # Velocity multiplier each frame (closer to 1 = less friction)

# Healthy Blob Properties
HEALTHY_VISION = 120
HEALTHY_SPEED = 3
HEALTHY_MAX_FORCE = 0.15
HEALTHY_REPRO_THRESHOLD = 100 # Energy needed to reproduce
HEALTHY_ENERGY_GAIN_RATE = 0.2 # Slow energy gain over time

# Predator Properties
PREDATOR_VISION = 150
PREDATOR_SPEED = 5
PREDATOR_MAX_FORCE = 0.2
PREDATOR_HUNGERRATE = 0.20 # How fast energy decreases
PREDATOR_EAT_ENERGY_GAIN = 12
PREDATOR_REPRO_THRESHOLD = 120

# Simulation settings
NUM_HEALTHY_START = 60
NUM_PREDATOR_START = 10
NUM_OBSTACLES = 8

