import pygame
from constants import SCREEN_WIDTH, SCREEN_HEIGHT, BLACK, WHITE, GRAY, font


def draw_credits(screen):
    screen.fill(BLACK)
    credits_font = pygame.font.Font(None, 60)
    credits_text = credits_font.render("Dakunesu & Gemini AI", True, WHITE)
    credits_rect = credits_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))
    screen.blit(credits_text, credits_rect)
    back_font = pygame.font.Font(None, 24)
    back_text = back_font.render("Press any key to go back", True, GRAY)
    back_rect = back_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT * 3 // 4))
    screen.blit(back_text, back_rect)
