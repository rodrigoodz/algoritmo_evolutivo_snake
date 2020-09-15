#from Snake import *
from collections import deque
import collections
import numpy as np
from snake2 import *

#determinar para que lado esta yendo la vibora
def direccion_vibora(cuerpo_snake):
    nueva_direccion=[int(cuerpo_snake[0]['x'])-int(cuerpo_snake[1]['x']),int(cuerpo_snake[0]['y'])-int(cuerpo_snake[1]['y'])]
    if nueva_direccion == [1,0]:
        boton=4 #right
    elif nueva_direccion == [-1,0]:
        boton=3 #left
    elif nueva_direccion == [0,1]:
        boton=2 #down
    else: 
        boton=1 #up
    return boton

#definir celdas a las que puede ir la vibora segun su direccion
def posibles_celdas(direccion_snake,cabeza_snake_x,cabeza_snake_y):
    celdas=[]
    if direccion_snake == 1: #up
        celdas = [{'x': cabeza_snake_x,    'y': cabeza_snake_y-1}, #recto
                  {'x': cabeza_snake_x-1, 'y': cabeza_snake_y}, #doblar_izq
                  {'x': cabeza_snake_x+1, 'y': cabeza_snake_y}] #doblar_der
        posibles_elecciones=[1,3,4]
    elif direccion_snake == 2: #down
        celdas = [{'x': cabeza_snake_x,    'y': cabeza_snake_y+1}, #recto
                  {'x': cabeza_snake_x+1, 'y': cabeza_snake_y}, #doblar_izq
                  {'x': cabeza_snake_x-1, 'y': cabeza_snake_y}] #doblar_der
        posibles_elecciones=[2,4,3]
    elif direccion_snake == 3: #left
        celdas = [{'x': cabeza_snake_x-1,    'y': cabeza_snake_y}, #recto
                  {'x': cabeza_snake_x, 'y': cabeza_snake_y+1}, #doblar_izq
                  {'x': cabeza_snake_x, 'y': cabeza_snake_y-1}] #doblar_der
        posibles_elecciones=[3,2,1]
    elif direccion_snake == 4: #right
        celdas = [{'x': cabeza_snake_x+1,    'y': cabeza_snake_y}, #recto
                  {'x': cabeza_snake_x, 'y': cabeza_snake_y-1}, #doblar_izq
                  {'x': cabeza_snake_x, 'y': cabeza_snake_y+1}] #doblar_der
        posibles_elecciones=[4,1,2]
    return celdas,posibles_elecciones

#----------------------------------------------------------------------------------------------------------------------------------------------------------
#Para mover a la izquierda,derecha, arriba y abajo
delta_x = [-1, 1, 0, 0]
delta_y = [0, 0, 1, -1]

def valid(x, y,escenario):
	if x < 0 or x >= len(escenario) or y < 0 or y >= len(escenario[x]):
		return False
	return (escenario[x][y] != 1)
 
def bfs(inicio,objetivo,escenario):
	Q = deque([inicio])
	dist = {inicio: 1}
	while len(Q):
		curPoint = Q.popleft()
		curDist = dist[curPoint]
		if curPoint == objetivo:
			return curDist
		for dx, dy in zip(delta_x, delta_y):
			nextPoint = (curPoint[0] + dx, curPoint[1] + dy)
			if not valid(nextPoint[0], nextPoint[1],escenario) or nextPoint in dist.keys():
				continue
			dist[nextPoint] = curDist + 1
			Q.append(nextPoint)

#-----------
wall, clear, goal = 9, 0, 1	
#bfs 2.0
def bfs2(grid, start):
    queue = collections.deque([[start]])
    seen = set([start])
    while queue:
        path = queue.popleft()
        x, y = path[-1]
        if grid[y][x] == goal:
            return path
        for x2, y2 in ((x+1,y), (x-1,y), (x,y+1), (x,y-1)):
            if 0 <= x2 < CELLWIDTH and 0 <= y2 < CELLHEIGHT and grid[y2][x2] != wall and (x2, y2) not in seen:
                queue.append(path + [(x2, y2)])
                seen.add((x2, y2))
                
def calculo_suavidadyespacio2(cuerpo_snake,siguiente_direccion_x,siguiente_direccion_y,apple):
    #print("VERSION BFS 2.0")
    escenario=np.zeros((CELLHEIGHT,CELLWIDTH))
    escenario_aux=np.zeros((CELLHEIGHT,CELLWIDTH))

    for i in range(len(cuerpo_snake)):
        columna=int(cuerpo_snake[i]['x'])
        fila=int(cuerpo_snake[i]['y'])
        if (columna>=0 and columna<=CELLWIDTH) and (fila>=0 and fila<=CELLHEIGHT):
            escenario[fila,columna]=9

    #calcular BFS a cada posicion de la matrix
    maximo=0
    espacio=0
    for i in range(escenario.shape[0]):
        for j in range(escenario.shape[1]):
            if(escenario[i,j] != 9):
                escenario[i,j]=1
                path = bfs2(escenario,(siguiente_direccion_x,siguiente_direccion_y))
                escenario[i,j]=0
                if (path!=None):
                    espacio+=1
                    escenario_aux[i,j]=len(path)
                    if len(path)>maximo:
                        maximo=len(path)
            else:
                escenario_aux[i,j]=None
    #print("\n",escenario_aux)
    return maximo,espacio





#calculo la 'rating function' de suavidad considerando las coordenadas del cuerpo y una posible direccion(doblar derecha,dobla izquierda o mantenerse recto)
def calculo_suavidadyespacio(cuerpo_snake,siguiente_direccion_x,siguiente_direccion_y,apple): 
    #print("VERSION BFS 1.0")
    escenario=np.zeros((CELLWIDTH,CELLHEIGHT))
    matrix_aux=np.zeros((CELLWIDTH,CELLHEIGHT))
    #considerar el cuerpo de la vibora para no pasar por ella
    for i in range(len(cuerpo_snake)):
        columna=int(cuerpo_snake[i]['x'])
        fila=int(cuerpo_snake[i]['y'])
        if (columna>=0 and columna<=CELLWIDTH) and (fila>=0 and fila<=CELLHEIGHT):
            escenario[fila,columna]=1
    #print(escenario)
    #calcular BFS a cada posicion de la matrix
    maximo=0
    espacio=0
    for i in range(escenario.shape[0]):
        for j in range(escenario.shape[1]):
            aux=bfs((siguiente_direccion_y,siguiente_direccion_x),(i,j),escenario)
            if aux!=None:
                espacio+=1
                if aux>maximo:
                    maximo=aux
            matrix_aux[i,j]=aux
    matrix_aux[int(apple['y']),int(apple['x'])]=99
    #print(matrix_aux,"\n")
    return maximo,espacio

#calcular 'rating manzana'
def calculo_manzana(cuerpo_snake,space,pos_manzana,siguiente_direccion_x,siguiente_direccion_y):
    rating_manzana=0
    escenario=np.zeros((CELLWIDTH,CELLHEIGHT))
    escenario[pos_manzana[0],pos_manzana[1]]=99
    #matrix_aux=np.zeros((CELLWIDTH,CELLHEIGHT))
    # for i in range(len(cuerpo_snake)):
    #     columna=int(cuerpo_snake[i]['x'])
    #     fila=int(cuerpo_snake[i]['y'])
    #     if (columna>=0 and columna<=CELLWIDTH) and (fila>=0 and fila<=CELLHEIGHT):
    #         escenario[fila,columna]=1
    distance=bfs((siguiente_direccion_y,siguiente_direccion_x),(pos_manzana[0],pos_manzana[1]),escenario)
   
    #print("distancia ",distance)
    #print("ESCENARIOOOOOOO: \n",escenario)
    if(distance!=None and space!=0):
        rating_manzana=space/distance
    else:
        rating_manzana=0
    return rating_manzana

def calculo_manzana2(cuerpo_snake,space,pos_manzana,siguiente_direccion_x,siguiente_direccion_y):
    rating_manzana2=0
    escenario=np.zeros((CELLWIDTH,CELLHEIGHT))
    escenario[pos_manzana[0],pos_manzana[1]]=1
    #matrix_aux=np.zeros((CELLWIDTH,CELLHEIGHT))
    # for i in range(len(cuerpo_snake)):
    #     columna=int(cuerpo_snake[i]['x'])
    #     fila=int(cuerpo_snake[i]['y'])
    #     if (columna>=0 and columna<=CELLWIDTH) and (fila>=0 and fila<=CELLHEIGHT):
    #         escenario[fila,columna]=1
    distance=bfs2(escenario,(siguiente_direccion_x,siguiente_direccion_y))
    escenario[pos_manzana[0],pos_manzana[1]]=0
    #print("distancia ",distance)
    #print("ESCENARIOOOOOOO: \n",escenario)
    if(distance!=None and space!=0):
        rating_manzana2=space/len(distance)
    else:
        rating_manzana2=0
    return rating_manzana2
#----------------------------------------------------------------------------------------------------------------------------------------------------------   

def movimiento_incorrecto(celda_siguiente_x,celda_siguiente_y,wormCoords):
    bandera=0
    for i in range(len(wormCoords)):
        if(wormCoords[i]['x']==celda_siguiente_x and wormCoords[i]['y']==celda_siguiente_y): #si choca con su propio cuerpo es un movimiento incorrecto
            bandera=1
    if (celda_siguiente_x<0 or celda_siguiente_x>CELLWIDTH-1) or (celda_siguiente_y<0 or celda_siguiente_y>CELLHEIGHT-1): #si esta fuera del escenario
        bandera=1
    return bandera

def controlador_snake(pesos):
    main()
    wormCoords, apple, score, direction,vivo=inicializar_posiciones()
    cant_celdas=CELLWIDTH*CELLHEIGHT
    
    contador=0
    while vivo:
        contador+=1
        #print(wormCoords)
       #------------------------------ 
       #usado en F(C)
        
        direccion_snake=direccion_vibora(wormCoords)
        #print("coordenadas",wormCoords)
        #print("direccion:",direccion_snake)
        #print("cabeza:",wormCoords[0]['x'],int(wormCoords[0]['y']))
        celdas_siguientes,eleccion_final=posibles_celdas(direccion_snake,wormCoords[0]['x'],int(wormCoords[0]['y']))
        #------------------------------------------------------------
        #Calcular Smoothness y Space
        rating_suavidad=[]
        rating_espacio=[]
        #rating_suavidad2=[]
        #rating_espacio2=[]
        for i in range(len(celdas_siguientes)): #me fijo las tres posibles direcciones_siguientes que puede ir la vibora en la direccion actual
            if (movimiento_incorrecto(celdas_siguientes[i]['x'],celdas_siguientes[i]['y'],wormCoords)==1): #verifico que no haya salida del escenario la direccion_siguiente, si lo hizo pongo su rating_suavidad en 0
                suavidad=0
                espacio=0
                #suavidad2=0
                #espacio2=0
            else:
                #suavidad,espacio=calculo_suavidadyespacio(wormCoords,int(celdas_siguientes[i]['x']),int(celdas_siguientes[i]['y']),apple)
                suavidad,espacio=calculo_suavidadyespacio2(wormCoords,int(celdas_siguientes[i]['x']),int(celdas_siguientes[i]['y']),apple)
            rating_suavidad.append(suavidad)
            rating_espacio.append(espacio)
            #rating_suavidad2.append(suavidad2)
            #rating_espacio2.append(espacio2)
        #------------------------------------------------------------
        #Calcular Score Manzana
        columna_manzana=int(apple['x'])
        fila_manzana=int(apple['y'])
        pos_manzana=[fila_manzana,columna_manzana]
        rating_manzana=[]
        #rating_manzana2=[]
        for i in range(len(celdas_siguientes)):
            if (movimiento_incorrecto(celdas_siguientes[i]['x'],celdas_siguientes[i]['y'],wormCoords)==1):
                manzana=0
                manzana2=0
            else:
                #manzana=calculo_manzana(wormCoords,rating_espacio[i],pos_manzana,int(celdas_siguientes[i]['x']),int(celdas_siguientes[i]['y']))
                manzana=calculo_manzana2(wormCoords,rating_espacio[i],pos_manzana,int(celdas_siguientes[i]['x']),int(celdas_siguientes[i]['y']))
            rating_manzana.append(manzana)  
            #rating_manzana2.append(manzana2)  
        #------------------------------------------------------------
        # print(" \n RATING SUAVIDAD")
        # print(rating_suavidad,"\n")
        # print(" \n RATING SUAVIDAD 2")
        # print(rating_suavidad2,"\n")

        # print(" \n RATING ESPACIO")
        # print(rating_espacio,"\n")
        # print(" \n RATING ESPACIO 2")
        # print(rating_espacio2,"\n")

        # print(" \n RATING MANZANA")
        # print(rating_manzana,"\n") 

        # print(" \n RATING MANZANA 2")
        # print(rating_manzana2,"\n")
        
         

        #calcular para cada posible direccion, la suma ponderada de smoothness,space y rating_manzana
        F=[]
        for c in range(len(celdas_siguientes)):
            suma_ponderada=(rating_suavidad[c]*(pesos[0]+(pesos[1]*(len(wormCoords)/cant_celdas)))) + (rating_espacio[c]*(pesos[2]+(pesos[3]*(len(wormCoords)/cant_celdas)))) + (rating_manzana[c]*(pesos[4]+(pesos[5]*(len(wormCoords)/cant_celdas))))
            F.append(suma_ponderada)
        
       # print(F)
        F=np.abs(F)
        #print(F)

        # #----------BORRAR-----------------
        # F2=[]
        # for c in range(len(celdas_siguientes)):
        #     suma_ponderada=(rating_suavidad2[c]*(pesos[0]+(pesos[1]*(len(wormCoords)/cant_celdas)))) + (rating_espacio2[c]*(pesos[2]+(pesos[3]*(len(wormCoords)/cant_celdas)))) + (rating_manzana2[c]*(pesos[4]+(pesos[5]*(len(wormCoords)/cant_celdas))))
        #     F2.append(suma_ponderada)
        
        # # F=np.absolute(F)
        # # print(F)
        # F2=np.abs(F2)
        # #print(F2)
        # if np.array_equal(F2,F):
        #     print("")
        # else:
        #     print("NO SON IGUALES")

        # #----------------------------------------------

        #La eleccion que tenga un valor mas grande sera tomada para el siguiente movimiento
        posicion_max=np.argmax(F) 
       # print(posicion_max)
        #en base al maximo y a la direccion que tenia la vibora anteriormente, voy a decidir el "choice" final
        choice=eleccion_final[posicion_max]
        #print(choice)
    #------------------------------
       # print("ELECCION:",choice)
        
        wormCoords, apple, score, direction,vivo=run2(wormCoords, apple, score, choice,vivo)
        #print(wormCoords)
        #print(contador)
        cant_movimientos_totales=600
        if contador==cant_movimientos_totales:
            vivo=0
        

        pasos_restantes=cant_movimientos_totales-contador
       
        fitness=(score/(CELLWIDTH*CELLHEIGHT))+(pasos_restantes/cant_movimientos_totales)
        #wait = input("PRESS ENTER TO CONTINUE.")
    return score,pasos_restantes,fitness



#---------------------------
#pesos=[7,7,7,7,15,15]
#controlador_snake(pesos)
    

