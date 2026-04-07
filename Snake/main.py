import pygame
import time
import random

pygame.init()

# Texte principale loose
fontLoose = pygame.font.SysFont(None, 100)
# Texte secondaire (plus petit)
smallFontLoose = pygame.font.SysFont(None, 40)
#Font du score
scoreFont = pygame.font.SysFont(None, 40)


#Flags
game_over = False
running = True

#Constantes
gridWidth = 15
gridHeight = 15
paddingGrid = 21
screenSizeWidth = 750
screenSizeHeight = 750
direction = {
    "RIGHT": (0,1),
    "LEFT": (0,-1),
    "DOWN": (1,0),
    "UP": (-1,0)
}
snakeSpeed = 200     # millisecondes entre chaque déplacement
snakeDirection = ["RIGHT"] #Direction de départ
snakeSizeStart = 4

#Buffer
lastMoveTime = 0
scoreValue = 0
countSuperGoal = 0
progressBar = 0
snakePosition = []
coordonneesGoal = None
coordonneesSuperGoal = None
snakeSize = snakeSizeStart
grid = [[0 for x in range(gridHeight)] for y in range(gridWidth)] #[Y, X]
progress = 0


screen = pygame.display.set_mode((screenSizeWidth, screenSizeHeight))
clock = pygame.time.Clock()

#SKIN
#head_img = pygame.image.load("head.png").convert_alpha()

def updateMap():
    for line in range(gridWidth):
        for column in range(gridHeight):
            if grid[line][column] == 0:
                #pygame.draw.circle(screen,(255,255,255),((screenSizeWidth/2)-(gridWidth*20)/2+(20*column),(screenSizeHeight/2)-(gridHeight*20)/2+(20*line)),10)
                printCircle((200,150,65), column , line)   #Normaux
            elif grid[line][column] == 2: 
                printCircle((245, 41, 0),  column , line)   #Objectifs
            elif grid[line][column] == 3: 
                printCircle((255, 244, 0),  column , line)   #SuperObjectifs
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
    global coordonneesGoal, grid ,snakeSize, game_over, scoreValue, coordonneesSuperGoal, progress
    #grid = [[0 for x in range(gridWidth)] for y in range(gridHeight)]

    if len(snakeDirection) > 1:
        snakeDirection.pop(0)

    moveDirection = direction[snakeDirection[0]] #Retourne le Tuple souhaité en selectionnant dans la lookup le nom de la direction
    print(snakeDirection)

    nextLine = snakePosition[-1][0] + moveDirection[0]      #Y
    nextColumn = snakePosition[-1][1] + moveDirection[1]    #X
    previousLine = snakePosition[0][0]                      #Y
    previousColumn = snakePosition[0][1]                    #X

    if(nextLine >= 0 and nextLine < gridHeight and nextColumn >= 0 and nextColumn < gridWidth): #On check la collision avec les murs
        snakePosition.pop(0)
        if (nextLine, nextColumn) in snakePosition: #On check la collision avec lui même
            game_over = True
            
        snakePosition.append((nextLine, nextColumn)) #Y, X
        if grid[nextLine][nextColumn] == 2: #On check si on a mangé un fruit
            coordonneesGoal = None
            snakeSize += 1
            snakePosition.insert(0, (previousLine, previousColumn)) #on ajoute la dernière position à la liste
            scoreValue +=10
            #print(snakeSize)
        if grid[nextLine][nextColumn] == 3: #On check si on a mangé un Super fruit
            coordonneesSuperGoal = None
            snakeSize += 1
            snakePosition.insert(0, (previousLine, previousColumn)) #on ajoute la dernière position à la liste
            scoreValue += round(10*(progress/10))
            #print(snakeSize)
    else: #Si collision
        game_over = True
        

    if(grid[previousLine][previousColumn] == 1): 
        grid[previousLine][previousColumn] = 0 #Y, X

    for x in range(snakeSize):
        grid[snakePosition[x][0]][snakePosition[x][1]] = 1

#def checkCollid():


def spawnGoal(): #Fait apparaitre l'objectif sur le terrain 
    global grid, countSuperGoal
    randomY = 0
    randomX = 0
    #print(snakePosition)
    #print(snakePosition[0][1])
    countSuperGoal += 1
    while True:
        randomY = random.randint(0,gridHeight - 1)
        randomX = random.randint(0,gridWidth - 1)
        if(randomY, randomX) not in snakePosition:
            grid[randomY][randomX] = 2
            return(randomY, randomX)

def spawnSuperGoal(): #Fait apparaitre l'objectif sur le terrain 
    global grid, progress
    randomY = 0
    randomX = 0
    #print(snakePosition)
    #print(snakePosition[0][1])
    progress = 0
    while True:
        randomY = random.randint(0,gridHeight - 1)
        randomX = random.randint(0,gridWidth - 1)
        if(randomY, randomX) not in snakePosition and grid[randomY][randomX] != 2:
            grid[randomY][randomX] = 3
            return(randomY, randomX)

def printLoose():
    # Texte principal
    text = fontLoose.render("PERDU", True, (255, 0, 0))
    rect = text.get_rect(center=(screenSizeWidth/2, screenSizeHeight/2))
    screen.blit(text, rect)


    text2 = smallFontLoose.render("Appuie sur SPACE pour recommencer", True, (255, 255, 255))

    # Positionné EN DESSOUS du premier
    rect2 = text2.get_rect(center=(screenSizeWidth/2, rect.bottom + 30))

    screen.blit(text2, rect2)

def restartGame():
    global grid, coordonneesGoal, snakeSize, snakeDirection, scoreValue
    snakePosition.clear()
    snakeSize = snakeSizeStart
    coordonneesGoal = None
    snakeDirection = ["RIGHT"]
    grid = [[0 for x in range(gridWidth)] for y in range(gridHeight)]
    scoreValue = 0
    spawnSnake()

def loadBarre(coordonneesSuperGoal, width, left, top, height, thickness):
    global progress
    if coordonneesSuperGoal != None:
        progressCalc = (((width-(thickness+1)*2))*progress)/100
        print("progressCalc:",progressCalc)

        pygame.draw.rect(screen, (200,0,0), (left, top, width, height), thickness)
        pygame.draw.rect(screen, (255,0,0), (left+thickness+1, top+thickness+1, progressCalc, height-(thickness+1)*2), 0)

        if progress < 100:
            progress += 0.4
     

spawnSnake()

while running:
    screen.fill((0,0,0))
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RIGHT and snakeDirection[-1] !="LEFT":
                snakeDirection.append("RIGHT")
                #print(snakeDirection)
            elif event.key == pygame.K_LEFT and snakeDirection[-1] !="RIGHT":
                snakeDirection.append("LEFT")
                #print(snakeDirection)
            elif event.key == pygame.K_UP and snakeDirection[-1] !="DOWN":
                snakeDirection.append("UP")
                #print(snakeDirection)
            elif event.key == pygame.K_DOWN and snakeDirection[-1] !="UP":
                snakeDirection.append("DOWN")
                #print(snakeDirection)
            elif event.key == pygame.K_SPACE and game_over == True:
                restartGame()
                game_over = False


    if coordonneesGoal == None:
        coordonneesGoal = spawnGoal()
    
    if countSuperGoal == 5 and coordonneesSuperGoal == None:
        countSuperGoal = 0 
        coordonneesSuperGoal = spawnSuperGoal()

    loadBarre(coordonneesSuperGoal ,221, 5, 5, 45, 2)


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

    # Texte principal
    score = scoreFont.render(f"Score: {scoreValue:05} ", True, (255, 255, 255))

    rect = score.get_rect(center=(screenSizeWidth/1.4, screenSizeHeight/16))
    screen.blit(score, rect)




    pygame.display.flip()
    clock.tick(60)

pygame.quit()
