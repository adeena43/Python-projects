import pygame

pygame.init()

XO = 'X'
winner = None
draw = None
board = [[None]*3, [None]*3, [None]*3]

clock = pygame.time.Clock()
screen = pygame.display.set_mode((400, 400))

ximg = pygame.image.load("X.png")
oimg = pygame.image.load("O-removebg-preview.png")
ximg = pygame.transform.scale(ximg, (80, 80))
oimg = pygame.transform.scale(oimg, (80, 80))

def drawgrid():
    screen.fill((241, 192, 185))
    
    # Vertical lines
    pygame.draw.line(screen, (236, 248, 127), (400//3, 0), (400//3, 400), 6)
    pygame.draw.line(screen, (236, 248, 127), (2 * 400//3, 0), (2 * 400//3, 400), 6)
    
    # Horizontal lines
    pygame.draw.line(screen, (236, 248, 127), (0, 400//3), (400, 400//3), 6)
    pygame.draw.line(screen, (236, 248, 127), (0, 2 * 400//3), (400, 2 * 400//3), 6)

def result():
    global draw, winner
    if winner:
        message = winner + " won!"
    else:
        message = "Game drawn!"
    
    font = pygame.font.SysFont('Georgia', 70)
    text = font.render(message, 1, (24, 154, 180))
    screen.fill((0, 0, 0), (0, 400, 500, 100))
    text_rect = text.get_rect(center=(400//2, 400//2))
    screen.blit(text, text_rect)
    
    pygame.display.update()

def wincases():
    global board, winner, draw
    # Check rows
    for row in range(3):
        if board[row][0] == board[row][1] == board[row][2] and board[row][0] is not None:
            winner = board[row][0]
            result()
            return
    
    # Check columns
    for col in range(3):
        if board[0][col] == board[1][col] == board[2][col] and board[0][col] is not None:
            winner = board[0][col]
            result()
            return
    
    # Check diagonals
    if board[0][0] == board[1][1] == board[2][2] and board[0][0] is not None:
        winner = board[0][0]
        pygame.draw.line(screen, (250, 70, 70), (50, 50), (350, 350), 4)
        result()
        return
    
    if board[0][2] == board[1][1] == board[2][0] and board[0][2] is not None:
        winner = board[0][2]
        pygame.draw.line(screen, (250, 70, 70), (350, 50), (50, 350), 4)
        result()
        return
    
    # Check for draw
    if all(all(row) for row in board) and winner is None:
        draw = True
        result()

def getimg(row, col):
    global board, XO

    posx = col * (400 // 3) + 30
    posy = row * (400 // 3) + 30

    board[row][col] = XO
    if XO == 'X':
        screen.blit(ximg, (posx, posy))
        XO = 'O'
    else:
        screen.blit(oimg, (posx, posy))
        XO = 'X'

    pygame.display.update()

def input_to_block():
    x, y = pygame.mouse.get_pos()
    row = y // (400 // 3)
    col = x // (400 // 3)

    if board[row][col] is None:
        getimg(row, col)
        wincases()

drawgrid()

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            quit()
        elif event.type == pygame.MOUSEBUTTONDOWN:
            input_to_block()

    pygame.display.update()
    clock.tick(30)
