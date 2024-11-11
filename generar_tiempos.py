# generador_tiempos.py
import numpy as np
from generadorNumeros import congruencial_lineal

def generar_tiempos_entre_llegadas(num_clientes, lambd):
    # Generar números aleatorios (Ri) usando tu método congruencial lineal
    Xi, Ri = congruencial_lineal(77, 2, 1, 5, num_clientes)
    AIT = [-np.log(1 - ri) / lambd for ri in Ri]  # Calcular tiempos entre llegadas
    return AIT
