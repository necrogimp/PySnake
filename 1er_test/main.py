import pygame
import time
import random

pygame.init()

#Constantes
gridWidth = 10
gridHeight = 10

paddingGrid = 21

screenSizeWidth = 1000
screenSizeHeight = 1000

running = True
cercle_x = 100

screen = pygame.display.set_mode((screenSizeWidth, screenSizeHeight))
clock = pygame.time.Clock()



grid = [[0 for x in range(gridWidth)] for y in range(gridHeight)]

for y in range(gridHeight):
    for x in range(gridWidth):
        grid[y][x] = random.randint(0,1)


for x in range(gridWidth):
    print(grid[x])

def printCircle(couleur):
    pygame.draw.circle(
        screen,
        couleur,
        ((screenSizeWidth/2)-(gridWidth*20)/2+(paddingGrid*column),
         (screenSizeHeight/2)-(gridHeight*20)/2+(paddingGrid*line)),
         10)

while running:

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    screen.fill((0,0,0))

    for line in range(gridWidth):
        for column in range(gridHeight):
            if grid[line][column] == 0:
                #pygame.draw.circle(screen,(255,255,255),((screenSizeWidth/2)-(gridWidth*20)/2+(20*column),(screenSizeHeight/2)-(gridHeight*20)/2+(20*line)),10)
                printCircle((200,150,65))
            else: 
                printCircle((20,150,65))

    pygame.display.flip()
    clock.tick(60)

pygame.quit()