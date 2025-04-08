import pygame
import random

# Constants
BALL_RADIUS = 10
PADDLE_WIDTH = 20
PADDLE_HEIGHT = 100
PADDLE1_COLOR = (168, 127, 50)
PADDLE2_COLOR = (106, 86, 168)

# Initialize the game
pygame.init()
screen = pygame.display.set_mode((1920,1080))
clock = pygame.time.Clock()
running = True
dt = 0

# Ball setup
ball_pos = pygame.Vector2(screen.get_width() / 2, screen.get_height() / 2)
ball_speed_x = random.choice([250, 500])
ball_speed_y = random.randint(-250, 500)

# Unrotated base paddle
paddle1_base = pygame.Surface((PADDLE_WIDTH,PADDLE_HEIGHT))
paddle1_base.fill(PADDLE1_COLOR)
paddle2_base = pygame.Surface((PADDLE_WIDTH,PADDLE_HEIGHT))
paddle2_base.fill(PADDLE2_COLOR)

# Rects to position -- easier to deal with collisions then to strictly use Surface
player1 = pygame.Rect(50, screen.get_height() / 2 - 50, PADDLE_WIDTH, PADDLE_HEIGHT)  # Left paddle
player2 = pygame.Rect(1870, screen.get_height() / 2 - 50, PADDLE_WIDTH, PADDLE_HEIGHT)  # Right paddle

# Rotation angles
paddle1_angle = 0
paddle2_angle = 0

# Initialize paddles for rotation
paddle1_rotated = paddle1_base
paddle2_rotated = paddle2_base


# Game loop
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    screen.fill("blue")

    # Player movement
    keys = pygame.key.get_pressed()
    if keys[pygame.K_w]:
        player1.y -= 6
    if keys[pygame.K_s]:
        player1.y += 6
    if keys[pygame.K_UP]:
        player2.y -= 6
    if keys[pygame.K_DOWN]:
        player2.y += 6
    player1.clamp_ip(screen.get_rect())
    player2.clamp_ip(screen.get_rect())
    # Player 1: W/S
    # Player 2: UP/DOWN

    # Ball movement
    # Update ball_pos, check top/bottom bounce, reset if off left/right
    # Move the ball
    if ball_pos.y > 1080 - BALL_RADIUS or ball_pos.y < BALL_RADIUS:
        ball_speed_y = -ball_speed_y
    if ball_pos.x < 5 or ball_pos.x > 1915:
        ball_speed_x = -ball_speed_x
    ball_pos.x += ball_speed_x * dt
    ball_pos.y += ball_speed_y * dt
    # Ball hitbox
    ball_hitbox = pygame.Rect(ball_pos.x - BALL_RADIUS, ball_pos.y - BALL_RADIUS, BALL_RADIUS * 2, BALL_RADIUS * 2)  # 20x20 bounding box
    if ball_hitbox.colliderect(player1):
        ball_speed_x = -ball_speed_x
        paddle1_angle += 30
        paddle1_rotated = pygame.transform.rotate(paddle1_base, paddle1_angle)
    if ball_hitbox.colliderect(player2):
        ball_speed_x = -ball_speed_x
        paddle2_angle += 30
        paddle2_rotated = pygame.transform.rotate(paddle2_base, paddle2_angle)
    paddle1_rect = paddle1_rotated.get_rect(center=player1.center)
    paddle2_rect = paddle2_rotated.get_rect(center=player2.center)


    # Draw rotated paddles
    screen.blit(paddle1_rotated, paddle1_rect.topleft)
    screen.blit(paddle2_rotated, paddle2_rect.topleft)
        # BALL_RADIUS += 1
        # increase ball size each hit

    
    # Render
    pygame.draw.circle(screen, "black", ball_pos, BALL_RADIUS)
    pygame.draw.rect(screen, "black", player1)
    pygame.draw.rect(screen, "black", player2)

    pygame.display.flip()
    dt = clock.tick(144) / 1000

pygame.quit()