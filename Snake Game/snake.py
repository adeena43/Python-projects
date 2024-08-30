import pygame
import random

pygame.init()
pygame.mixer.init()  # Initialize the mixer

# Screen dimensions
screen_width = 1200
screen_height = 600
gameWindow = pygame.display.set_mode((screen_width, screen_height))

# Colors
white = (255, 255, 255)
red = (255, 0, 0)
black = (0, 0, 0)

pygame.display.set_caption("Snake!!")
clock = pygame.time.Clock()

# Initial snake properties
font = pygame.font.SysFont(None, 55)

def text_screen(text, color, x, y):
    screen_text = font.render(text, True, color)
    gameWindow.blit(screen_text, (x, y))

def plot_snake(gameWindow, color, snk_list, snake_size):
    for segment in snk_list:
        pygame.draw.rect(gameWindow, color, [segment[0], segment[1], snake_size, snake_size])

def load_high_score():
    try:
        with open("hiscore.txt", "r") as f:
            return int(f.read())
    except (FileNotFoundError, ValueError):
        return 0

def save_high_score(high_score):
    with open("hiscore.txt", "w") as f:
        f.write(str(high_score))

def play_background_music():
    try:
        pygame.mixer.music.load("snake_music.mp3")  # Load the background music file
        pygame.mixer.music.play(-1)  # Play the music indefinitely
        print("Background music started.")
    except pygame.error as e:
        print(f"Error loading background music: {e}")

def play_game_over_music():
    try:
        pygame.mixer.music.stop()  # Stop background music
        pygame.mixer.music.load("gameOver.mp3")  # Load the game over music file
        pygame.mixer.music.play()  # Play the music once
        print("Game over music started.")
    except pygame.error as e:
        print(f"Error loading game over music: {e}")

def game_loop():
    global exit_game, game_over
    snake_x = 100
    snake_y = 100
    velocity_x = 0
    velocity_y = 0
    snake_size = 15
    snake_speed = 10
    food_x = random.randint(20, screen_width - 20)
    food_y = random.randint(20, screen_height - 20)
    score = 0
    hiscore = load_high_score()
    
    snk_list = []
    snk_length = 1

    exit_game = False
    game_over = False

    play_background_music()  # Start playing background music when the game starts

    while not exit_game:
        if game_over:
            save_high_score(hiscore)
            gameWindow.fill(white)
            text_screen('Game Over!! Press Enter to play again', red, 250, screen_height // 2)
            #play_game_over_music()  # Play game over music

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    exit_game = True
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN:
                        pygame.mixer.music.stop()  # Stop the game over music
                        return  # Exit the game loop to go back to the welcome screen

        else:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    exit_game = True

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RIGHT and velocity_x == 0:
                        velocity_x = snake_speed
                        velocity_y = 0
                    elif event.key == pygame.K_LEFT and velocity_x == 0:
                        velocity_x = -snake_speed
                        velocity_y = 0
                    elif event.key == pygame.K_UP and velocity_y == 0:
                        velocity_y = -snake_speed
                        velocity_x = 0
                    elif event.key == pygame.K_DOWN and velocity_y == 0:
                        velocity_y = snake_speed
                        velocity_x = 0

            snake_x += velocity_x
            snake_y += velocity_y

            # Check for collision with food
            if abs(snake_x - food_x) < snake_size and abs(snake_y - food_y) < snake_size:
                score += 10
                food_x = random.randint(20, screen_width - 20)
                food_y = random.randint(20, screen_height - 20)
                snk_length += 3  # Adjusted increment value
                if score > hiscore:
                    hiscore = score

            gameWindow.fill(white)
            text_screen(f"Score: {score} Hiscore: {hiscore}", red, 5, 5)

            # Update the snake's position
            head = [snake_x, snake_y]
            snk_list.append(head)
            
            if len(snk_list) > snk_length:
                del snk_list[0]

            if head in snk_list[:-1]:
                game_over = True
                pygame.mixer.music.load("gameOver.mp3")  # Load the game over music file
                pygame.mixer.music.play()

            if snake_x < 0 or snake_x > screen_width or snake_y < 0 or snake_y > screen_height:
                game_over = True
                pygame.mixer.music.load("gameOver.mp3")  # Load the game over music file
                pygame.mixer.music.play()
            
            pygame.draw.rect(gameWindow, red, [food_x, food_y, snake_size, snake_size])
            plot_snake(gameWindow, black, snk_list, snake_size)
        pygame.display.update()
        clock.tick(20)

    pygame.quit()

def welcome():
    global exit_game
    exit_game = False

    font = pygame.font.SysFont('Georgia', 40, bold=True)
    play_text = font.render('Play', True, 'red')
    
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
            pygame.draw.rect(gameWindow, 'light grey', playButton)
        else:
            pygame.draw.rect(gameWindow, 'dark grey', playButton)
        
        # Draw the play text
        text_rect = play_text.get_rect(center=playButton.center)
        gameWindow.fill((255, 223, 223))  # Background color
        text_screen("Welcome to Snakes!!", black, 400, 250)
        gameWindow.blit(play_text, text_rect)
        
        pygame.display.update()
        clock.tick(60)

welcome()
