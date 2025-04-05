import pygame
import collections


class GraphGenerator:
    def __init__(self, width=200, height=100, max_points=100):
        self.width = width
        self.height = height
        self.max_points = max_points
        self.surface = pygame.Surface((width, height))
        
        self.healthy_history = collections.deque(maxlen=max_points)
        self.predator_history = collections.deque(maxlen=max_points)
        
        self.healthy_color = (0, 255, 0)  # Green
        self.predator_color = (255, 0, 0)  # Red
        self.background = (30, 30, 30)  # Dark grey

    def update(self, healthy_count, predator_count):
        """Add new data points"""
        self.healthy_history.append(healthy_count)
        self.predator_history.append(predator_count)

    def draw(self):
        """Generate and return the graph surface"""

        self.surface.fill(self.background)
        

        if len(self.healthy_history) > 0:
            max_value = max(
                max(self.healthy_history),
                max(self.predator_history),
            )
            scale_y = (self.height - 10) / max(max_value, 1)
            scale_x = self.width / self.max_points
        
            for i in range(4):
                y = int(self.height * (i / 3))
                pygame.draw.line(self.surface, (50, 50, 50), 
                               (0, y), (self.width, y), 1)

            self._draw_line(self.healthy_history, self.healthy_color, scale_x, scale_y)
            self._draw_line(self.predator_history, self.predator_color, scale_x, scale_y)

        return self.surface
    def _draw_line(self, data_points, color, scale_x, scale_y):
        """Helper method to draw a single line graph"""
        if len(data_points) > 1:
            points = [(int(i * scale_x), 
                      int(self.height - (val * scale_y))) 
                     for i, val in enumerate(data_points)]
            pygame.draw.lines(self.surface, color, False, points, 2)
