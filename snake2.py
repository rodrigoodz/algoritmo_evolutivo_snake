import random, pygame, sys,os
from pygame.locals import *

#hacer que no sea visible el juego
#os.environ["SDL_VIDEODRIVER"] = "dummy"

FPS = 10
WINDOWWIDTH = 240  #160
WINDOWHEIGHT = 240 #160
CELLSIZE = 40
assert WINDOWWIDTH % CELLSIZE == 0, "Window width must be a multiple of cell size."
assert WINDOWHEIGHT % CELLSIZE == 0, "Window height must be a multiple of cell size."
CELLWIDTH = int(WINDOWWIDTH / CELLSIZE)
CELLHEIGHT = int(WINDOWHEIGHT / CELLSIZE)

#             R    G    B
WHITE     = (255, 255, 255)
BLACK     = (  0,   0,   0)
RED       = (255,   0,   0)
GREEN     = (  0, 255,   0)
DARKGREEN = (  0, 155,   0)
DARKGRAY  = ( 40,  40,  40)
BLUE     = (0,0,255)
BGCOLOR = WHITE

UP = 1 #'up'           #choice=1
DOWN =2 # 'down'       #choice=2
LEFT =3#'left'       #choice=3
RIGHT =4# 'right'     #choice=4
HEAD = 0 # syntactic sugar: index of the worm's head



def main():
    global FPSCLOCK, DISPLAYSURF, BASICFONT

    pygame.init()
    #pygame.display.iconify()
    FPSCLOCK = pygame.time.Clock()
    DISPLAYSURF = pygame.display.set_mode((WINDOWWIDTH, WINDOWHEIGHT))
    BASICFONT = pygame.font.Font('freesansbold.ttf', 18)
    pygame.display.set_caption('Inteligencia 2019')

    #score,wormCoords,manzana,direction=runGame()

    # #showStartScreen()
    # coordenadas,manzana,puntaje,direc,vivo=inicializar_posiciones()
    # while True:
    #     #s=runGame()
    #     #coordenadas,manzana,puntaje,direc
    #     #wormCoords, apple, score, direction
    #     coordenadas,manzana,puntaje,direc,vivo=run2(coordenadas,manzana,puntaje,direc,vivo)
    #     #coordenadas,manzana,puntaje,direc,vivo=runGame()
    #     print("posiciones: ",coordenadas)
    #     print("score: ",puntaje)
    #     print(manzana)
    #     print(direc)
    #     print("esta vivo=",vivo)
    #     terminate()
    #     #print("manzana:",apple)
    #     #print("direccion:",direction)
    #     #showGameOverScreen()
    # #     puntaje,m,gusano=estado()
    # #     print("score: ",puntaje,"manzana: ",m)
    # #     #accion=controlador(estado)
    # #convenrtiraccion
    # #     #runGame1(accion)
    # #     terminate()

vivo=0

def inicializar_posiciones():
    #startx = random.randint(5, CELLWIDTH)
    #starty = random.randint(5, CELLHEIGHT)
    #vibora fija
    startx = (CELLWIDTH/2)
    starty = (CELLHEIGHT/2)
    wormCoords = [{'x': startx,     'y': starty},
                  {'x': startx - 1, 'y': starty},
                  {'x': startx - 2, 'y': starty}]
    direction = RIGHT
    # Start the apple in a random place.
    del wormCoords[-1]

    apple = getRandomLocation()
    score=len(wormCoords)-4
    vivo=1
    return wormCoords, apple, score, direction, vivo

def run2(wormCoords, apple, score, direction,vivo):
        for event in pygame.event.get():
            if event.type == QUIT:
                terminate()
            # elif event.type == KEYDOWN:
            #     if (event.key == K_LEFT or event.key == K_a) and direction != RIGHT:
            #         direction = LEFT
            #     elif (event.key == K_RIGHT or event.key == K_d) and direction != LEFT:
            #         direction = RIGHT
            #     elif (event.key == K_UP or event.key == K_w) and direction != DOWN:
            #         direction = UP
            #     elif (event.key == K_DOWN or event.key == K_s) and direction != UP:
            #         direction = DOWN
            #     elif event.key == K_ESCAPE:
            #         terminate()
        # comprobar si el gusano se ha golpeado a sí mismo o al borde
        if colisiona(wormCoords,HEAD,CELLWIDTH,CELLHEIGHT):
            vivo=0
            return wormCoords, apple, score, direction, vivo
            #gameover
        #print(direction)



        #  # comprobar si el gusano ha comido una manzana
        #
        #    # no elimine el segmento de cola del gusano

        #     #apple = getRandomLocation() # establecer una nueva manzana en alguna parte
        # else:
        #     del wormCoords[-1]# eliminar el segmento de la cola del gusano

        # mueve el gusano agregando un segmento en la dirección en que se mueve
        if direction == UP:
            newHead = {'x': wormCoords[HEAD]['x'], 'y': wormCoords[HEAD]['y'] - 1}
        elif direction == DOWN:
            newHead = {'x': wormCoords[HEAD]['x'], 'y': wormCoords[HEAD]['y'] + 1}
        elif direction == LEFT:
            newHead = {'x': wormCoords[HEAD]['x'] - 1, 'y': wormCoords[HEAD]['y']}
        elif direction == RIGHT:
            newHead = {'x': wormCoords[HEAD]['x'] + 1, 'y': wormCoords[HEAD]['y']}


        wormCoords.insert(0, newHead)
        score=len(wormCoords)-3
        DISPLAYSURF.fill(BGCOLOR)
        drawGrid()
        apple=drawWorm(wormCoords,apple)
        drawApple(apple)
        drawScore(score)
        pygame.display.update()
        FPSCLOCK.tick(FPS)
        return wormCoords, apple, score, direction,vivo

def terminate():
    pygame.quit()
    sys.exit()

def getRandomLocation():
    return {'x': random.randint(0, CELLWIDTH - 1), 'y': random.randint(0, CELLHEIGHT - 1)}


def drawScore(score):
    scoreSurf = BASICFONT.render('Score: %s' % (score), True, BLACK)
    scoreRect = scoreSurf.get_rect()
    scoreRect.topleft = (WINDOWWIDTH - 120, 3)
    DISPLAYSURF.blit(scoreSurf, scoreRect)


def drawWorm(wormCoords,apple):
    for coord in wormCoords:
        x = coord['x'] * CELLSIZE
        y = coord['y'] * CELLSIZE
        wormSegmentRect = pygame.Rect(x, y, CELLSIZE, CELLSIZE)
        pygame.draw.rect(DISPLAYSURF,(0,0,230), wormSegmentRect)
        wormInnerSegmentRect = pygame.Rect(x + 4, y + 4, CELLSIZE - 8, CELLSIZE - 8)
        pygame.draw.rect(DISPLAYSURF, (0,0,139), wormInnerSegmentRect)
    if wormCoords[HEAD]['x'] == apple['x'] and wormCoords[HEAD]['y'] == apple['y']:
        apple=getRandomLocation()
    else:
        del wormCoords[-1]
    return apple

def drawApple(coord):
    x = coord['x'] * CELLSIZE
    y = coord['y'] * CELLSIZE
    appleRect = pygame.Rect(x, y, CELLSIZE, CELLSIZE)
    pygame.draw.rect(DISPLAYSURF, RED, appleRect)

def drawGrid():
    for x in range(0, WINDOWWIDTH, CELLSIZE): # draw vertical lines
        pygame.draw.line(DISPLAYSURF, (211,211,211), (x, 0), (x, WINDOWHEIGHT))
    for y in range(0, WINDOWHEIGHT, CELLSIZE): # draw horizontal lines
        pygame.draw.line(DISPLAYSURF, (211,211,211), (0, y), (WINDOWWIDTH, y))


def colisiona(wormCoords,HEAD,CELLWIDTH,CELLHEIGHT):
 # comprobar si el gusano se ha golpeado a sí mismo o al borde
    if wormCoords[HEAD]['x'] == -1 or wormCoords[HEAD]['x'] == CELLWIDTH or wormCoords[HEAD]['y'] == -1 or wormCoords[HEAD]['y'] == CELLHEIGHT:
        return 1
     # game over
    for wormBody in wormCoords[1:]:
        #print(wormBody['x'],wormBody['y'])
        if wormBody['x'] == wormCoords[HEAD]['x'] and wormBody['y'] == wormCoords[HEAD]['y']:
         return 1
        # game over

# def generar_boton_direccion(nueva_direccion):
#     boton=0
#     if nueva_direccion == [1,0]:
#         boton=4 #right
#         direction = RIGHT
#     elif nueva_direccion == [-1,0]:
#         boton=3 #left
#         direction = LEFT
#     elif nueva_direccion == [0,1]:
#         boton=2 #down
#         direction = DOWN
#     else:
#         boton=0#up
#         direction = UP
#     return boton,direction
