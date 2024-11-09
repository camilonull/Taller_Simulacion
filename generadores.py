import tkinter as tk  # Importamos el módulo tkinter para crear interfaces gráficas.
from tkinter import messagebox  # Importamos messagebox para mostrar mensajes emergentes.
import matplotlib.pyplot as plt  # Importamos matplotlib para graficar.
import numpy as np  # Importamos numpy para manejar operaciones matemáticas y arrays.
import random  # Importamos random para generar números aleatorios.
from scipy.stats import norm  # Importamos norm de scipy para trabajar con distribuciones normales.

# Funciones de generación de números

def cuadrados_medios(seed, n, min_val, max_val):
    """Genera números pseudoaleatorios usando el método de cuadrados medios."""
    x = seed  # Inicializa la semilla.
    result = []  # Lista para almacenar los resultados generados.
    resultRi = [] # Lista para almacenar los Ri generados.
    resultXi = [] # Lista para almacenar los Xi generados.
    m = 10 ** len(str(seed))  # Calcula el máximo basado en el tamaño de la semilla.
    
    for _ in range(n):  # Repite el proceso n veces.
        square = str(x**2).zfill(8)  # Calcula el cuadrado de x y lo formatea a 8 dígitos.
        x = int(square[len(square)//2-2:len(square)//2+2])  # Toma el medio del cuadrado como nuevo x.
        Ri = x / m  # Normaliza el número para que esté en [0, 1].
        Ni = min_val + (max_val - min_val) * Ri  # Escala al rango [min_val, max_val].
        resultRi.append(Ri)
        resultXi.append(x)
        result.append(Ni)  # Agrega el número generado a la lista de resultados.
    
    return resultXi, resultRi, result  # Retorna la lista de números generados.

def congruencial_lineal(seed, k, c, g, n, min_val, max_val):
    """Genera números pseudoaleatorios usando el método congruencial lineal."""
    x = seed  # Inicializa la semilla.
    a = 1 + 2 * k  # Calcula el multiplicador.
    m = 2**g  # Calcula el módulo.
    result = []  # Lista para almacenar los resultados generados.
    resultXi = []  # Lista para almacenar los Xi generados.
    resultRi = []  # Lista para almacenar los Ri generados.
    
    for _ in range(n):  # Repite el proceso n veces.
        x = (a * x + c) % m  # Calcula el siguiente valor de x.
        Ri = x / m  # Normaliza el número para que esté en [0, 1).
        Ni = min_val + (max_val - min_val) * Ri  # Escala al rango [min_val, max_val].
        resultXi.append(x) 
        resultRi.append(Ri) 
        result.append(Ni)  # Agrega el número generado a la lista de resultados.
    
    return resultXi, resultRi, result  # Retorna el último Ri y la lista de resultados.

def congruencial_multiplicativa(seed, t, g, n, min_val, max_val):
    """Genera números pseudoaleatorios usando el método congruencial multiplicativa."""
    x = seed  # Inicializa la semilla.
    a = 8 * t + 3  # Calcula el multiplicador.
    m = 2**g  # Calcula el módulo.
    result = []  # Lista para almacenar los resultados generados.
    resultXi = []  # Lista para almacenar los Xi generados.
    resultRi = []  # Lista para almacenar los Ri generados.
    
    for _ in range(n):  # Repite el proceso n veces.
        x = (a * x) % m  # Calcula el siguiente valor de x.
        Ri = x / m  # Normaliza el número para que esté en [0, 1).
        Ni = min_val + (max_val - min_val) * Ri  # Escala al rango [min_val, max_val].
        result.append(Ni)  # Agrega el número generado a la lista de resultados.
        resultXi.append(x) 
        resultRi.append(Ri) 
    
    return resultXi, resultRi, result  # Retorna el último Ri y la lista de resultados.

def distribucion_uniforme(n, min_val, max_val):
    """Genera números aleatorios con distribución uniforme."""
    resultados = []  # Lista para almacenar los números generados.
    Ri = []  # Lista para almacenar los valores de Ri.

    for _ in range(n):  # Repite el proceso n veces.
        ri = random.uniform(0, 1)  # Genera un número aleatorio Ri entre 0 y 1.
        Ri.append(ri)  # Agrega Ri a la lista.
        resultados.append(min_val + (max_val - min_val) * ri)  # Escala Ri al rango [min_val, max_val].

    return Ri, resultados  # Retorna la lista de Ri y la lista de números generados.

def distribucion_normal_inversa(n, min_val, max_val):
    """Genera números pseudoaleatorios usando la distribución normal inversa."""
    # Paso 1: Generar valores aleatorios entre min_val y max_val
    valores_aleatorios = np.random.uniform(min_val, max_val, n)
    
    # Paso 2: Generar números aleatorios entre 0 y 1
    numeros_entre_0_y_1 = np.random.uniform(0, 1, n)
    
    # Paso 3: Sumar ambos conjuntos de valores para obtener las semillas
    semillas = valores_aleatorios + numeros_entre_0_y_1
    
    # Paso 4: Calcular la media y desviación estándar de las semillas
    media_semillas = np.mean(semillas)
    desviacion_semillas = np.std(semillas)
    
    # Paso 5: Crear Ri
    Ri = np.random.uniform(0, 1, n)

    # Paso 6: Generar nuevos números con distribución normal inversa
    resultados = norm.ppf(Ri, loc=media_semillas, scale=desviacion_semillas)
    
    return semillas, Ri, resultados  # Retorna las semillas, Ri y los resultados generados.

def distribucion_normal_estandar_inversa(n):
    """Genera números pseudoaleatorios usando la distribución normal estándar inversa."""
    # Paso 1: Crear Ri
    Ri = np.random.uniform(0, 1, n)

    # Paso 2: Generar nuevos números con distribución normal estándar inversa
    resultados = norm.ppf(Ri, loc=0, scale=1)  # Cambiar a media 0 y desviación estándar 1 para normal estándar

    return Ri, resultados  # Retorna Ri y los resultados generados.

# Función para graficar y mostrar resultados en un plano cartesiano
def graficar_y_mostrar_resultados(resultados, titulo, metodo):
    """Muestra los resultados en un gráfico de dispersión y en un título específico."""
    plt.figure(figsize=(8, 5))  # Define el tamaño de la figura.
    
    plt.scatter(range(len(resultados)), resultados, color='blue', alpha=0.7)  # Ubica los puntos en el gráfico.
    plt.title(titulo)  # Establece el título del gráfico.
    plt.xlabel('Índice')  # Etiqueta del eje x.
    plt.ylabel('Valor generado')  # Etiqueta del eje y.
    
    # Añadir resultados en el gráfico
    for i, valor in enumerate(resultados):
        plt.annotate(f'{valor:.2f}', (i, valor), textcoords="offset points", xytext=(0,10), ha='center', fontsize=8)

    plt.grid(True)  # Activa la cuadrícula.
    plt.show()  # Muestra el gráfico.

# Función para guardar los resultados en un archivo .txt
def guardar_en_archivo(resultados, metodo):
    """Guarda los resultados generados en un archivo de texto."""
    with open(f"resultados_{metodo}.txt", "w") as f:  # Abre (o crea) un archivo para escribir.
        for num in resultados:  # Itera sobre cada número generado.
            f.write(f"{num}\n")  # Escribe el número en el archivo.
    messagebox.showinfo("Guardado", f"Resultados guardados en 'resultados_{metodo}.txt'")  # Mensaje de confirmación.

# Crear ventanas secundarias para cada método
def crear_ventana_cuadrados_medios():
    """Crea la interfaz para el método de cuadrados medios."""
    ventana_cuadrados = tk.Toplevel()  # Crea una nueva ventana.
    ventana_cuadrados.title("Cuadrados Medios")  # Establece el título de la ventana.

    # Crea las etiquetas y entradas para los parámetros
    tk.Label(ventana_cuadrados, text="Semilla:").grid(row=0, column=0)
    entrada_seed = tk.Entry(ventana_cuadrados)
    entrada_seed.grid(row=0, column=1)

    tk.Label(ventana_cuadrados, text="Número de Números (n):").grid(row=1, column=0)
    entrada_n = tk.Entry(ventana_cuadrados)
    entrada_n.grid(row=1, column=1)

    tk.Label(ventana_cuadrados, text="Valor mínimo:").grid(row=2, column=0)
    entrada_min = tk.Entry(ventana_cuadrados)
    entrada_min.grid(row=2, column=1)

    tk.Label(ventana_cuadrados, text="Valor máximo:").grid(row=3, column=0)
    entrada_max = tk.Entry(ventana_cuadrados)
    entrada_max.grid(row=3, column=1)

    def ejecutar_cuadrados_medios():
        """Ejecuta la generación de números usando cuadrados medios y muestra los resultados."""
        seed = int(entrada_seed.get())  # Obtiene la semilla ingresada.
        n = int(entrada_n.get())  # Obtiene el número de números a generar.
        min_val = float(entrada_min.get())  # Obtiene el valor mínimo.
        max_val = float(entrada_max.get())  # Obtiene el valor máximo.
        
        Xi, Ri, resultados = cuadrados_medios(seed, n, min_val, max_val)  # Genera los números.

        # Concatenar los resultados para mostrarlos en el mensaje
        resultados_mensaje = f"Números generados: {resultados}\nXi generados: {Xi}\nRi generados: {Ri}"
    
        # Muestra los resultados generados
        messagebox.showinfo("Resultados", resultados_mensaje)
        graficar_y_mostrar_resultados(resultados, "Resultados de Cuadrados Medios", "cuadrados_medios")  # Grafica los resultados.
        guardar_en_archivo(resultados, "cuadrados_medios")  # Guarda los resultados en un archivo.

    tk.Button(ventana_cuadrados, text="Generar", command=ejecutar_cuadrados_medios).grid(row=4, column=0, columnspan=2)

def crear_ventana_congruencial_lineal():
    """Crea la interfaz para el método de congruencial lineal."""
    ventana_lineal = tk.Toplevel()  # Crea una nueva ventana.
    ventana_lineal.title("Congruencial Lineal")  # Establece el título de la ventana.

    # Crea las etiquetas y entradas para los parámetros
    tk.Label(ventana_lineal, text="Semilla:").grid(row=0, column=0)
    entrada_seed = tk.Entry(ventana_lineal)
    entrada_seed.grid(row=0, column=1)

    tk.Label(ventana_lineal, text="k:").grid(row=1, column=0)
    entrada_k = tk.Entry(ventana_lineal)
    entrada_k.grid(row=1, column=1)

    tk.Label(ventana_lineal, text="c:").grid(row=2, column=0)
    entrada_c = tk.Entry(ventana_lineal)
    entrada_c.grid(row=2, column=1)

    tk.Label(ventana_lineal, text="g:").grid(row=3, column=0)
    entrada_g = tk.Entry(ventana_lineal)
    entrada_g.grid(row=3, column=1)

    tk.Label(ventana_lineal, text="Número de Números (n):").grid(row=4, column=0)
    entrada_n = tk.Entry(ventana_lineal)
    entrada_n.grid(row=4, column=1)

    tk.Label(ventana_lineal, text="Valor mínimo:").grid(row=5, column=0)
    entrada_min = tk.Entry(ventana_lineal)
    entrada_min.grid(row=5, column=1)

    tk.Label(ventana_lineal, text="Valor máximo:").grid(row=6, column=0)
    entrada_max = tk.Entry(ventana_lineal)
    entrada_max.grid(row=6, column=1)

    def ejecutar_congruencial_lineal():
        """Ejecuta la generación de números usando congruencial lineal y muestra los resultados."""
        seed = int(entrada_seed.get())  # Obtiene la semilla ingresada.
        k = int(entrada_k.get())  # Obtiene el valor de k.
        c = int(entrada_c.get())  # Obtiene el valor de c.
        g = int(entrada_g.get())  # Obtiene el valor de g.
        n = int(entrada_n.get())  # Obtiene el número de números a generar.
        min_val = float(entrada_min.get())  # Obtiene el valor mínimo.
        max_val = float(entrada_max.get())  # Obtiene el valor máximo.

        Xi, Ri, resultados = congruencial_lineal(seed, k, c, g, n, min_val, max_val)  # Genera los números.
        # Concatenar los resultados para mostrarlos en el mensaje
        resultados_mensaje = f"Números generados: {resultados}\nXi generados: {Xi}\nRi generados: {Ri}"
    
        # Muestra los resultados generados
        messagebox.showinfo("Resultados", resultados_mensaje)
        
        graficar_y_mostrar_resultados(resultados, "Resultados de Congruencial Lineal", "congruencial_lineal")  # Grafica los resultados.
        guardar_en_archivo(resultados, "congruencial_lineal")  # Guarda los resultados en un archivo.

    tk.Button(ventana_lineal, text="Generar", command=ejecutar_congruencial_lineal).grid(row=7, column=0, columnspan=2)

def crear_ventana_congruencial_multiplicativa():
    """Crea la interfaz para el método de congruencial multiplicativa."""
    ventana_multiplicativa = tk.Toplevel()  # Crea una nueva ventana.
    ventana_multiplicativa.title("Congruencial Multiplicativa")  # Establece el título de la ventana.

    # Crea las etiquetas y entradas para los parámetros
    tk.Label(ventana_multiplicativa, text="Semilla:").grid(row=0, column=0)
    entrada_seed = tk.Entry(ventana_multiplicativa)
    entrada_seed.grid(row=0, column=1)

    tk.Label(ventana_multiplicativa, text="t:").grid(row=1, column=0)
    entrada_t = tk.Entry(ventana_multiplicativa)
    entrada_t.grid(row=1, column=1)

    tk.Label(ventana_multiplicativa, text="g:").grid(row=2, column=0)
    entrada_g = tk.Entry(ventana_multiplicativa)
    entrada_g.grid(row=2, column=1)

    tk.Label(ventana_multiplicativa, text="Número de Números (n):").grid(row=3, column=0)
    entrada_n = tk.Entry(ventana_multiplicativa)
    entrada_n.grid(row=3, column=1)

    tk.Label(ventana_multiplicativa, text="Valor mínimo:").grid(row=4, column=0)
    entrada_min = tk.Entry(ventana_multiplicativa)
    entrada_min.grid(row=4, column=1)

    tk.Label(ventana_multiplicativa, text="Valor máximo:").grid(row=5, column=0)
    entrada_max = tk.Entry(ventana_multiplicativa)
    entrada_max.grid(row=5, column=1)

    def ejecutar_congruencial_multiplicativa():
        """Ejecuta la generación de números usando congruencial multiplicativa y muestra los resultados."""
        seed = int(entrada_seed.get())  # Obtiene la semilla ingresada.
        t = int(entrada_t.get())  # Obtiene el valor de t.
        g = int(entrada_g.get())  # Obtiene el valor de g.
        n = int(entrada_n.get())  # Obtiene el número de números a generar.
        min_val = float(entrada_min.get())  # Obtiene el valor mínimo.
        max_val = float(entrada_max.get())  # Obtiene el valor máximo.

        Xi, Ri, resultados = congruencial_multiplicativa(seed, t, g, n, min_val, max_val)  # Genera los números.

        # Concatenar los resultados para mostrarlos en el mensaje
        resultados_mensaje = f"Números generados: {resultados}\nXi generados: {Xi}\nRi generados: {Ri}"
    
        # Muestra los resultados generados
        messagebox.showinfo("Resultados", resultados_mensaje)

        graficar_y_mostrar_resultados(resultados, "Resultados de Congruencial Multiplicativa", "congruencial_multiplicativa")  # Grafica los resultados.
        guardar_en_archivo(resultados, "congruencial_multiplicativa")  # Guarda los resultados en un archivo.

    tk.Button(ventana_multiplicativa, text="Generar", command=ejecutar_congruencial_multiplicativa).grid(row=6, column=0, columnspan=2)

def crear_ventana_distribucion_uniforme():
    """Crea la interfaz para el método de distribución uniforme."""
    ventana_uniforme = tk.Toplevel()  # Crea una nueva ventana.
    ventana_uniforme.title("Distribución Uniforme")  # Establece el título de la ventana.

    # Crea las etiquetas y entradas para los parámetros
    tk.Label(ventana_uniforme, text="Número de Números (n):").grid(row=0, column=0)
    entrada_n = tk.Entry(ventana_uniforme)
    entrada_n.grid(row=0, column=1)

    tk.Label(ventana_uniforme, text="Valor mínimo:").grid(row=1, column=0)
    entrada_min = tk.Entry(ventana_uniforme)
    entrada_min.grid(row=1, column=1)

    tk.Label(ventana_uniforme, text="Valor máximo:").grid(row=2, column=0)
    entrada_max = tk.Entry(ventana_uniforme)
    entrada_max.grid(row=2, column=1)

    def ejecutar_distribucion_uniforme():
        """Ejecuta la generación de números usando distribución uniforme y muestra los resultados."""
        n = int(entrada_n.get())  # Obtiene el número de números a generar.
        min_val = float(entrada_min.get())  # Obtiene el valor mínimo.
        max_val = float(entrada_max.get())  # Obtiene el valor máximo.

        Ri, resultados = distribucion_uniforme(n, min_val, max_val)  # Genera los números.

        # Concatenar los resultados para mostrarlos en el mensaje
        resultados_mensaje = f"Números generados: {resultados}\n\nRi generados: {Ri}"
    
        # Muestra los resultados generados
        messagebox.showinfo("Resultados", resultados_mensaje)

        graficar_y_mostrar_resultados(resultados, "Resultados de Distribución Uniforme", "distribucion_uniforme")  # Grafica los resultados.
        guardar_en_archivo(resultados, "distribucion_uniforme")  # Guarda los resultados en un archivo.

    tk.Button(ventana_uniforme, text="Generar", command=ejecutar_distribucion_uniforme).grid(row=3, column=0, columnspan=2)

def crear_ventana_distribucion_normal_inversa():
    """Crea la interfaz para el método de distribución normal inversa."""
    ventana_normal_inversa = tk.Toplevel()  # Crea una nueva ventana.
    ventana_normal_inversa.title("Distribución Normal Inversa")  # Establece el título de la ventana.

    # Crea las etiquetas y entradas para los parámetros
    tk.Label(ventana_normal_inversa, text="Número de Números (n):").grid(row=0, column=0)
    entrada_n = tk.Entry(ventana_normal_inversa)
    entrada_n.grid(row=0, column=1)

    tk.Label(ventana_normal_inversa, text="Valor Minimo:").grid(row=1, column=0)
    entrada_promedio = tk.Entry(ventana_normal_inversa)
    entrada_promedio.grid(row=1, column=1)

    tk.Label(ventana_normal_inversa, text="Valor Maximo:").grid(row=2, column=0)
    entrada_desviacion = tk.Entry(ventana_normal_inversa)
    entrada_desviacion.grid(row=2, column=1)

    def ejecutar_distribucion_normal_inversa():
        """Ejecuta la generación de números usando distribución normal inversa y muestra los resultados."""
        n = int(entrada_n.get())  # Obtiene el número de números a generar.
        min = float(entrada_promedio.get())  # Obtiene el minimo.
        max = float(entrada_desviacion.get())  # Obtiene el maximo.

        semillas, Ri, resultados = distribucion_normal_inversa(n, min, max)  # Genera los números.

        # Concatenar los resultados para mostrarlos en el mensaje
        resultados_mensaje = f"Números generados: {resultados}\n\nRi generados: {Ri} \n Semillas generadas: {semillas}"
    
        # Muestra los resultados generados
        messagebox.showinfo("Resultados", resultados_mensaje)
        graficar_y_mostrar_resultados(resultados, "Resultados de Distribución Normal Inversa", "distribucion_normal_inversa")  # Grafica los resultados.
        guardar_en_archivo(resultados, "distribucion_normal_inversa")  # Guarda los resultados en un archivo.

    tk.Button(ventana_normal_inversa, text="Generar", command=ejecutar_distribucion_normal_inversa).grid(row=3, column=0, columnspan=2)

def crear_ventana_distribucion_estandar_normal_inversa():
    """Crea la interfaz para el método de distribución normal Estandar inversa."""
    ventana_normal_inversa = tk.Toplevel()  # Crea una nueva ventana.
    ventana_normal_inversa.title("Distribución Normal Estandar Inversa")  # Establece el título de la ventana.

    # Crea las etiquetas y entradas para los parámetros
    tk.Label(ventana_normal_inversa, text="Número de Números (n):").grid(row=0, column=0)
    entrada_n = tk.Entry(ventana_normal_inversa)
    entrada_n.grid(row=0, column=1)

    tk.Label(ventana_normal_inversa, text="Valor Min:").grid(row=1, column=0)
    entrada_promedio = tk.Entry(ventana_normal_inversa)
    entrada_promedio.grid(row=1, column=1)

    tk.Label(ventana_normal_inversa, text="Valor Max:").grid(row=2, column=0)
    entrada_desviacion = tk.Entry(ventana_normal_inversa)
    entrada_desviacion.grid(row=2, column=1)

    def ejecutar_distribucion_normal_Estandar_inversa():
        """Ejecuta la generación de números usando distribución normal inversa y muestra los resultados."""
        n = int(entrada_n.get())  # Obtiene el número de números a generar.

        Ri, resultados = distribucion_normal_estandar_inversa(n)  # Genera los números.
        # Concatenar los resultados para mostrarlos en el mensaje
        resultados_mensaje = f"Números generados: {resultados}\n\nRi generados: {Ri}"
    
        # Muestra los resultados generados
        messagebox.showinfo("Resultados", resultados_mensaje)
        graficar_y_mostrar_resultados(resultados, "Resultados de Distribución Normal Inversa", "distribucion_normal_inversa")  # Grafica los resultados.
        guardar_en_archivo(resultados, "distribucion_normal_estandar_inversa")  # Guarda los resultados en un archivo.

    tk.Button(ventana_normal_inversa, text="Generar", command=ejecutar_distribucion_normal_Estandar_inversa).grid(row=3, column=0, columnspan=2)


# Crear la ventana principal
ventana_principal = tk.Tk()  # Crea la ventana principal.
ventana_principal.title("Generadores de Números Pseudoaleatorios")  # Establece el título de la ventana.

# Crear los botones para abrir las diferentes ventanas
tk.Button(ventana_principal, text="Cuadrados Medios", command=crear_ventana_cuadrados_medios).pack(pady=10)
tk.Button(ventana_principal, text="Congruencial Lineal", command=crear_ventana_congruencial_lineal).pack(pady=10)
tk.Button(ventana_principal, text="Congruencial Multiplicativa", command=crear_ventana_congruencial_multiplicativa).pack(pady=10)
tk.Button(ventana_principal, text="Distribución Uniforme", command=crear_ventana_distribucion_uniforme).pack(pady=10)
tk.Button(ventana_principal, text="Distribución Normal Inversa", command=crear_ventana_distribucion_normal_inversa).pack(pady=10)
tk.Button(ventana_principal, text="Distribución Estandar Normal Inversa", command=crear_ventana_distribucion_estandar_normal_inversa).pack(pady=10)

ventana_principal.mainloop()  # Inicia el bucle principal de la ventana.
