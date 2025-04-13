import pygame
import random

# Constants
BALL_RADIUS = 10
PADDLE_WIDTH = 20
PADDLE_HEIGHT = 100
PADDLE1_COLOR = (168, 127, 50)
PADDLE2_COLOR = (106, 86, 168)
SPIN_ACCELERATION = 10

# Initialize the game
pygame.init()
screen = pygame.display.set_mode((1920, 1080))
clock = pygame.time.Clock()
running = True
dt = 0

# Ball setup
ball_pos = pygame.Vector2(screen.get_width() / 2, screen.get_height() / 2)
ball_speed_x = random.choice([250, 500])
ball_speed_y = random.randint(-250, 500)
ball_hitbox = pygame.Rect(0, 0, BALL_RADIUS * 2, BALL_RADIUS * 2)

# Unrotated base paddle
paddle1_base = pygame.Surface((PADDLE_WIDTH, PADDLE_HEIGHT))
paddle1_base.fill(PADDLE1_COLOR)
paddle2_base = pygame.Surface((PADDLE_WIDTH, PADDLE_HEIGHT))
paddle2_base.fill(PADDLE2_COLOR)

# Paddle rectangles
paddle1_rect = pygame.Rect(50, screen.get_height() / 2 - 50, PADDLE_WIDTH, PADDLE_HEIGHT)
paddle2_rect = pygame.Rect(1870, screen.get_height() / 2 - 50, PADDLE_WIDTH, PADDLE_HEIGHT)


# Spinning vars
paddle1_spinning = False
paddle2_spinning = False
paddle1_spin_speed = 0  # Degrees per second 
paddle2_spin_speed = 0  # Degrees per second 
paddle2_angle = 0
paddle1_angle = 0

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
        paddle1_rect.y -= 6
    if keys[pygame.K_s]:
        paddle1_rect.y += 6
    if keys[pygame.K_UP]:
        paddle2_rect.y -= 6
    if keys[pygame.K_DOWN]:
        paddle2_rect.y += 6
    if keys[pygame.K_LALT]:  # Auto-track player1
        paddle1_rect.y = ball_pos.y
    if keys[pygame.K_SPACE]:  # Auto-track player2
        paddle2_rect.y = ball_pos.y
    paddle1_rect.clamp_ip(screen.get_rect())
    paddle2_rect.clamp_ip(screen.get_rect())

# Spin paddles
    if paddle1_spinning:
        paddle1_spin_speed += SPIN_ACCELERATION * dt
        paddle1_angle += paddle1_spin_speed * dt
    
    if paddle2_spinning:
        paddle2_spin_speed += SPIN_ACCELERATION * dt
        paddle2_angle += paddle2_spin_speed * dt

    # Update paddle rotations and rectangles
    paddle1_rotated = pygame.transform.rotate(paddle1_base, paddle1_angle)
    paddle2_rotated = pygame.transform.rotate(paddle2_base, paddle2_angle)
    paddle1_rect = paddle1_rotated.get_rect(center=paddle1_rect.center)
    paddle2_rect = paddle2_rotated.get_rect(center=paddle2_rect.center)

    # Ball movement
    if ball_pos.y > 1080 - BALL_RADIUS or ball_pos.y < BALL_RADIUS:
        ball_speed_y = -ball_speed_y
    if ball_pos.x < 5 or ball_pos.x > 1915:
        ball_speed_x = -ball_speed_x
        paddle1_spinning = False 
        paddle2_spinning = False 
        paddle1_spin_speed = 0  
        paddle2_spin_speed = 0   

    ball_pos.x += ball_speed_x * dt
    ball_pos.y += ball_speed_y * dt
    ball_hitbox.center = (ball_pos.x, ball_pos.y)

    # Check collisions
    if ball_hitbox.colliderect(paddle1_rect):
        ball_speed_x = -ball_speed_x
        paddle1_spinning = True
        if paddle1_spin_speed == 0:
            paddle1_spin_speed = 100
            paddle1_rotated = pygame.transform.rotate(paddle1_base, paddle1_angle)
    if ball_hitbox.colliderect(paddle2_rect):
        ball_speed_x = -ball_speed_x
        paddle2_spinning = True
        if paddle2_spin_speed == 0:
            paddle2_spin_speed = 100

    # Draw rotated paddles
    screen.blit(paddle1_rotated, paddle1_rect.topleft)
    screen.blit(paddle2_rotated, paddle2_rect.topleft)

    # Draw ball
    pygame.draw.circle(screen, "black", ball_pos, BALL_RADIUS)

    pygame.display.flip()
    dt = clock.tick(144) / 1000

pygame.quit()