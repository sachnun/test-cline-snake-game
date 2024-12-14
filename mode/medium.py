import pygame
from constants import BASE_SPEED, NUM_FOOD
from food import Food


def set_medium_mode(snake, food, screen, obstacle):
    lives = 5
    current_speed = BASE_SPEED + 0.3
    food.positions = []
    while len(food.positions) < 3:
        food.generate_position(snake.body, screen, obstacle.positions)
    return lives, current_speed
