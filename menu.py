import pygame
from constants import (
    SCREEN_WIDTH,
    SCREEN_HEIGHT,
    BLACK,
    WHITE,
    GREEN,
    font,
    screen,
)

# Game states
MENU = 0
GAME = 1
CREDITS = 2
DIFFICULTY_SELECT = 3

# Menu options
menu_options = ["Start", "Credits", "Exit"]
selected_option = 0

# Difficulty options
difficulty_options = ["Easy", "Medium", "Hard"]
selected_difficulty = 0

# Game state variables
continue_game = False
paused = False


def draw_menu(high_score, continue_game, selected_option):
    screen.fill(BLACK)
    title_text = font.render("Snake Game", True, WHITE)
    title_rect = title_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 4))
    screen.blit(title_text, title_rect)

    small_font = pygame.font.Font(None, 24)
    high_score_text = small_font.render(
        f"High Score: {high_score}", True, (169, 169, 169)
    )
    high_score_rect = high_score_text.get_rect(
        center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 4 + 30)
    )
    screen.blit(high_score_text, high_score_rect)

    menu_items = []
    if continue_game:
        menu_items = ["Continue", "Credits", "Exit"]
    else:
        menu_items = menu_options

    for i, option in enumerate(menu_items):
        text_color = WHITE if i != selected_option else GREEN
        text_surface = font.render(option, True, text_color)
        text_rect = text_surface.get_rect(
            center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + i * 50)
        )
        screen.blit(text_surface, text_rect)


def draw_difficulty_select(selected_difficulty):
    screen.fill(BLACK)
    title_text = font.render("Select Difficulty", True, WHITE)
    title_rect = title_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 4))
    screen.blit(title_text, title_rect)

    for i, option in enumerate(difficulty_options):
        text_color = WHITE if i != selected_difficulty else GREEN
        text_surface = font.render(option, True, text_color)
        text_rect = text_surface.get_rect(
            center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + i * 50)
        )
        screen.blit(text_surface, text_rect)
