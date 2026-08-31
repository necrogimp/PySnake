import pygame
import time
import random
import mariadb

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
directionTable = {
    "RIGHT": (0, 1, 0),
    "DOWN": (1,0, 1),
    "LEFT": (0,-1, 2),
    "UP": (-1,0, 3)
}

cellTypes = {
    "VIDE": 0,
    "TETE": 1,
    "CORPS_PAIR": 2,
    "CORPS_IMPAIR": 3,
    "QUEUE": 4,
    "SUPERGOAL": 5,
    "GOAL": 6
}

snakeSpeed = 300    # millisecondes entre chaque déplacement
snakeDirection = ["RIGHT"] #Direction de départ
snakeSizeStart = 4

#Buffer
lastMoveTime = 0
scoreValue = 0
countSuperGoal = 0
progressBar = 0

coordonneesGoal = None
coordonneesSuperGoal = None
snakePosition = [] #Liste des points de coordonnées dans la grid | [Ligne], [Colonne], [Direction]
snakeSize = snakeSizeStart
snakeParity = True;
grid = [[[0, 0] for x in range(gridWidth)] for y in range(gridHeight)] #[Y, X] // [y][x][0] = Type de case => [1] = Orientation de la case
progress = 0


screen = pygame.display.set_mode((screenSizeWidth, screenSizeHeight))
clock = pygame.time.Clock()

#SKIN
head_img = pygame.image.load("./Snake/assets/tete_serpent.png").convert_alpha()
body_odd = pygame.image.load("./Snake/assets/corp_impair.png").convert_alpha()
body_even = pygame.image.load("./Snake/assets/corp_pair.png").convert_alpha()
tail = pygame.image.load("./Snake/assets/queue_serpent.png").convert_alpha()

def updateMap(): #Execute les commandes de mise en page de l'écran
    
    for line in range(gridWidth):
        for column in range(gridHeight):
            if grid[column][line][0] == cellTypes["VIDE"]: #Y, X
                #pygame.draw.circle(screen,(255,255,255),((screenSizeWidth/2)-(gridWidth*20)/2+(20*column),(screenSizeHeight/2)-(gridHeight*20)/2+(20*line)),10)
                printCircle((200,150,65), column , line, 10)   #Vide

            elif grid[column][line][0] == cellTypes["GOAL"]: 
                printCircle((245, 41, 0),  column , line, 10)   #Objectifs

            elif grid[column][line][0] == cellTypes["SUPERGOAL"]: 
                printCircle((120, 120, 0),  column , line, 10)   #SuperObjectifs

            elif grid[column][line][0] == cellTypes["CORPS_PAIR"]: 
                printBodyParts(body_even, grid[column][line][1], line, column)

            elif grid[column][line][0] == cellTypes["CORPS_IMPAIR"]: 
                printBodyParts(body_odd, grid[column][line][1], line, column)

            elif grid[column][line][0] == cellTypes["QUEUE"]: 
                printBodyParts(tail, grid[column][line][1], line, column)

            elif grid[column][line][0] == cellTypes["TETE"]: 
                printBodyParts(head_img, grid[column][line][1], line, column)


def printBodyParts(bodyPart, orientation, line, column):
            #if grid[column][line][0] == cellTypes["CORPS_PAIR"]: 
                if orientation == 0: #Droite
                    screen.blit(bodyPart, (
                    (screenSizeWidth/2)-(gridWidth*20)/2+(paddingGrid*line)-10, 
                    (screenSizeHeight/2)-(gridHeight*20)/2+(paddingGrid*column)-10
                    )
                    )
                elif orientation == 1: #bas
                    rotated_part = pygame.transform.rotate(bodyPart, 270)
                    screen.blit(rotated_part, (
                    (screenSizeWidth/2)-(gridWidth*20)/2+(paddingGrid*line)-10, 
                    (screenSizeHeight/2)-(gridHeight*20)/2+(paddingGrid*column)-10
                    )
                    )
                elif orientation == 2: #gauche
                    rotated_part = pygame.transform.rotate(bodyPart, 180)
                    screen.blit(rotated_part, (
                    (screenSizeWidth/2)-(gridWidth*20)/2+(paddingGrid*line)-10, 
                    (screenSizeHeight/2)-(gridHeight*20)/2+(paddingGrid*column)-10
                    )
                    )
                elif orientation == 3: #haut
                    rotated_part = pygame.transform.rotate(bodyPart, 90)
                    screen.blit(rotated_part, (
                    (screenSizeWidth/2)-(gridWidth*20)/2+(paddingGrid*line)-10, 
                    (screenSizeHeight/2)-(gridHeight*20)/2+(paddingGrid*column)-10
                    )
                    )

def printCircle(couleur, column, line, radius):
    pygame.draw.circle(
        screen,
        couleur,
        (
        (screenSizeWidth/2)-(gridWidth*20)/2+(paddingGrid*line),
        (screenSizeHeight/2)-(gridHeight*20)/2+(paddingGrid*column)
        ),
         radius)
    


def spawnSnake():
    for i in range(snakeSize):
        if(i == 0):
            grid[gridHeight//2][i] = [cellTypes["QUEUE"], 0]   #On init la grille
        elif(i == snakeSize-1):
            grid[gridHeight//2][i] = [cellTypes["TETE"], 0]   #On init la grille
        else:
            grid[gridHeight//2][i] = [cellTypes["CORPS_PAIR"], 0]   #On init la grille

        snakePosition.append([gridHeight//2, i, 0])             #On init la liste de position du serpent.
        """print(snakePosition[i])"""
        


def moveSnake(): #Deplace dans la matrice GRID le serpent
    global coordonneesGoal, grid ,snakeSize, game_over, scoreValue, coordonneesSuperGoal, progress, snakeParity
    #grid = [[0 for x in range(gridWidth)] for y in range(gridHeight)]
    #print(grid)
    if len(snakeDirection) > 1:
        snakeDirection.pop(0)

    moveDirection = directionTable[snakeDirection[0]] #Retourne le Tuple souhaité en selectionnant dans la lookup le nom de la direction
    #print(snakeDirection)

    nextLine =      snakePosition[-1][0] + moveDirection[0]     #Y On stock le numéro de la prochaine ligne 
    nextColumn =    snakePosition[-1][1] + moveDirection[1]     #X On stock le numéro de la prochaine colonne
    nextDirection = moveDirection[2]                            #2 est la case avec l'information de la direction
    # print("\n nextdirection")
    # print(nextDirection)
    firstLine =         snakePosition[0][0]         #Dans le premier tuple je prend Y
    firstColumn  =      snakePosition[0][1]         #Dans le premier tuple je prend X
    firstDirection  =   snakePosition[0][2]      
    # print(snakePosition)   
    # print("prevousLine", firstLine)
    # print("prevousColumn", firstColumn )


    """"COLLISION CHECKER"""
    #print(snakePosition)
    if(nextLine >= 0 and nextLine < gridHeight and nextColumn >= 0 and nextColumn < gridWidth): #On check la collision avec les murs
        snakePosition.pop(0)
        if any(p[0] == nextLine and p[1] == nextColumn for p in snakePosition): #On check la collision avec lui même
            game_over = True
            
        snakePosition.append((nextLine, nextColumn, nextDirection)) #Y, X On applique le mouvement

        if grid[nextLine][nextColumn][0] == cellTypes["GOAL"]: #On check si on a mangé un fruit
            coordonneesGoal = None
            snakeSize += 1
            snakePosition.insert(0, (firstLine, firstColumn, firstDirection)) #on ajoute la dernière position à la liste
            scoreValue +=10
            #print(snakeSize)

        if grid[nextLine][nextColumn][0] == cellTypes["SUPERGOAL"]: #On check si on a mangé un Super fruit
            coordonneesSuperGoal = None
            snakeSize += 1
            snakePosition.insert(0, (firstLine, firstColumn, firstDirection)) #on ajoute la dernière position à la liste
            if(round(100-progress < 10)):
               scoreValue += 10
            else:
                scoreValue += round(100-progress)
            #print(snakeSize)

    else: #Si collision
        game_over = True
        
        """"ECRITURE DE LA GRID"""

    if(grid[firstLine][firstColumn ] != 0): #on nettois dérrière le passage du serpent
        grid[firstLine][firstColumn ][0] = cellTypes["VIDE"] #Y, X
        grid[firstLine][firstColumn ][1] = 0 #Y, X

    for x in range(snakeSize): #on update la grid en fonction du tableau de position du snake
        #print(snakePosition)
        #print("\n\n",grid)
        if(x == snakeSize-1): #Dernière case du serpent
            #grid[y][x][dir]
            grid[snakePosition[x][0]][snakePosition[x][1]][0] = cellTypes["TETE"] 
            grid[snakePosition[x][0]][snakePosition[x][1]][1] = snakePosition[x][2] #on renseigne la direction du serpent

        elif( x == 0):  #Première case du serpent
            grid[snakePosition[x][0]][snakePosition[x][1]][0] = cellTypes["QUEUE"] 
            grid[snakePosition[x][0]][snakePosition[x][1]][1] = snakePosition[x][2] #on renseigne la direction du serpent

        elif(x == snakeSize-2): #Avant dernière case du serpent

            print(grid[snakePosition[x-1][0]][snakePosition[x-1][1]][0])

            if(grid[snakePosition[x-1][0]][snakePosition[x-1][1]][0] == cellTypes["CORPS_IMPAIR"]):
                 grid[snakePosition[x][0]][snakePosition[x][1]][0] = cellTypes["CORPS_PAIR"]

            if(grid[snakePosition[x-1][0]][snakePosition[x-1][1]][0] == cellTypes["CORPS_PAIR"]):
                 grid[snakePosition[x][0]][snakePosition[x][1]][0] = cellTypes["CORPS_IMPAIR"]


        # else:
        #     grid[snakePosition[x][0]][snakePosition[x][1]][0] = cellTypes["CORPS_PAIR"] 
        #     grid[snakePosition[x][0]][snakePosition[x][1]][1] = snakePosition[x][2] #on renseigne la direction du serpent


def spawnGoal(): #Fait apparaitre l'objectif sur le terrain 
    global grid, countSuperGoal
    randomY = 0
    randomX = 0
    countSuperGoal += 1
    while True:
        randomY = random.randint(0,gridHeight - 1)
        randomX = random.randint(0,gridWidth - 1)
        if(randomY, randomX) not in [(p[0], p[1]) for p in snakePosition]:
            grid[randomY][randomX][0] = cellTypes["GOAL"] #Goal
            return(randomY, randomX)

def spawnSuperGoal(): #Fait apparaitre l'objectif sur le terrain 
    global grid, progress
    randomY = 0
    randomX = 0
    progress = 0
    while True:
        randomY = random.randint(0,gridHeight - 1)
        randomX = random.randint(0,gridWidth - 1)
        if(randomY, randomX) not in [(p[0], p[1]) for p in snakePosition]:
            grid[randomY][randomX][0] = cellTypes["SUPERGOAL"] #Supergoal
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
    global grid, coordonneesGoal, coordonneesSuperGoal,snakeSize, snakeDirection, scoreValue, countSuperGoal
    snakePosition.clear()
    snakeSize = snakeSizeStart
    coordonneesGoal = None
    coordonneesSuperGoal = None
    countSuperGoal = 0
    snakeDirection = ["RIGHT"]
    grid = [[[cellTypes["VIDE"],0] for x in range(gridWidth)] for y in range(gridHeight)]
    scoreValue = 0
    
    spawnSnake()

def loadBarre(coordonneesSuperGoal, width, height, left, top, thickness):
    global progress
    #print(progress)
    if coordonneesSuperGoal != None:
        progressCalc = (((width-(thickness+1)*2))*progress)/100
        #print("progressCalc:",progressCalc)

        pygame.draw.rect(screen, (200,0,0), (left, top, width, height), thickness)
        pygame.draw.rect(screen, (255,0,0), (left+thickness+1, top+thickness+1, progressCalc, height-(thickness+1)*2), 0)

        if progress < 100:
            progress += 0.4
    

mariadb.connecter_mariadb()
spawnSnake()

while running:
    #print(grid)
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
        #print(grid)

    loadBarre(coordonneesSuperGoal ,screenSizeWidth/2, 20, screenSizeWidth/4, screenSizeHeight/8, 2)




    currentTime = pygame.time.get_ticks()
    if game_over == False:
        updateMap() #Si on est pas game over on update la map
        if currentTime - lastMoveTime > snakeSpeed:
            # print(grid)
            moveSnake()#On bouge le serpent avec une période défini par snakeSpeed

            lastMoveTime = currentTime
    else:
        #mariadb.ajouter_score_snake("Jean", 250)
        printLoose()


    """"
    for x in range(gridWidth):
        print(grid[x])
    """

    # Texte score
    textScore = scoreFont.render(f"Score: {scoreValue:05} ", True, (255, 255, 255))

    rect = textScore.get_rect(center=(screenSizeWidth/1.4, screenSizeHeight/16))

    screen.blit(textScore, rect)

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
