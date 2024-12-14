import pygame
from constants import (
    SCREEN_WIDTH,
    SCREEN_HEIGHT,
    GRID_SIZE,
    WHITE,
    GREEN,
    RED,
)


class Snake:
    def __init__(self, difficulty):
        self.body = [(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)]
        self.direction = (1, 0)
        self.last_direction = (1, 0)
        self.last_direction_change_time = 0
        self.previous_body = []
        self.difficulty = difficulty

    def change_direction(self, direction):
        self.last_direction = self.direction
        self.direction = direction
        self.last_direction_change_time = pygame.time.get_ticks()

    def move(self):
        self.previous_body = list(self.body)
        head = self.body[0]
        new_head = (
            head[0] + self.direction[0] * GRID_SIZE,
            head[1] + self.direction[1] * GRID_SIZE,
        )

        if self.difficulty != 2:
            # Wrap around the screen edges
            if new_head[0] >= SCREEN_WIDTH:
                new_head = (0, new_head[1])
            elif new_head[0] < 0:
                new_head = (SCREEN_WIDTH - GRID_SIZE, new_head[1])
            if new_head[1] >= SCREEN_HEIGHT:
                new_head = (new_head[0], 0)
            elif new_head[1] < 0:
                new_head = (new_head[0], SCREEN_HEIGHT - GRID_SIZE)

        self.body.insert(0, new_head)
        self.body.pop()
        return False

    def grow(self):
        head = self.body[0]
        new_head = (
            head[0] + self.direction[0] * GRID_SIZE,
            head[1] + self.direction[1] * GRID_SIZE,
        )
        self.body.insert(0, new_head)

    def check_tail_collision(self):
        head = self.body[0]
        if not self.previous_body:
            return False
        if len(self.previous_body) < 2:
            return False

        return head == self.previous_body[1]

    def check_wall_collision(self):
        head = self.body[0]
        if (
            head[0] < 0
            or head[0] >= SCREEN_WIDTH
            or head[1] < 0
            or head[1] >= SCREEN_HEIGHT
        ):
            return True
        return False

    def draw(self, screen, color=None):
        if color is None:
            head_color = RED
            body_color = GREEN
            tail_color = WHITE
        else:
            head_color = color
            body_color = color
            tail_color = color

        for i, segment in enumerate(self.body):
            if i > 0 and i < len(self.body) - 1:  # Body
                pygame.draw.rect(
                    screen, body_color, (segment[0], segment[1], GRID_SIZE, GRID_SIZE)
                )
                pygame.draw.rect(
                    screen, (0, 0, 0), (segment[0], segment[1], GRID_SIZE, GRID_SIZE), 1
                )
            elif i == len(self.body) - 1:  # Tail
                pygame.draw.rect(
                    screen, tail_color, (segment[0], segment[1], GRID_SIZE, GRID_SIZE)
                )
                pygame.draw.rect(
                    screen, (0, 0, 0), (segment[0], segment[1], GRID_SIZE, GRID_SIZE), 1
                )

        if len(self.body) > 0:  # Head
            head = self.body[0]
            pygame.draw.rect(
                screen, head_color, (head[0], head[1], GRID_SIZE, GRID_SIZE)
            )
            pygame.draw.rect(
                screen, (0, 0, 0), (head[0], head[1], GRID_SIZE, GRID_SIZE), 1
            )
