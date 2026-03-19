import pygame
import time
import random

pygame.init()
font = pygame.font.SysFont(None, 100)

#Flags
game_over = False
running = True
flagMoveAck = 0

#Constantes
gridWidth = 10
gridHeight = 10
paddingGrid = 21
screenSizeWidth = 750
screenSizeHeight = 750
direction = {
    "RIGHT": (0,1),
    "LEFT": (0,-1),
    "DOWN": (1,0),
    "UP": (-1,0)
}
snakeDirection = "RIGHT" #Direction de départ
snakeSizeStart = 4

snakePosition = []
coordonneesGoal = None
snakeSize = snakeSizeStart
grid = [[0 for x in range(gridHeight)] for y in range(gridWidth)] #[Y, X]


snakeSpeed = 200      # millisecondes entre chaque déplacement
lastMoveTime = 0



screen = pygame.display.set_mode((screenSizeWidth, screenSizeHeight))
clock = pygame.time.Clock()





def updateMap():
    for line in range(gridWidth):
        for column in range(gridHeight):
            if grid[line][column] == 0:
                #pygame.draw.circle(screen,(255,255,255),((screenSizeWidth/2)-(gridWidth*20)/2+(20*column),(screenSizeHeight/2)-(gridHeight*20)/2+(20*line)),10)
                printCircle((200,150,65), column , line)   #Normaux
            elif grid[line][column] == 2: 
                printCircle((245, 41, 0),  column , line)   #Objectifs
            else: 
                printCircle((20,150,65),  column , line)    #Snake

def printCircle(couleur, column, line):
    pygame.draw.circle(
        screen,
        couleur,
        (
        (screenSizeWidth/2)-(gridWidth*20)/2+(paddingGrid*column),
        (screenSizeHeight/2)-(gridHeight*20)/2+(paddingGrid*line)
        ),
         10)

def spawnSnake():
    for x in range(snakeSize):
        grid[gridHeight//2][x] = 1
        snakePosition.append((gridHeight//2, x))  #Y, X

def moveSnake():
    global coordonneesGoal, grid ,snakeSize, game_over, flagMoveAck
    #grid = [[0 for x in range(gridWidth)] for y in range(gridHeight)]

    moveDirection = direction[snakeDirection] #Retourne le Tuple souhaité en selectionnant dans la lookup le nom de la direction
    
    nextLine = snakePosition[-1][0] + moveDirection[0]      #Y
    nextColumn = snakePosition[-1][1] + moveDirection[1]    #X
    previousLine = snakePosition[0][0]                      #Y
    previousColumn = snakePosition[0][1]                    #X

    if(nextLine >= 0 and nextLine < gridHeight and nextColumn >= 0 and nextColumn < gridWidth): #On check la collision avec les murs
        print(snakeDirection)
        snakePosition.pop(0)
        if (nextLine, nextColumn) in snakePosition: #On check la collision avec lui même
            game_over = True
            
        snakePosition.append((nextLine, nextColumn)) #Y, X
        flagMoveAck = 1 

        if grid[nextLine][nextColumn] == 2:
            coordonneesGoal = None
            snakeSize += 1
            snakePosition.insert(0, (previousLine, previousColumn))
            #print(snakeSize)
    else: #Si collision
        game_over = True
        

    if(grid[previousLine][previousColumn] == 1): 
        grid[previousLine][previousColumn] = 0 #Y, X

    for x in range(snakeSize):
        grid[snakePosition[x][0]][snakePosition[x][1]] = 1

#def checkCollid():


def spawnGoal(): #Fait apparaitre l'objectif sur le terrain 
    global grid
    randomY = 0
    randomX = 0
    #print(snakePosition)
    #print(snakePosition[0][1])

    while True:
        randomY = random.randint(0,gridHeight - 1)
        randomX = random.randint(0,gridWidth - 1)
        if(randomY, randomX) not in snakePosition:
            grid[randomY][randomX] = 2
            return(randomY, randomX)          

def printLoose():
    # Texte principal
    text = font.render("PERDU", True, (255, 0, 0))
    rect = text.get_rect(center=(screenSizeWidth/2, screenSizeHeight/2))
    screen.blit(text, rect)

    # Texte secondaire (plus petit)
    smallFont = pygame.font.SysFont(None, 40)
    text2 = smallFont.render("Appuie sur SPACE pour recommencer", True, (255, 255, 255))

    # Positionné EN DESSOUS du premier
    rect2 = text2.get_rect(center=(screenSizeWidth/2, rect.bottom + 30))

    screen.blit(text2, rect2)

def restartGame():
    global grid, coordonneesGoal, snakeSize, snakeDirection
    snakePosition.clear()
    snakeSize = snakeSizeStart
    coordonneesGoal = None
    snakeDirection = "RIGHT"
    grid = [[0 for x in range(gridWidth)] for y in range(gridHeight)]
    spawnSnake()



spawnSnake()

while running:
    screen.fill((0,0,0))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RIGHT and snakeDirection !="LEFT":
                if flagMoveAck == 1:
                    snakeDirection="RIGHT"
                    flagMoveAck=0
                #print(snakeDirection)
            elif event.key == pygame.K_LEFT and snakeDirection !="RIGHT":
                if flagMoveAck == 1:
                    snakeDirection="LEFT"
                    flagMoveAck=0
                    #print(snakeDirection)
            elif event.key == pygame.K_UP and snakeDirection !="DOWN":
                if flagMoveAck == 1:
                    snakeDirection="UP"
                    flagMoveAck=0
                    #print(snakeDirection)
            elif event.key == pygame.K_DOWN and snakeDirection !="UP":
                if flagMoveAck == 1:
                    snakeDirection="DOWN"
                    flagMoveAck=0
                #print(snakeDirection)
            elif event.key == pygame.K_SPACE and game_over == True:
                restartGame()
                game_over = False


    if coordonneesGoal == None:
        coordonneesGoal = spawnGoal()

    updateMap()

    currentTime = pygame.time.get_ticks()
    if game_over == False:
        if currentTime - lastMoveTime > snakeSpeed:
            moveSnake()
            lastMoveTime = currentTime
    else:
        printLoose()

    """"
    for x in range(gridWidth):
        print(grid[x])
    """
    pygame.display.flip()
    clock.tick(60)

pygame.quit()