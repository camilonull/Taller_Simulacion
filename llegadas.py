import tkinter as tk
import numpy as np
import time
import threading

from generadorNumeros import congruencial_lineal

# Parámetros
lambd = 1  # tasa de llegada (lambda)
num_clientes = 20  # número de clientes

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

# Método propio de generación de números aleatorios
def mi_generador_aleatorio():
    # Implementa tu propio método de generación de números aleatorios
    return np.random.uniform(0, 1)

# Función para mover un cuadro en una caminata aleatoria con mayor probabilidad de moverse a la izquierda
def mover_cuadro(canvas, rect):
    while True:
        # Obtener la posición actual del cuadro
        x1, y1, x2, y2 = canvas.coords(rect)
        if x1 <= 0 or y1 <= 0:  # Si alcanza la esquina superior izquierda, detener
            break

        # Generar un número aleatorio con tu método
        num_aleatorio = mi_generador_aleatorio()

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
