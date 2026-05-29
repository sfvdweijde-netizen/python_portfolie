import pygame
import random
import sys

# 1. Initialize Pygame
pygame.init()

# Screen configurations (Classic retro arcade aspect ratio)
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Retro 1982 Arcade Shooter - GitHub Edition")
clock = pygame.time.Clock()

# Classic Retro Colors (Monochrome / Black & White)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)

# Player configuration (The shooting device)
PLAYER_WIDTH = 40
PLAYER_HEIGHT = 20
player_speed = 8

# The straight horizontal line from the 1982 classics
LINE_Y = 550

# Bullet configurations
BULLET_SPEED = -12
SHOOT_DELAY = 15  # Lower value equals faster automatic firing rate

# Enemy configurations (The flying discs)
ENEMY_SPEED_Y = 1.5  # Calm descending speed

# Font configurations
FONT_LARGE = pygame.font.SysFont("Courier", 50, bold=True)
FONT_MEDIUM = pygame.font.SysFont("Courier", 35, bold=True)
FONT_SMALL = pygame.font.SysFont("Courier", 24)

# Game states: "START_SCREEN", "PLAYING", "GAME_OVER"
game_state = "START_SCREEN"


def reset_game():
    """Resets all game variables for a new playthrough."""
    global player_x, player_y, bullets, enemies, shoot_timer, spawn_timer, score
    player_x = SCREEN_WIDTH // 2
    player_y = 530
    bullets = []
    enemies = []
    shoot_timer = 0
    spawn_timer = 0
    score = 0


# Initialize the first game state parameters
reset_game()

# Main Game Loop
running = True
while running:
    # Always clear the screen with a pure black background
    screen.fill(BLACK)

    # ------------------ STATE 1: START SCREEN ------------------
    if game_state == "START_SCREEN":
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:  # SPACE BAR starts the game
                    reset_game()
                    game_state = "PLAYING"

        # Render Start Screen Text
        title_text = FONT_LARGE.render("RETRO SHOOTER 1982", True, WHITE)
        start_text = FONT_SMALL.render("PRESS SPACE TO START", True, WHITE)
        controls_text = FONT_SMALL.render("CONTROLS: A/D OR ARROW KEYS", True, WHITE)

        # Center the text elements horizontally
        screen.blit(title_text, (SCREEN_WIDTH // 2 - title_text.get_width() // 2, 200))
        screen.blit(start_text, (SCREEN_WIDTH // 2 - start_text.get_width() // 2, 350))
        screen.blit(controls_text, (SCREEN_WIDTH // 2 - controls_text.get_width() // 2, 420))

    # ------------------ STATE 2: PLAYING STATE ------------------
    elif game_state == "PLAYING":
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        # Input Handling: Support both Arrow Keys and A/D keys
        keys = pygame.key.get_pressed()
        if (keys[pygame.K_LEFT] or keys[pygame.K_a]) and player_x > 0:
            player_x -= player_speed
        if (keys[pygame.K_RIGHT] or keys[pygame.K_d]) and player_x < SCREEN_WIDTH - PLAYER_WIDTH:
            player_x += player_speed

        # AUTOMATIC AUTO-FIRE SYSTEM
        shoot_timer += 1
        if shoot_timer >= SHOOT_DELAY:
            bullets.append([player_x + PLAYER_WIDTH // 2 - 2, player_y])
            shoot_timer = 0

        # Draw the static horizontal vector line
        pygame.draw.line(screen, WHITE, (0, LINE_Y), (SCREEN_WIDTH, LINE_Y), 3)

        # Draw the Player (Arcade wireframe style)
        pygame.draw.rect(screen, WHITE, (player_x, player_y, PLAYER_WIDTH, PLAYER_HEIGHT), 2)
        pygame.draw.rect(screen, WHITE, (player_x + 15, player_y - 8, 10, 8))  # Blaster barrel

        # Enemy Spawning Management
        spawn_timer += 1
        if spawn_timer > 45:
            enemy_x = random.randint(50, SCREEN_WIDTH - 50)
            enemy_speed_x = random.choice([-2, -1, 1, 2])  # Random horizontal zigzag direction
            enemies.append([enemy_x, 0, enemy_speed_x, ENEMY_SPEED_Y])
            spawn_timer = 0

        # Update and draw projectiles
        for bullet in bullets[:]:
            bullet[1] += BULLET_SPEED
            pygame.draw.rect(screen, WHITE, (bullet[0], bullet[1], 4, 12))
            if bullet[1] < 0:
                bullets.remove(bullet)

        # Update and draw enemies (zigzag movements)
        for enemy in enemies[:]:
            enemy[0] += enemy[2]  # Move horizontally (X)
            enemy[1] += enemy[3]  # Move vertically (Y)

            # Bounce enemies back when hitting screen boundaries
            if enemy[0] <= 16 or enemy[0] >= SCREEN_WIDTH - 16:
                enemy[2] = -enemy[2]

            # Render enemy disc (Retro concentric circles)
            pygame.draw.circle(screen, WHITE, (int(enemy[0]), int(enemy[1])), 16, 2)
            pygame.draw.circle(screen, WHITE, (int(enemy[0]), int(enemy[1])), 6, 1)

            # Collision Check: Bullet vs Enemy Disc
            for bullet in bullets[:]:
                if (enemy[0] - 16 < bullet[0] < enemy[0] + 16) and (enemy[1] - 16 < bullet[1] < enemy[1] + 16):
                    if enemy in enemies:
                        enemies.remove(enemy)
                        score += 10
                    if bullet in bullets:
                        bullets.remove(bullet)

            # Penalty if an enemy breaks through the baseline
            if enemy[1] >= LINE_Y:
                if enemy in enemies:
                    enemies.remove(enemy)
                    score -= 5

        # Trigger Game Over condition if score drops below zero
        if score < 0:
            game_state = "GAME_OVER"

        # Display current active score
        score_text = FONT_SMALL.render(f"SCORE: {score}", True, WHITE)
        screen.blit(score_text, (20, 20))

    # ------------------ STATE 3: GAME OVER SCREEN ------------------
    elif game_state == "GAME_OVER":
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:  # 'R' key restarts the session
                    reset_game()
                    game_state = "PLAYING"
                if event.key == pygame.K_q:  # 'Q' key quits the software
                    running = False

        # Render Game Over screen texts
        game_over_title = FONT_LARGE.render("GAME OVER", True, WHITE)
        restart_prompt = FONT_SMALL.render("PRESS 'R' TO PLAY AGAIN", True, WHITE)
        quit_prompt = FONT_SMALL.render("PRESS 'Q' TO QUIT", True, WHITE)

        screen.blit(game_over_title, (SCREEN_WIDTH // 2 - game_over_title.get_width() // 2, 200))
        screen.blit(restart_prompt, (SCREEN_WIDTH // 2 - restart_prompt.get_width() // 2, 350))
        screen.blit(quit_prompt, (SCREEN_WIDTH // 2 - quit_prompt.get_width() // 2, 410))

    # Refresh screen output & cap at fluid 60 frames per second
    pygame.display.flip()
    clock.tick(60)

pygame.quit()
sys.exit()
