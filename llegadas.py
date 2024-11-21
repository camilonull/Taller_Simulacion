import tkinter as tk
import numpy as np
import time
import threading

from generadorNumeros import congruencial_lineal

# Parámetros
lambd = 100  # tasa de llegada (lambda)
num_clientes = 5  # número de clientes

# Generar números aleatorios uniformes (Ri) y tiempos inter-arrival (AIT)
Xi, Ri = congruencial_lineal(77, 2, 1, 5, num_clientes)
AIT = []
for i in range(len(Ri)):
    AIT.append(-np.log(1 - Ri[i]) / lambd)  # Tiempos entre llegadas


# Convertir los tiempos de llegada a milisegundos para usar en `root.after`
AIT_ms = []
for i in range(len(AIT)):
    AIT_ms.append((AIT[i] * 1000).astype(int))

# Crear la ventana principal
root = tk.Tk()
root.title("Simulación de Llegadas")
root.geometry("800x600")


# Función para mover un cuadro en una caminata aleatoria con mayor probabilidad de moverse a la izquierda
def mover_cuadro(canvas, rect):
    while True:
        # Obtener la posición actual del cuadro
        x1, y1, x2, y2 = canvas.coords(rect)
        if x1 <= 0 or y1 <= 0:  # Si alcanza la esquina superior izquierda, detener
            break

        # Generar un número aleatorio con tu método
        num_aleatorio = congruencial_lineal(13, 2, 1, 5, 100)

        # Definir los movimientos posibles y sus probabilidades
        movimientos = [(-2, 0), (0, -2), (0, 2)]  # Izquierda, arriba, abajo
        probabilidades = [0.4, 0.4, 0.2]  # Mayor probabilidad de moverse a la izquierda

        # Determinar el movimiento basado en el número generado y las probabilidades
        if num_aleatorio < probabilidades[0]:  # Probabilidad de moverse a la izquierda
            dx, dy = movimientos[0]
        elif num_aleatorio < sum(probabilidades[:2]):  # Probabilidad de moverse hacia arriba
            dx, dy = movimientos[1]
        else:  # Probabilidad de moverse hacia abajo
            dx, dy = movimientos[2]

        # Mover el cuadro
        canvas.move(rect, dx, dy)
        time.sleep(0.01)  # Pausa para la animación

# Función para mostrar un cuadro y moverlo
def mostrar_cuadro(canvas):
    colores = ['red', 'green', 'blue', 'yellow', 'orange', 'purple']
    color = np.random.choice(colores)
    # Crear un cuadro en la esquina inferior derecha (respawn)
    rect = canvas.create_rectangle(750, 550, 790, 590, fill=color)
    # Mover el cuadro en un hilo separado
    threading.Thread(target=mover_cuadro, args=(canvas, rect)).start()

# Función para iniciar la aparición de cuadros respetando los tiempos entre llegadas
def iniciar_simulacion(canvas):
    
    for i, tiempo in enumerate(AIT_ms):
        # Usar `root.after` para programar la aparición de cada cuadro
        root.after(sum(AIT_ms[:i+1]), lambda: mostrar_cuadro(canvas))

# Crear el canvas
canvas = tk.Canvas(root, width=800, height=600)
canvas.pack()

# Iniciar la simulación
iniciar_simulacion(canvas)

# Iniciar la ventana principal
root.mainloop()


# Definir la matriz de transición (4 estados)
P = np.array([[0.1, 0.3, 0.4, 0.2],  # Desde el estado 0
              [0.2, 0.5, 0.1, 0.2],  # Desde el estado 1
              [0.3, 0.2, 0.3, 0.2],  # Desde el estado 2
              [0.4, 0.3, 0.1, 0.2]]) # Desde el estado 3

# Definir una función que simula la transición de estados usando Monte Carlo
def simular_cadena_markov(P, estado_inicial, num_pasos):
    estado_actual = estado_inicial
    secuencia_estados = [estado_actual]  # Guarda la secuencia de estados
    Xi, num_aleatorio = congruencial_lineal(13, 832262, 1013904223, 32, num_pasos)

    for i in range(num_pasos):
        # Generar un número aleatorio
        num = num_aleatorio[i]
        # Obtener las probabilidades de transición para el estado actual
        probabilidades_transicion = P[estado_actual]
        print(probabilidades_transicion)
        # Calcular los intervalos acumulados para la selección del próximo estado
        intervalos = np.cumsum(probabilidades_transicion)

        # Determinar el siguiente estado en función del número aleatorio
        siguiente_estado = np.where(intervalos >= num)[0][0]

        # Actualizar el estado actual
        estado_actual = siguiente_estado
        secuencia_estados.append(estado_actual)

    return secuencia_estados

# Parámetros
estado_inicial = 0  # El estado inicial es 0
num_pasos = 10  # Número de pasos a simular

# Simular la cadena de Markov
secuencia = simular_cadena_markov(P, estado_inicial, num_pasos)

# Mostrar los resultados
print(f"Secuencia de estados simulada: {secuencia}")
