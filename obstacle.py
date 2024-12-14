import pygame
import random
from constants import GRID_SIZE, MIN_OBSTACLE_DISTANCE
from snake import Snake
from food import Food


# Obstacle class
class Obstacle:
    def __init__(self):
        self.positions = []
        self.breakable = True
        self.hit_timers = {}

    def generate_position(self, snake_body, food_positions, screen):
        while True:
            position = (
                random.randint(0, screen.get_width() // GRID_SIZE - 1) * GRID_SIZE,
                random.randint(0, screen.get_height() // GRID_SIZE - 1) * GRID_SIZE,
            )

            valid_position = True
            for segment in snake_body:
                distance = (
                    (position[0] - segment[0]) ** 2 + (position[1] - segment[1]) ** 2
                ) ** 0.5
                if distance < MIN_OBSTACLE_DISTANCE * GRID_SIZE:
                    valid_position = False
                    break

            if (
                valid_position
                and position not in [pos[0] for pos in food_positions]
                and position not in self.positions
            ):
                self.positions.append(position)
                break

    def hit(self, position):
        if self.breakable and position in self.positions:
            self.hit_timers[position] = 10  # 10 frames for hit effect
            if self.breakable:
                self.positions.remove(position)

    def draw(self, screen):
        for position in self.positions:
            color = (100, 100, 100)
            if position in self.hit_timers:
                color = (255, 255, 255)  # White color for hit effect
                self.hit_timers[position] -= 1
                if self.hit_timers[position] <= 0:
                    del self.hit_timers[position]
            pygame.draw.rect(
                screen,
                color,
                (
                    position[0],
                    position[1],
                    GRID_SIZE,
                    GRID_SIZE,
                ),
            )
