import pygame
import random
import sys
from pygame.locals import *

# Initialize Pygame
pygame.init()

# Game Variables
FPS = 32
SCREENWIDTH = 289
SCREENHEIGHT = 511
GROUNDY = SCREENHEIGHT * 0.8
GAME_SPRITES = {}
GAME_SOUNDS = {}
PLAYER = 'gallery/sprites/bird02.png'
BACKGROUND = 'gallery/sprites/background.png'
PIPE = 'gallery/sprites/pipe.png'
MESSAGE = 'gallery/sprites/message.png'

# Create the screen
SCREEN = pygame.display.set_mode((SCREENWIDTH, SCREENHEIGHT))
FPSCLOCK = pygame.time.Clock()

def welcomeScreen():
    playerx = int(SCREENWIDTH / 5)
    playery = int((SCREENHEIGHT - GAME_SPRITES['player'].get_height()) / 2.25)
    messagex = int((SCREENWIDTH - GAME_SPRITES['message'].get_width()) / 2)
    messagey = int(SCREENHEIGHT * 0.13)
    basex = 0

    while True:
        for event in pygame.event.get():
            if event.type == QUIT or (event.type == KEYDOWN and event.key == K_ESCAPE):
                pygame.quit()
                sys.exit()

            elif event.type == KEYDOWN and (event.key == K_SPACE or event.key == K_RETURN):
                return

        SCREEN.blit(GAME_SPRITES['background'], (0, 0))
        SCREEN.blit(GAME_SPRITES['player'], (playerx, playery))
        SCREEN.blit(GAME_SPRITES['message'], (messagex, messagey))
        SCREEN.blit(GAME_SPRITES['base'], (basex, GROUNDY))
        
        pygame.display.update()
        FPSCLOCK.tick(FPS)

def getRandomPipe():
    pipeHeight = GAME_SPRITES['pipe'][0].get_height()
    offset = SCREENHEIGHT / 3
    min_pipe_y = 50
    max_pipe_y = SCREENHEIGHT - GROUNDY - 1.2 * offset - min_pipe_y

    if max_pipe_y <= 0:
        max_pipe_y = 100

    y2 = offset + random.randrange(0, int(max_pipe_y)) 
    pipeX = SCREENWIDTH + 10
    y1 = pipeHeight - y2 + offset

    pipe = [
        {'x': pipeX, 'y': -y1},
        {'x': pipeX, 'y': y2}
    ]

    return pipe

def isCollide(playerx, playery, upperPipes, lowerPipes):
    # Check if the player has hit the ground or top of the screen
    if playery >= GROUNDY - GAME_SPRITES['player'].get_height() or playery <= 0:
        GAME_SOUNDS['hit'].play()
        return True
    
    player_rect = pygame.Rect(playerx, playery, GAME_SPRITES['player'].get_width()-175, GAME_SPRITES['player'].get_height())

    # Check for collision with upper pipes
    if(len(upperPipes) and len(lowerPipes)):
        for pipe in upperPipes:
            pipe_rect = pygame.Rect(pipe['x'], pipe['y'], GAME_SPRITES['pipe'][0].get_width(), GAME_SPRITES['pipe'][0].get_height())
            if player_rect.colliderect(pipe_rect):
                GAME_SOUNDS['hit'].play()
                return True
        
        # Check for collision with lower pipes
        for pipe in lowerPipes:
            pipe_rect = pygame.Rect(pipe['x'], pipe['y'], GAME_SPRITES['pipe'][1].get_width(), GAME_SPRITES['pipe'][1].get_height())
            if player_rect.colliderect(pipe_rect):
                GAME_SOUNDS['hit'].play()
                return True
    
    return False

def mainGame():
    score = 0
    playerx = int(SCREENWIDTH / 5)
    playery = int(SCREENWIDTH / 2)
    basex = 0
    newPipe1 = getRandomPipe()
    newPipe2 = getRandomPipe()

    upperPipes = [
        {'x': SCREENWIDTH + 200, 'y': newPipe1[0]['y']},
        {'x': SCREENWIDTH + 200 + (SCREENWIDTH / 2), 'y': newPipe2[0]['y']}
    ]

    lowerPipes = [
        {'x': SCREENWIDTH + 200, 'y': newPipe1[1]['y']},
        {'x': SCREENWIDTH + 200 + (SCREENWIDTH / 2), 'y': newPipe2[1]['y']}
    ]
    
    pipeVelx = -4
    playerVelY = -9
    playerMaxVelY = 10
    playerMinVelY = -8
    playerAccY = 1
    playerFlapAccv = -8
    playerFlapped = False

    while True:
        for event in pygame.event.get():
            if event.type == QUIT or (event.type == KEYDOWN and event.key == K_ESCAPE):
                pygame.quit()
                sys.exit()

            if event.type == KEYDOWN and (event.key == K_SPACE or event.key == K_UP):
                if playery > 0:
                    playerVelY = playerFlapAccv
                    playerFlapped = True
                    GAME_SOUNDS['wing'].play()

        crashTest = isCollide(playerx, playery, upperPipes, lowerPipes)
        if crashTest:
            return
        
        playerMidPos = playerx + GAME_SPRITES['player'].get_width() / 2
        for pipe in upperPipes:
            pipeMidPos = pipe['x'] + GAME_SPRITES['pipe'][0].get_width() / 2
            if pipeMidPos <= playerMidPos < pipeMidPos + 4:
                score += 1
                print(f"Your score is {score}")
                GAME_SOUNDS['point'].play()

        if playerVelY < playerMaxVelY and not playerFlapped:
            playerVelY += playerAccY
        if playerFlapped:
            playerFlapped = False
        playerHeight = GAME_SPRITES['player'].get_height()
        playery = playery + min(playerVelY, GROUNDY - playery - playerHeight)

        # Update pipe positions
        for upperPipe, lowerPipe in zip(upperPipes, lowerPipes):
            upperPipe['x'] += pipeVelx
            lowerPipe['x'] += pipeVelx

        # Generate new pipes when needed
        if upperPipes and 0 < upperPipes[0]['x'] < 5:
            newPipe = getRandomPipe()
            upperPipes.append(newPipe[0])
            lowerPipes.append(newPipe[1])

        # Remove old pipes that have gone off screen
        if upperPipes and upperPipes[0]['x'] < -GAME_SPRITES['pipe'][0].get_width():
            upperPipes.pop(0)
            lowerPipes.pop(0)

        # Ensure pipes are never empty
        if not upperPipes or not lowerPipes:
            newPipe = getRandomPipe()
            upperPipes.append(newPipe[0])
            lowerPipes.append(newPipe[1])

        SCREEN.blit(GAME_SPRITES['background'], (0, 0))
        for upperPipe, lowerPipe in zip(upperPipes, lowerPipes):
            SCREEN.blit(GAME_SPRITES['pipe'][0], (upperPipe['x'], upperPipe['y']))
            SCREEN.blit(GAME_SPRITES['pipe'][1], (lowerPipe['x'], lowerPipe['y']))

        SCREEN.blit(GAME_SPRITES['base'], (basex, GROUNDY))
        SCREEN.blit(GAME_SPRITES['player'], (playerx, playery))
        
        myDigits = [int(x) for x in str(score)]
        width = 0

        for digit in myDigits:
            width += GAME_SPRITES['numbers'][digit].get_width()
        Xoffset = (SCREENWIDTH - width) / 2

        for digit in myDigits:
            SCREEN.blit(GAME_SPRITES['numbers'][digit], (Xoffset, SCREENHEIGHT * 0.12))
            Xoffset += GAME_SPRITES['numbers'][digit].get_width()

        pygame.display.update()
        FPSCLOCK.tick(FPS)

if __name__ == "__main__":
    # Load images
    original_player_image = pygame.image.load(PLAYER).convert_alpha()
    original_width, original_height = original_player_image.get_size()
    new_width = original_width // 2
    new_height = original_height // 2
    resized_player_image = pygame.transform.scale(original_player_image, (new_width, new_height))

    GAME_SPRITES['numbers'] = (
        pygame.image.load('gallery/sprites/0.png').convert_alpha(),
        pygame.image.load('gallery/sprites/1.png').convert_alpha(),
        pygame.image.load('gallery/sprites/2.png').convert_alpha(),
        pygame.image.load('gallery/sprites/3.jfif').convert_alpha(),
        pygame.image.load('gallery/sprites/4.jfif').convert_alpha(),
        pygame.image.load('gallery/sprites/5.jfif').convert_alpha(),
        pygame.image.load('gallery/sprites/6.jfif').convert_alpha(),
        pygame.image.load('gallery/sprites/7.png').convert_alpha(),
        pygame.image.load('gallery/sprites/8.png').convert_alpha(),
        pygame.image.load('gallery/sprites/9.jfif').convert_alpha(),
    )

    GAME_SPRITES['base'] = pygame.image.load('gallery/sprites/base.png').convert_alpha()
    GAME_SPRITES['pipe'] = (
        pygame.transform.rotate(pygame.image.load(PIPE).convert_alpha(), 180),
        pygame.image.load(PIPE).convert_alpha()
    )
    GAME_SPRITES['background'] = pygame.image.load(BACKGROUND).convert_alpha()
    GAME_SPRITES['player'] = resized_player_image
    GAME_SPRITES['message'] = pygame.image.load(MESSAGE).convert_alpha()

    GAME_SOUNDS['die'] = pygame.mixer.Sound('gallery/audio/die.mp3')
    GAME_SOUNDS['hit'] = pygame.mixer.Sound('gallery/audio/hit.wav')
    GAME_SOUNDS['swoosh'] = pygame.mixer.Sound('gallery/audio/swoosh.mp3')
    GAME_SOUNDS['point'] = pygame.mixer.Sound('gallery/audio/point.mp3')
    GAME_SOUNDS['wing'] = pygame.mixer.Sound('gallery/audio/wing.mp3')

    while True:
        welcomeScreen()  # Shows welcome screen to the user until the user quits the game
        mainGame()
