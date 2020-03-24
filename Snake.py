import pygame
import random
import time

#Setting basic pygame vars
screenSize = 500
screen = pygame.display.set_mode((screenSize, screenSize))
End = False

#Setting Font vars
pygame.font.init()
gameFont = pygame.font.SysFont('Comic Sans MS', 30)
def updateScore():
    text = gameFont.render(str(len(snakeLocations)+1), False, SNAKE)
    screen.blit(text, (10,0))

#Setting game vars
blockNum = 25
blockSize = screenSize/blockNum
originalSize = 3
snakeSize = 3
snakeLocations = []
xspeed = 1
yspeed = 0
snakeLocation = [0,0]

#Makes the snake fade (And be cooler)
IS_FADE = True

#Defining colors
BACKGROUND = (0,0,0)
SNAKE = (50,255,50)
APPLE = (255,0,0)
SNAKEHEAD = (50,255,50)

#Returns a fading color based on the distance from the head
def getSnakeLoctionColor(length, location: int):
    loc = length - location + 1
    decamount = (245 // max(length, 10))
    dec = decamount * loc
    return tuple(map(lambda x : max(x-dec, 0),SNAKE))

def getNewAppleLocation(startPoint = 0):
    return [random.randint(startPoint,blockNum-1), random.randint(startPoint,blockNum-1)]

appleLocation = getNewAppleLocation(1)

#Sample rate vars, to control the speed of the game
tickNumber = 0
workPerTicks = 100

#Gets a key and returns the snake speed
def keyDown(key):
    x = 0
    y = 0
    if key == pygame.K_w or key == pygame.K_UP:
        x = 0
        y = -1
    if key == pygame.K_s or key == pygame.K_DOWN:
        x = 0
        y = 1
    if key == pygame.K_a or key == pygame.K_LEFT:
        x = -1
        y = 0
    if key == pygame.K_d or key == pygame.K_RIGHT:
        x = 1
        y = 0
    return [x,y]

lastSnakeLength = len(snakeLocation)
updateScore()

while not End:
    #Check events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            End = True
        if event.type == pygame.KEYDOWN:
            xspeed, yspeed = keyDown(event.key)
    
    if tickNumber % workPerTicks == 0:
        snakeLocations.append(list(snakeLocation))

        #Control the snakes length
        while len(snakeLocations) >= snakeSize:
            snakeLocations.pop(0)

        snakeLocation[0] += xspeed
        snakeLocation[1] += yspeed

        #Wrap-Around
        for i in range(len(snakeLocation)):
            if snakeLocation[i] >= blockNum:
                snakeLocation[i] = 0
            elif snakeLocation[i] < 0:
                snakeLocation[i] = blockNum

        #Check for apple
        if snakeLocation[0] == appleLocation[0] and snakeLocation[1] == appleLocation[1]:
            snakeSize += 1
            appleLocation = getNewAppleLocation()

        #Increase speed (Higher smaple rate) the longer the snake is 
        workPerTicks = max([100 - (snakeSize-originalSize)*3, 35])

    screen.fill(BACKGROUND)
    
    #Render apple
    pygame.draw.rect(screen, APPLE, (appleLocation[0] * blockSize, appleLocation[1] * blockSize, blockSize, blockSize))

    #Render snake head
    pygame.draw.rect(screen, SNAKEHEAD, (snakeLocation[0] * blockSize, snakeLocation[1] * blockSize, blockSize, blockSize))

    #Render snake body
    for index, i in enumerate(snakeLocations):
        #Check if snake is touching itself
        if i[0] == snakeLocation[0] and i[1] == snakeLocation[1]:
            snakeSize = originalSize
        
        if IS_FADE:
            pygame.draw.rect(screen, getSnakeLoctionColor(len(snakeLocations),index), (i[0] * blockSize, i[1] * blockSize, blockSize, blockSize))
        else:
            pygame.draw.rect(screen, SNAKE, (i[0] * blockSize, i[1] * blockSize, blockSize, blockSize))

    updateScore()

    pygame.display.update()
    
    tickNumber = (tickNumber+1) % workPerTicks

