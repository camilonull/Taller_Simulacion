import numpy as np
import pygame
import random

from generadorNumeros import congruencial_lineal, verificacionRi

# Cargar imágenes de los power-ups
powerups = {
    "curar": pygame.transform.scale(pygame.image.load("assets/powerups/salud.png"), (100, 100)),
    "escudo": pygame.transform.scale(pygame.image.load("assets/powerups/escudo.png"), (100, 100)),
    "municion": pygame.transform.scale(pygame.image.load("assets/powerups/bala.png"), (100, 100)),
}

P = np.array([
    [0.4, 0.3, 0.3],  # Desde "curar"
    [0.2, 0.3, 0.5],  # Desde "escudo"
    [0.3, 0.3, 0.4],  # Desde "municion"
])


# Variables internas de estado
_ruleta_mostrando = False
_powerup_seleccionado = None
_tiempo_inicio_ruleta = 0
_tiempo_mostrar_powerup = 0  # Nuevo tiempo para mostrar el power-up seleccionado
duracion_ruleta = 3000  # Duración de la ruleta en milisegundos (3 segundos)
duracion_powerup_ganador = 2000  # Duración del power-up ganador en ms (1 segundo)
escudo_activo = False

# Mostrar la ruleta
def mostrar_ruleta():
    global _ruleta_mostrando, _tiempo_inicio_ruleta
    _ruleta_mostrando = True
    _tiempo_inicio_ruleta = pygame.time.get_ticks()
    _powerup_seleccionado = None  # Resetear selección de power-up

# Aplicar el power-up seleccionado
def aplicar_powerup(powerup, vida_actual_casa, vida_maxima_casa, municion_actual):
    global escudo_activo
    if powerup == "curar":
        vida_actual_casa = min(vida_actual_casa + 300, vida_maxima_casa)  # Curar la casa
    elif powerup == "municion":
        municion_actual += 40
    return vida_actual_casa, municion_actual


# Variable para llevar el control del índice en la secuencia de Ri
indice_Ri = 0

# Nueva función de dibujar_ruleta actualizada
def dibujar_ruleta(ventana, vida_actual_casa, vida_maxima_casa, municion_actual):
    global _ruleta_mostrando, _powerup_seleccionado, indice_Ri, _tiempo_mostrar_powerup
    # Generar un arreglo de números pseudoaleatorios con congruencial lineal
    numerosProbados = False
    while(numerosProbados == False):
          Xi, num_aleatorio_arr = congruencial_lineal(13, 832262, 1013904223, 32, 50)
          numerosProbados = verificacionRi(num_aleatorio_arr)

    # Si la ruleta está mostrando, selecciona el siguiente power-up con la cadena de Markov
    if _ruleta_mostrando:       
        # Elegir el siguiente número de Ri en la secuencia
        num_aleatorio = num_aleatorio_arr[indice_Ri]
        # Si es la primera vez, elegir un power-up inicial aleatorio
        if _powerup_seleccionado is None:
            _powerup_seleccionado = random.choice(list(powerups.keys()))
        else:
            # Seleccionar el siguiente power-up usando la cadena de Markov
            _powerup_seleccionado = seleccionar_powerup_markov(_powerup_seleccionado, num_aleatorio)

        # Aplicar el power-up seleccionado
        vida_actual_casa, municion_actual = aplicar_powerup(_powerup_seleccionado, vida_actual_casa, vida_maxima_casa, municion_actual)

        
        # Detener la ruleta después de mostrar el power-up
        _ruleta_mostrando = False
        
        # Avanzar el índice para usar el siguiente número de Ri en la próxima iteración
        indice_Ri += 1
        if indice_Ri >= len(num_aleatorio_arr):  # Si llegamos al final de la secuencia, reiniciamos el índice
            indice_Ri = 0
      
    return vida_actual_casa, _powerup_seleccionado, municion_actual



def seleccionar_powerup_markov(powerup_actual, num_aleatorio):
    
    # Obtener el índice del power-up actual
    estado_actual = list(powerups.keys()).index(powerup_actual)
    
    # Obtener las probabilidades de transición para el power-up actual
    probabilidades_transicion = P[estado_actual]
    
    # Calcular los intervalos acumulados para la selección del siguiente power-up
    intervalos = np.cumsum(probabilidades_transicion)
    
    # Determinar el siguiente power-up en función del número aleatorio
    siguiente_powerup_idx = np.where(intervalos >= num_aleatorio)[0][0]
    
    # Retornar el siguiente power-up basado en el índice
    return list(powerups.keys())[siguiente_powerup_idx]


# Función para comprobar si la ruleta está mostrándose
def ruleta_mostrando():
    return _ruleta_mostrando
