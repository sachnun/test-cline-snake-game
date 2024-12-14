import pygame
import random
from constants import GRID_SIZE, NUM_FOOD
from snake import Snake

# Load the apple image
apple_image = pygame.image.load("apple.png")
apple_image = pygame.transform.scale(apple_image, (GRID_SIZE, GRID_SIZE))


# Food class
class Food:
    def __init__(self):
        self.positions = []

    def generate_position(self, snake_body, screen, obstacle_positions=[]):
        while True:
            position = (
                random.randint(0, screen.get_width() // GRID_SIZE - 1) * GRID_SIZE,
                random.randint(0, screen.get_height() // GRID_SIZE - 1) * GRID_SIZE,
            )
            if (
                position not in snake_body
                and position not in [pos[0] for pos in self.positions]
                and position not in obstacle_positions
            ):
                self.positions.append([position, random.uniform(5, 10)])
                break

    def update(self, time_elapsed):
        for i in range(len(self.positions)):
            self.positions[i][1] -= time_elapsed / 1000
        self.positions = [pos for pos in self.positions if pos[1] > 0]

    def draw(self, screen):
        for position, time_to_live in self.positions:
            alpha = int((time_to_live / 10) * 255)
            alpha = max(0, min(alpha, 255))

            apple_image_copy = apple_image.copy()
            apple_image_copy.set_alpha(alpha)

            food_rect = apple_image_copy.get_rect(
                center=(
                    position[0] + GRID_SIZE // 2,
                    position[1] + GRID_SIZE // 2,
                )
            )
            screen.blit(apple_image_copy, food_rect)
