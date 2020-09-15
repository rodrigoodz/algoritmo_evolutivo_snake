import numpy as np
import random
from controlador import *

#Evaluamos la poblacion: 
#Para cada individuo calculamos su fitness, esto quiere decir que hariamos jugar a cada serpiente con determinados pesos dados y devolvemos el score que hizo con esos pesos
def evaluar_poblacion(poblacion):
    fitness=[]
    #print(poblacion)
   # print((poblacion * 15.0))
    for i in range(poblacion.shape[0]): #for i=0 hasta cant_filas(individuos)
        aux=poblacion[i]* 15.0
        score,pasos_restantes,fitn=controlador_snake(aux)   #llamamos al controlador con los pesos del individuo
        print("Fitness del individuo",i+1,"->",fitn,"// Cromosoma del Individuo:",poblacion[i,:], "// Pasos Restantes: ",pasos_restantes,"     Puntaje",i+1,":",score) #mostramos su score
        fitness.append(score)     #guardamos el score en fitness[]
    return np.array(fitness)


#Seleccion de padres
#Realizamos la seleccion de padres mediante el Metodo de torneo con k
def seleccion_metodo_competencia(poblacion, fitness_individuos, cant_padres_generacion,k):
    ganadores = np.empty((cant_padres_generacion, poblacion.shape[1])) #matriz de padres, filas = cant. padres que queremos, columnas=pesos
    N=poblacion.shape[0] #cantidad de individuos en la poblacion
    for i in range(cant_padres_generacion):  #seleccionaremos una cantidad igual a 'cant_padres_generacion' de padres
        competidores=[]
        fitness_competidores=[]
        for j in range(k): #metodo de torneo con k
            aux=random.randint(0, N-1) #selecciono un individuo al azar
            competidores.append(aux) #adjunto el individuo a lista de competidores
            fitness_competidores.append(fitness_individuos[aux]) #adjunto una lista con los fitness de los competidores
        maximo_fitness=max(fitness_competidores)  #de la lista de fitness[] 'tomo' el maximo
        posicion_max_fitness=fitness_competidores.index(max(fitness_competidores)) #hallo la posicion de la lista de fitness[] donde esta el maximo
        ganador_numero=competidores[posicion_max_fitness] #localizo en el vector competidores[] el ganador
        print("Competidores seleccionados [ iteracion",i+1,"]",competidores,"// Fitness del individuo",fitness_competidores,"GANADOR ->",ganador_numero)
        ganadores[i, :] = poblacion[ganador_numero,:] #retorno los pesos de los ganadores
    return ganadores

def seleccion_elitismo(poblacion, fitness_individuos, cant_padres_generacion):
    # Selecting the best individuals in the current generation as parents for producing the offspring of the next generation.
    padres = np.empty((cant_padres_generacion, poblacion.shape[1]))
    fitness_individuos_aux=fitness_individuos
    for i in range(cant_padres_generacion):
        max_fitness_idx = np.where(fitness_individuos_aux == np.max(fitness_individuos_aux))
        max_fitness_idx = max_fitness_idx[0][0]
        padres[i, :] = poblacion[max_fitness_idx, :]
        print("Seleccion Padres [ iteracion",i+1,"] // Individuo",max_fitness_idx+1," Fitness del individuo ->",fitness_individuos[max_fitness_idx])
        fitness_individuos_aux[max_fitness_idx] = -99999999 
    return padres

#Cruza
#Dos tipos, Single Point y Cruza Aleatoria
def cruza_sp(padres,tam_descendencia):
    hijos=np.empty((tam_descendencia,padres.shape[1])) #matriz con filas=cant_hijos y columnas=pesos(posibles cromosomas nueva generacion)
    for m in range(tam_descendencia): #hasta formar todos los hijos
        #selecciono 2 padres al azar
        padre1 = random.randint(0, padres.shape[0] - 1)
        padre2 = random.randint(0, padres.shape[0] - 1)
        punto_corte=random.randint(1,padres.shape[1]-1) #punto de corte aleatorio entre 1 y 7
        hijos[m, 0:punto_corte] = padres[padre1, 0:punto_corte] #primera parte del hijo
        hijos[m, punto_corte:] = padres[padre2, punto_corte:] #segunda parte del hijo
        print("Cruza Padres [ Iteracion",m+1,"]","//","pto. de corte",punto_corte,"// Padre",padre1,"->",padres[padre1, :]," Padre",padre2,"->",padres[padre2, :],"Pesos del Hijo",hijos[m,:])
    return hijos

def cruza_rc(padres,tam_descendencia):
    hijos=np.empty((tam_descendencia,padres.shape[1])) #matriz con filas=cant_hijos y columnas=pesos
    for m in range(tam_descendencia): #hasta formar todos los hijos
        #selecciono 2 padres al azar
        padre1 = random.randint(0, padres.shape[0] - 1)
        padre2 = random.randint(0, padres.shape[0] - 1)
        #print("Cruza Padres [ Iteracion",m+1,"]","// Padre",padre1,"->",padres[padre1, :]," Padre",padre2,"->",padres[padre2, :],end=' ')
        for j in range(padres.shape[1]):
            if random.random() < 0.5:
                aux=padres[padre1, j] #guardo en aux el indice j del padre 1
                padres[padre1, j] = padres[padre2, j] #reemplazo el indice j del padre 1 con el indice j del padre 2
                padres[padre2, j] = aux #lo que guarde en aux, lo coloco en indice j del padre 2
        hijos[m,:]=padres[padre1, :]
        print("Pesos del Hijo",hijos[m,:])
    return hijos

#simple con dos hijos
def cruza_sp_2(padres,tam_descendencia):
    hijos=np.empty((tam_descendencia,padres.shape[1])) #matriz con filas=cant_hijos y columnas=pesos(posibles cromosomas nueva generacion)
    for m in range(0,tam_descendencia,2): #hasta formar todos los hijos
        #selecciono 2 padres al azar
        padre1 = random.randint(0, padres.shape[0] - 1)
        padre2 = random.randint(0, padres.shape[0] - 1)
        punto_corte=random.randint(1,padres.shape[1]-1) #punto de corte aleatorio entre 1 y 7
        hijos[m, 0:punto_corte] = padres[padre1, 0:punto_corte] #primera parte del hijo
        hijos[m, punto_corte:] = padres[padre2, punto_corte:] #segunda parte del hijo
        #hijo 2
        hijos[m+1, 0:punto_corte] = padres[padre2, 0:punto_corte] #primera parte del hijo
        hijos[m+1, punto_corte:] = padres[padre1, punto_corte:] #segunda parte del hijo
        print("Cruza Padres [ Iteracion",m+1,"]","//","pto. de corte",punto_corte,"// Padre",padre1,"->",padres[padre1, :]," Padre",padre2,"->",padres[padre2, :],"Pesos del Hijo1",hijos[m,:],' ',"Pesos del Hijo 2",hijos[m+1,:] )
    return hijos





#Mutacion, cambiamos con cierta probabilidad dada, un gen de un cromosoma de la poblacion
# def mutacion(hijos,porcentaje_mutacion):
#     for i in range(hijos.shape[0]):
#         if random.random() < porcentaje_mutacion:
#             indice=random.randint(0,hijos.shape[1]-1)
#             valor_aleatorio = np.random.uniform(-1.0, 1.0, 1)
#             hijos[i,indice]=hijos[i,indice] + valor_aleatorio
#     return hijos

def mutacion(hijos,porcentaje_mutacion):
    for i in range(hijos.shape[0]):
        for j in range(hijos.shape[1]):
            if random.random() < porcentaje_mutacion:
                #indice=random.randint(0,hijos.shape[1]-1)
                valor_aleatorio = np.random.uniform(-1.0, 1.0, 1)
                hijos[i,j]=hijos[i,j] + valor_aleatorio
    return hijos

def mutacion_aux(hijos,porcentaje_mutacion):
    n1=hijos.shape[0]*porcentaje_mutacion
    n=round(n1)
    for i in range(n):
        aleatorio=random.randint(0, hijos.shape[0] - 1)
        aleatorio2=random.randint(0, hijos.shape[1] - 1)
        valor_aleatorio = np.random.uniform(-1.0, 1.0, 1)
        print("Hijo Original ->",hijos[aleatorio,:],end=' ')
        hijos[aleatorio,aleatorio2]=hijos[aleatorio,aleatorio2] + valor_aleatorio
        if(hijos[aleatorio,aleatorio2]>1):
            hijos[aleatorio,aleatorio2]=1
        elif (hijos[aleatorio,aleatorio2]<-1):
            hijos[aleatorio,aleatorio2]=-1  
        print("Hijo Mutado ->",hijos[aleatorio,:])
    return hijos

