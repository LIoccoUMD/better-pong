import pygame
import random

def inverse(num):
    return -num

pygame.init()
screen = pygame.display.set_mode((1920,1080))
clock = pygame.time.Clock()
running = True
dt = 0

# Ball setup
ball_pos = pygame.Vector2(screen.get_width() / 2, screen.get_height() / 2)
ball_speed_x = random.choice([250, 500])
ball_speed_y = random.randint(-250, 500)

# Paddle setup (Rect objects)
player1 = pygame.Rect(50, screen.get_height() / 2 - 50, 20, 100)  # Left paddle
player2 = pygame.Rect(1870, screen.get_height() / 2 - 50, 20, 100)  # Right paddle

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    screen.fill("blue")

    # Paddle movement (fill this in)
    keys = pygame.key.get_pressed()
    if keys[pygame.K_w]:
        player1.y -= 10
    if keys[pygame.K_s]:
        player1.y += 10
    if keys[pygame.K_UP]:
        player2.y -= 10
    if keys[pygame.K_DOWN]:
        player2.y += 10
    # Player 1: W/S
    # Player 2: UP/DOWN

    # Ball movement (fill this in)
    # Update ball_pos, check top/bottom bounce, reset if off left/right
    # Move the ball
    if ball_pos.x < 5 or ball_pos.x > 1915:
        ball_speed_x = -ball_speed_x
    if ball_pos.y > 1075 or ball_pos.y < 5:
        ball_speed_y = -ball_speed_y
    ball_pos.x += ball_speed_x * dt
    ball_pos.y += ball_speed_y * dt
    # Ball hitbox
    ball_hitbox = pygame.Rect(ball_pos.x - 10, ball_pos.y - 10, 20, 20)  # 20x20 bounding box
    if ball_hitbox.colliderect(player1) or ball_hitbox.colliderect(player2):
        ball_speed_x = -ball_speed_x
    
    # Render
    pygame.draw.circle(screen, "black", ball_pos, 10)
    pygame.draw.rect(screen, "black", player1)
    pygame.draw.rect(screen, "black", player2)

    pygame.display.flip()
    dt = clock.tick(60) / 1000

pygame.quit()