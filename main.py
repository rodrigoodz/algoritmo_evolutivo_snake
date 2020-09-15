from algoritmo_evolutivo import * #asocio el controlador
import matplotlib.pyplot as plt


np.set_printoptions(precision=5)
total_generaciones=20 #cant. generaciones total


#-------------------------------------------Crear poblacion-------------------------------------------------------
cant_individuos=20 #cant. individuos por generacion
cant_pesos=6
# Tamaño de la poblacion
tam_poblacion = (cant_individuos,cant_pesos)
# Crear la poblacion para la primer generacion
poblacion_actual = np.random.choice(np.arange(-1,1,step=0.0001),size=tam_poblacion,replace=True)
#print(" \n -------------------------------------------------- POBLACION -------------------------------------------------- \n")
#np.set_printoptions(precision=2)
#print(poblacion_actual)
#-----------------------------------------------------------------------------------------------------------------

#mientras llegue al tope de generacion o encuentre una aptitud requerida(por ejemplo,score=100)
fitness_poblacion=[]
max_fitness_generacion=[]
min_fitness_generacion=[]
media_fitness_generacion=[]
var_fitness_poblacion=[]
std_fitness_poblacion=[]
for i in range(total_generaciones):
    print("################################################################ Generacion ",i+1,"################################################################")

    #--------------------------------Evaluar poblacion(calcular fitness de todos los individuos)----------------------------------------
    #calcular fitness de cada individuo
    print(" \n -------------------------------------------------- FITNESS INDIVIDUOS -------------------------------------------------- \n")
    fitness_poblacion=evaluar_poblacion(poblacion_actual)
    max_fitness_generacion.append(np.amax(fitness_poblacion))
    min_fitness_generacion.append(np.amin(fitness_poblacion))
    media_fitness_generacion.append(np.mean(fitness_poblacion))
    var_fitness_poblacion.append(np.var(fitness_poblacion))
    std_fitness_poblacion.append(np.std(fitness_poblacion))
    print("Mejor Fitness Generacion",i+1,": ",max_fitness_generacion[i])
    #print(fitness_poblacion)
    #---------------------------------------------------------------------------------------------------------------------------------
    #-------------------------------------Seleccion de Padres----------------------------------------------------------------------------
    print(" \n --------------------------------------------------  SELECCION --------------------------------------------------n")
    cant_padres_generacion=10
    k=2
    padres=seleccion_metodo_competencia(poblacion_actual, fitness_poblacion, cant_padres_generacion,k)
    #padres=seleccion_elitismo(poblacion_actual,fitness_poblacion,cant_padres_generacion)
    #print(" \n Pesos Padres \n ",padres)
    #-----------------------------------------------------------------------------------------------------------------
    #---------------------------------Cruzas(dos tipos, Single Point y Random Crossover)---------------------------------------------------------------------
    print(" \n --------------------------------------------------  CRUZA -------------------------------------------------- \n")
    cant_hijos=10 #La cantidad de hijos va a depender del modelo de reproduccion -> "Generational Model"(deberia crear una cantidad de hijos igual al TAMAÑO TOTAL de la poblacion y para "(n+n) method" deberia armar una cantidad de hijos igual a la MITAD de la poblacion
    hijos=cruza_rc(padres,cant_hijos)
    #print("\n Pesos Hijos \n",hijos)
    #-----------------------------------------------------------------------------------------------------------------
    #-------------------------------------------------Mutacion------------------------------------------------------------------
    print(" \n --------------------------------------------------  MUTACION -------------------------------------------------- \n")
    p_m=0.10
    hijos_mutados=mutacion_aux(hijos,p_m)
    #print("\n Pesos Hijos Mutados \n",hijos)
    #-----------------------------------------------------------------------------------------------------------------
    #------------------------------------------Crear Nueva Poblacion------------------------------------------------------------------
    #Reemplazo total(Generational Model), reemplaza toda la poblacion con los hijos
    #poblacion_actual=hijos_mutados

    #Brecha Generacional((n+n) Method), elige la mitad de padres con mejores fitness y la mitad de hijos con mejores fitness
    poblacion_actual[0:padres.shape[0], :] = padres
    poblacion_actual[padres.shape[0]:, :] = hijos_mutados

    #print("\n Generacion Siguiente \n",poblacion_actual)
    #-----------------------------------------------------------------------------------------------------------------

print(" \nMayor Fitness Encontrado ->",np.amax(max_fitness_generacion))
print("Menor Fitness Encontrado ->",np.amin(min_fitness_generacion))
print("Fitness Promedio ->",np.mean(media_fitness_generacion)) #promedio todas las generaciones
print("Fitness Promedio Ultima Generacion->",np.mean(media_fitness_generacion[-1])) #promedio ultima generacion
plt.title('Algoritmo Evolutivo')
plt.ylabel('Fitness')
plt.xlabel("Generaciones")
plt.plot(range(1,np.size(max_fitness_generacion)+1,1),max_fitness_generacion,'g', label='max')
plt.plot(range(1,np.size(media_fitness_generacion)+1,1),media_fitness_generacion,'k', label='media')
plt.plot(range(1,np.size(min_fitness_generacion)+1,1),min_fitness_generacion, 'r', label='min')
plt.plot(range(1,np.size(var_fitness_poblacion)+1,1),var_fitness_poblacion, '--c', label='var')
plt.plot(range(1,np.size(std_fitness_poblacion)+1,1),std_fitness_poblacion, '--y', label='var')
plt.gca().legend(('max','media','min','varianza','std'))
plt.show()
