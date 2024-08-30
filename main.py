import pygame
import sys
import random

# Initialize Pygame
pygame.init()

# Screen dimensions
screen_width = 1280
screen_height = 750

# Create the screen
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("PONG")

# Set up the clock
clock = pygame.time.Clock()

# Define the ball
ball = pygame.Rect(0, 0, 30, 30)
ball.center = (screen_width / 2, screen_height / 2)

# Define the paddles
cpu = pygame.Rect(0, 0, 20, 100)
cpu.centery = screen_height / 2

player = pygame.Rect(0, 0, 20, 100)
player.midright = (screen_width, screen_height / 2)

# Ball speed
ball_speed_x = 6
ball_speed_y = 6

# Paddle speeds
player_speed = 0
cpu_speed = 6

# Score
cpu_points = 0
player_points = 0

# Font for displaying the score
score_font = pygame.font.Font(None, 100)

def reset_ball():
    global ball_speed_x, ball_speed_y
    ball.x = screen_width / 2 - ball.width / 2
    ball.y = screen_height / 2 - ball.height / 2
    ball_speed_x = random.choice([-6, 6])
    ball_speed_y = random.choice([-6, 6])

def point_won(winner):
    global cpu_points, player_points
    if winner == 'cpu':
        cpu_points += 1
    elif winner == 'player':
        player_points += 1
    

def animate_ball():
    global ball_speed_x, ball_speed_y
    ball.x += ball_speed_x
    ball.y += ball_speed_y

    if ball.bottom >= screen_height or ball.top <= 0:
        ball_speed_y *= -1
    if ball.right >= screen_width:
        reset_ball()
    if ball.left <= 0:
        reset_ball()

    if ball.colliderect(player) :
        ball_speed_x *= -1
        ball_speed_x *= 1.1
        point_won('player')
    if ball.colliderect(cpu):
        ball_speed_x *= -1
        ball_speed_x *= 1.1
        point_won('cpu')
          # Increase ball speed on collision

def animate_player_paddle():
    player.y += player_speed
    if player.top < 0:
        player.top = 0
    if player.bottom > screen_height:
        player.bottom = screen_height

def animate_cpu_paddle():
    if ball.centery < cpu.centery:
        cpu.y -= cpu_speed
    if ball.centery > cpu.centery:
        cpu.y += cpu_speed

    if cpu.top < 0:
        cpu.top = 0
    if cpu.bottom > screen_height:
        cpu.bottom = screen_height

# Main game loop
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                player_speed = -6
            if event.key == pygame.K_DOWN:
                player_speed = 6

        if event.type == pygame.KEYUP:
            if event.key == pygame.K_UP or event.key == pygame.K_DOWN:
                player_speed = 0

    # Update game state
    animate_ball()
    animate_player_paddle()
    animate_cpu_paddle()

    # Draw everything
    screen.fill('black')
    pygame.draw.ellipse(screen, 'white', ball)
    pygame.draw.aaline(screen, 'white', (screen_width / 2, 0), (screen_width / 2, screen_height))
    pygame.draw.rect(screen, 'white', cpu)
    pygame.draw.rect(screen, 'white', player)

    cpu_score_surface = score_font.render(str(cpu_points), True, 'white')
    player_score_surface = score_font.render(str(player_points), True, 'white')
    screen.blit(cpu_score_surface, (screen_width / 4, 20))
    screen.blit(player_score_surface, (3 * screen_width / 4, 20))

    pygame.display.update()
    clock.tick(60)
