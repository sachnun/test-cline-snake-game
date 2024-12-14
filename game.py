import pygame
import random
from constants import (
    SCREEN_WIDTH,
    SCREEN_HEIGHT,
    BLACK,
    WHITE,
    GREEN,
    RED,
    font,
    BASE_SPEED,
    BOOST_SPEED,
    SPEED_INCREMENT,
    screen,
    GRID_SIZE,
)
from snake import Snake
from food import Food
from obstacle import Obstacle
from mode.easy import set_easy_mode, draw_grid
from mode.medium import set_medium_mode
from mode.hard import set_hard_mode
from credits import draw_credits
from menu import (
    MENU,
    GAME,
    CREDITS,
    DIFFICULTY_SELECT,
    menu_options,
    selected_option,
    difficulty_options,
    selected_difficulty,
    continue_game,
    paused,
    draw_menu,
    draw_difficulty_select,
)

DIRECTION_CHANGE_DELAY = 100


def load_high_score():
    try:
        with open("high_score.txt", "r") as file:
            return int(file.read())
    except FileNotFoundError:
        return 0
    except ValueError:
        return 0


def save_high_score(score):
    with open("high_score.txt", "w") as file:
        file.write(str(score))


# Game setup
snake = Snake(0)  # Initialize with a default difficulty
food = Food()
obstacle = Obstacle()
clock = pygame.time.Clock()
score = 0
current_speed = BASE_SPEED
last_obstacle_time = 0
lives = 10  # Initialize lives
hit_timer = 0
blink_interval = 100
blink_count = 0
obstacle_interval = 10000
high_score = 0

# Game states
current_state = MENU

# Game loop
running = True
game_over = False
high_score = load_high_score()
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if current_state == MENU:
                if event.key == pygame.K_UP:
                    selected_option = (selected_option - 1) % len(
                        menu_options
                        if not continue_game
                        else ["Continue", "Credits", "Exit"]
                    )
                elif event.key == pygame.K_DOWN:
                    selected_option = (selected_option + 1) % len(
                        menu_options
                        if not continue_game
                        else ["Continue", "Credits", "Exit"]
                    )
                elif event.key == pygame.K_RETURN:
                    if continue_game:
                        if selected_option == 0:
                            current_state = GAME
                            continue_game = False
                        elif selected_option == 1:
                            current_state = CREDITS
                        elif selected_option == 2:
                            running = False
                    else:
                        if selected_option == 0:
                            current_state = DIFFICULTY_SELECT
                        elif selected_option == 1:
                            current_state = CREDITS
                        elif selected_option == 2:
                            running = False
            elif current_state == CREDITS:
                current_state = MENU
            elif current_state == DIFFICULTY_SELECT:
                if event.key == pygame.K_UP:
                    selected_difficulty = (selected_difficulty - 1) % len(
                        difficulty_options
                    )
                elif event.key == pygame.K_DOWN:
                    selected_difficulty = (selected_difficulty + 1) % len(
                        difficulty_options
                    )
                elif event.key == pygame.K_RETURN:
                    current_state = GAME
                    snake = Snake(selected_difficulty)
                    if selected_difficulty == 0:  # Easy
                        lives, current_speed = set_easy_mode(
                            snake, food, screen, obstacle
                        )
                    elif selected_difficulty == 1:  # Medium
                        lives, current_speed = set_medium_mode(
                            snake, food, screen, obstacle
                        )
                    elif selected_difficulty == 2:  # Hard
                        lives, current_speed, snake = set_hard_mode(
                            snake, food, screen, obstacle
                        )
                elif event.key == pygame.K_ESCAPE or event.key == pygame.K_BACKSPACE:
                    current_state = MENU

            elif current_state == GAME:
                if game_over:
                    current_state = MENU
                    if score > high_score:
                        high_score = score
                        save_high_score(high_score)
                    game_over = False
                    snake = Snake(0)  # Reset with default difficulty
                    food = Food()
                    obstacle = Obstacle()
                    score = 0
                    current_speed = BASE_SPEED
                    last_obstacle_time = 0
                    lives = 3  # Reset lives
                    hit_timer = 0
                    blink_count = 0
                else:
                    if event.key == pygame.K_UP:
                        snake.change_direction((0, -1))
                        if paused:
                            paused = False
                    if event.key == pygame.K_DOWN:
                        snake.change_direction((0, 1))
                        if paused:
                            paused = False
                    if event.key == pygame.K_LEFT:
                        snake.change_direction((-1, 0))
                        if paused:
                            paused = False
                    if event.key == pygame.K_RIGHT:
                        snake.change_direction((1, 0))
                        if paused:
                            paused = False
                    if event.key == pygame.K_SPACE:
                        current_speed = BOOST_SPEED
                        if paused:
                            paused = False
                    if event.key == pygame.K_ESCAPE:
                        if not paused:
                            paused = True
                            current_state = MENU
                            continue_game = True
                        else:
                            paused = False
                            current_state = GAME
                            continue_game = False
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_SPACE:
                current_speed = BASE_SPEED

    if current_state == MENU:
        draw_menu(high_score, continue_game, selected_option)
    elif current_state == CREDITS:
        draw_credits(screen)
    elif current_state == DIFFICULTY_SELECT:
        draw_difficulty_select(selected_difficulty)
    elif current_state == GAME:
        if not game_over and not paused:
            # Obstacle generation
            if pygame.time.get_ticks() - last_obstacle_time >= obstacle_interval:
                obstacle.generate_position(
                    snake.body, [pos[0] for pos in food.positions], screen
                )
                last_obstacle_time = pygame.time.get_ticks()
                obstacle_interval = random.randint(3000, 15000)

            time_elapsed = clock.get_time()
            food.update(time_elapsed)
            for i, position_data in enumerate(food.positions):
                position = position_data[0]
                if snake.body[0] == position:
                    snake.grow()
                    food.positions.pop(i)
                    score += 1
                    if selected_difficulty == 0:
                        while len(food.positions) < 1:
                            food.generate_position(
                                snake.body, screen, obstacle.positions
                            )
                    elif selected_difficulty == 1:
                        while len(food.positions) < 3:
                            food.generate_position(
                                snake.body, screen, obstacle.positions
                            )
                    elif selected_difficulty == 2:
                        while len(food.positions) < 6:
                            food.generate_position(
                                snake.body, screen, obstacle.positions
                            )
                    break

            if snake.move():
                lives -= 1
                hit_timer = pygame.time.get_ticks()
                blink_count = 0
                if lives <= 0:
                    game_over = True

            if (
                pygame.time.get_ticks() - snake.last_direction_change_time
                > DIRECTION_CHANGE_DELAY
            ):
                if (
                    selected_difficulty == 1 or selected_difficulty == 2
                ):  # Medium or Hard
                    if snake.check_tail_collision():
                        lives -= 1
                        hit_timer = pygame.time.get_ticks()
                        blink_count = 0
                        if lives <= 0:
                            game_over = True
                else:  # Easy
                    if snake.check_tail_collision():
                        lives -= 1
                        hit_timer = pygame.time.get_ticks()
                        blink_count = 0
                        if lives <= 0:
                            game_over = True

            obstacle_hit = False
            for position in obstacle.positions:
                if snake.body[0] == position:
                    obstacle.hit(position)
                    obstacle_hit = True
                    break
            if obstacle_hit:
                lives -= 1
                hit_timer = pygame.time.get_ticks()
                blink_count = 0
                if lives <= 0:
                    game_over = True

        screen.fill(BLACK)

        # Draw grid
        if selected_difficulty == 0:
            draw_grid(screen)

        # Draw border for hard mode
        if selected_difficulty == 2:
            pygame.draw.rect(
                screen, (128, 128, 128), (0, 0, SCREEN_WIDTH, SCREEN_HEIGHT), 5
            )

        # Draw snake with blinking effect
        if hit_timer > 0 and blink_count < 6:
            if (
                pygame.time.get_ticks() - hit_timer
            ) % blink_interval < blink_interval / 2:
                snake.draw(screen, WHITE)  # Draw snake in white during blink
            else:
                snake.draw(screen)  # Draw snake in normal color
            if pygame.time.get_ticks() - hit_timer >= blink_interval:
                hit_timer = pygame.time.get_ticks()
                blink_count += 1
        else:
            snake.draw(screen)

        food.draw(screen)
        obstacle.draw(screen)

        # Display score
        apple_image = pygame.image.load("apple.png")
        apple_image = pygame.transform.scale(apple_image, (20, 20))
        screen.blit(apple_image, (SCREEN_WIDTH - 110, 10))
        score_text = font.render(f"  x {score}", True, WHITE)
        screen.blit(score_text, (SCREEN_WIDTH - 90, 10))

        # Display lives
        heart_image = pygame.image.load("heart.png")
        heart_image = pygame.transform.scale(heart_image, (20, 20))
        for i in range(lives):
            screen.blit(heart_image, (10 + i * 25, 10))

        if game_over:
            # Draw game over modal
            modal_width = 300
            modal_height = 150
            modal_x = (SCREEN_WIDTH - modal_width) // 2
            modal_y = (SCREEN_HEIGHT - modal_height) // 2
            pygame.draw.rect(
                screen, WHITE, (modal_x, modal_y, modal_width, modal_height)
            )

            text_surface = font.render("Game Over", True, BLACK)
            text_rect = text_surface.get_rect(center=(SCREEN_WIDTH // 2, modal_y + 40))
            screen.blit(text_surface, text_rect)

            # Display high score
            high_score_text = font.render(f"High Score: {high_score}", True, BLACK)
            high_score_rect = high_score_text.get_rect(
                center=(SCREEN_WIDTH // 2, modal_y + 70)
            )
            screen.blit(high_score_text, high_score_rect)

            restart_text = font.render("Press any key to restart", True, BLACK)
            restart_rect = restart_text.get_rect(
                center=(SCREEN_WIDTH // 2, modal_y + 100)
            )
            screen.blit(restart_text, restart_rect)

        if paused:
            pause_text = font.render("Paused", True, WHITE)
            pause_rect = pause_text.get_rect(
                center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)
            )
            screen.blit(pause_text, pause_rect)

    base_speed_with_score = BASE_SPEED + (score * SPEED_INCREMENT)
    if current_speed != BOOST_SPEED:
        current_speed = base_speed_with_score
    pygame.display.flip()
    clock.tick(current_speed)

pygame.quit()
