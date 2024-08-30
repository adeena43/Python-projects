import pygame
from pygame.locals import *
import random

# Initialize Pygame
pygame.init()
pygame.mixer.init()

# Define colors
white = (255, 255, 255)
red = (255, 0, 0)
black = (0, 0, 0)

# Set up clock
clock = pygame.time.Clock()

# Set up screen dimensions
size = width, height = (800, 700)
gameWindow = pygame.display.set_mode(size)

# Calculate road and roadmark dimensions
road_w = int(width / 1.6)
roadmark_w = int(width / 80)
right_lane = width / 2 + road_w / 4
left_lane = width / 2 - road_w / 4

# Load car images
car = pygame.image.load("car.png")
car2 = pygame.image.load("otherCar.png")

# Set up font
font = pygame.font.SysFont(None, 55)

def text_screen(text, color, x, y):
    screen_text = font.render(text, True, color)
    gameWindow.blit(screen_text, (x, y))

def load_high_score():
    try:
        with open("score_hi.txt", "r") as f:
            return int(f.read())
    except (FileNotFoundError, ValueError):
        return 0

def save_high_score(high_score):
    with open("score_hi.txt", "w") as f:
        f.write(str(high_score))

def play_background_music():
    try:
        pygame.mixer.music.load("bgMusic.mp3")
        pygame.mixer.music.play(-1)
        print("Background music started.")
    except pygame.error as e:
        print(f"Error loading background music: {e}")

def play_game_over_music():
    try:
        pygame.mixer.music.stop()
        pygame.mixer.music.load("gameOver.mp3")
        pygame.mixer.music.play()
        print("Game over music started.")
    except pygame.error as e:
        print(f"Error loading game over music: {e}")

def initialize_game():
    """Initialize game variables and reset positions."""
    global car_loc, car2_loc, speed, counter
    car_loc = car.get_rect()
    car_loc.center = right_lane, height * 0.8

    car2_loc = car2.get_rect()
    car2_loc.center = left_lane, height * 0.2

    speed = 10
    counter = 0

def game_loop():
    global exit_game, game_over, counter, speed
    score = 0
    hiscore = load_high_score()
    exit_game = False
    game_over = False

    initialize_game()  # Initialize or reset game variables

    play_background_music()

    while not exit_game:
        counter += 1
        if counter == 5000:
            speed += 0.15
            counter = 0

        if game_over:
            if score > hiscore:
                save_high_score(score)
            gameWindow.fill(white)
            text_screen('Game Over!! Press Enter to play again', red, 50, height // 2 - 30)
            text_screen(f'Final Score: {score}', red, 50, height // 2 + 30)
            
            pygame.display.update()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN:
                        pygame.mixer.music.stop()
                        return  # Exit the game_loop to return to the welcome screen

        else:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()

                if event.type == pygame.KEYDOWN:
                    if event.key in [K_a, K_LEFT]:
                        car_loc.x -= int(road_w / 2)
                    if event.key in [K_d, K_RIGHT]:
                        car_loc.x += int(road_w / 2)

            # Restrict car movement within road bounds
            if car_loc.x < width / 2 - road_w / 2:
                car_loc.x = width / 2 - road_w / 2
            if car_loc.x > width / 2 + road_w / 2 - car.get_width():
                car_loc.x = width / 2 + road_w / 2 - car.get_width()

            # Move the other car downwards
            car2_loc.y += speed
            if car2_loc.y > height:
                car2_loc.center = (right_lane if random.randint(0, 100) >= 50 else left_lane, -200)
                score += 10  # Increase score by 10 for successfully avoiding the obstacle
            
            if car_loc.colliderect(car2_loc):
                game_over = True
                pygame.mixer.music.load("gameOver.mp3")
                pygame.mixer.music.play()

            # Clear the screen
            gameWindow.fill((60, 220, 0))

            # Draw the road
            pygame.draw.rect(gameWindow, (50, 50, 50), (width / 2 - road_w / 2, 0, road_w, height))
            pygame.draw.rect(gameWindow, (255, 240, 60), (width / 2 - roadmark_w / 2, 0, roadmark_w, height))
            pygame.draw.rect(gameWindow, (255, 255, 255), (width / 2 - road_w / 2 + roadmark_w * 2, 0, roadmark_w, height))
            pygame.draw.rect(gameWindow, (255, 255, 255), (width / 2 + road_w / 2 - roadmark_w * 3, 0, roadmark_w, height))

            # Draw the cars
            gameWindow.blit(car, car_loc)
            gameWindow.blit(car2, car2_loc)

            # Draw score and hiscore
            text_screen(f"Score: {score} Hiscore: {hiscore}", red, width / 2 - 100, 10)

            # Update the display
            pygame.display.update()

        clock.tick(20)

    pygame.quit()

def welcome():
    global exit_game
    exit_game = False

    font = pygame.font.SysFont('Georgia', 40, bold=True)
    play_text = font.render('Play', True, red)
    
    playButton = pygame.Rect(500, 300, 200, 80)
    
    while not exit_game:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                exit_game = True
            if event.type == pygame.MOUSEBUTTONDOWN:
                if playButton.collidepoint(event.pos):
                    game_loop()

        # Button appearance based on mouse position
        mouse_x, mouse_y = pygame.mouse.get_pos()
        if playButton.collidepoint((mouse_x, mouse_y)):
            pygame.draw.rect(gameWindow, (200, 200, 200), playButton)
        else:
            pygame.draw.rect(gameWindow, (100, 100, 100), playButton)
        
        # Draw the play text
        text_rect = play_text.get_rect(center=playButton.center)
        gameWindow.fill((255, 223, 223))  # Background color
        text_screen("Welcome to Speedy Car!!", black, 200, 250)
        gameWindow.blit(play_text, text_rect)
        
        pygame.display.update()
        clock.tick(60)

if __name__ == "__main__":
    try:
        welcome()
    except pygame.error as e:
        print(f"Pygame error: {e}")
    finally:
        pygame.quit()
