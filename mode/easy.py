import pygame
from constants import BASE_SPEED, GRID_SIZE, NUM_FOOD
from food import Food


def set_easy_mode(snake, food, screen, obstacle):
    lives = 10
    current_speed = BASE_SPEED + 0.2
    food.positions = []
    while len(food.positions) < 1:
        food.generate_position(snake.body, screen, obstacle.positions)
    return lives, current_speed


def draw_grid(screen):
    grid_color = (50, 50, 50)
    screen_width = screen.get_width()
    screen_height = screen.get_height()
    for x in range(0, screen_width, GRID_SIZE):
        pygame.draw.line(screen, grid_color, (x, 0), (x, screen_height))
    for y in range(0, screen_height, GRID_SIZE):
        pygame.draw.line(screen, grid_color, (0, y), (screen_width, y))
