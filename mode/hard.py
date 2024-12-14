import pygame
from constants import BASE_SPEED, NUM_FOOD, SCREEN_WIDTH, SCREEN_HEIGHT
from food import Food


def set_hard_mode(snake, food, screen, obstacle):
    lives = 3
    current_speed = BASE_SPEED + 0.4
    food.positions = []
    while len(food.positions) < 6:
        food.generate_position(snake.body, screen, obstacle.positions)

    original_move = snake.move

    def hard_mode_move():
        head_after_move = snake.body[0]
        if (
            head_after_move[0] < 0
            or head_after_move[0] >= SCREEN_WIDTH
            or head_after_move[1] < 0
            or head_after_move[1] >= SCREEN_HEIGHT
        ):
            print("hit")
            snake.body[0] = (
                head_after_move[0] % SCREEN_WIDTH,
                head_after_move[1] % SCREEN_HEIGHT,
            )
            return True

        if not original_move():
            return False
        return True

    snake.move = hard_mode_move
    return lives, current_speed, snake
