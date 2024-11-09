import tkinter as tk
import numpy as np
import time

# Parámetros
lambd = 1  # tasa de llegada (lambda)
num_clientes = 20  # número de clientes

# Generar números aleatorios uniformes (Ri) y tiempos inter-arrival (AIT)
Ri = np.random.uniform(0, 1, num_clientes)
AIT = -np.log(1 - Ri) / lambd  # Tiempos entre llegadas

# Crear la ventana principal
root = tk.Tk()
root.title("Simulación de Llegadas")
root.geometry("600x400")

# Función para mostrar cuadros de colores
def mostrar_cuadros():
    canvas = tk.Canvas(root, width=600, height=400)
    canvas.pack()
    colores = ['red', 'green', 'blue', 'yellow', 'orange', 'purple']

    for i, tiempo in enumerate(AIT):
        color = np.random.choice(colores)
        x1, y1 = 50 * (i % 10), 50 * (i // 10)
        x2, y2 = x1 + 40, y1 + 40
        
        # Crear un cuadro en el canvas
        canvas.create_rectangle(x1, y1, x2, y2, fill=color)
        root.update()  # Actualizar la ventana
        time.sleep(tiempo)  # Esperar el tiempo correspondiente entre llegadas

# Llamar a la función para mostrar cuadros después de iniciar la interfaz
root.after(1000, mostrar_cuadros)
root.mainloop()
