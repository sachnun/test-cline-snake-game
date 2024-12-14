import pygame

# Initialize Pygame
pygame.init()

# Constants
GRID_SIZE = 20
GRID_WIDTH = 30
GRID_HEIGHT = 20
SCREEN_WIDTH = GRID_SIZE * GRID_WIDTH
SCREEN_HEIGHT = GRID_SIZE * GRID_HEIGHT
BASE_SPEED = 5
BOOST_SPEED = 15
SPEED_INCREMENT = 0.2
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
BLACK = (0, 0, 0)
GRAY = (150, 150, 150)
NUM_FOOD = 5
OBSTACLE_INTERVAL = 10000  # 10 seconds in milliseconds
MIN_OBSTACLE_DISTANCE = 5  # Minimum distance from snake
APPLE_TIME_TO_LIVE = 10  # 10 seconds

# Set up the display
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.RESIZABLE)
pygame.display.set_caption("Snake Game")

# Font setup
font = pygame.font.Font(None, 36)
food_font = pygame.font.Font(None, GRID_SIZE)
