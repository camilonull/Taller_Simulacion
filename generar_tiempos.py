# generador_tiempos.py
import random
import numpy as np
from generadorNumeros import congruencial_lineal, verificacionRi

def generar_tiempos_entre_llegadas(num_clientes, lambd):
    # Generar números aleatorios (Ri) usando tu método congruencial lineal
    semillas = [77,13,55,20,90,4434]
    numerosProbados = False
    AIT = []
    while(numerosProbados == False):
          Xi, Ri = congruencial_lineal(random.choice(semillas), 832262, 1013904223, 32, num_clientes)
          numerosProbados = verificacionRi(Ri)
    
    
    # Validar que no haya valores de Ri cercanos a 1, para evitar infinito
    for ri in Ri:
        if ri == 1:
            ri = 1 - 1e-10  # Asegurarse de que no sea exactamente 1
        AIT.append(-np.log(1 - ri) / lambd)  # Calcular tiempos entre llegadas

    return AIT

