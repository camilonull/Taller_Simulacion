import tkinter as tk
from tkinter import filedialog, messagebox
from matplotlib.pylab import chisquare
import numpy as np
import matplotlib.pyplot as plt
from scipy import stats
from scipy.stats import chi2  # Necesario para los valores de chi-cuadrado
from collections import Counter


# Función para cargar el archivo de números
def cargar_archivo():
    filepath = filedialog.askopenfilename(filetypes=[("Text files", "*.txt"), ("All files", "*.*")])
    if filepath:
        with open(filepath, 'r') as file:
            numeros = [float(line.strip()) for line in file.readlines()]
        return numeros
    else:
        messagebox.showwarning("Advertencia", "No se ha seleccionado un archivo.")
        return []
    
def normalizar_numeros(numeros_generados):
    """Normaliza la lista de números para que estén en el rango [0, 1]."""
    min_val = min(numeros_generados)
    max_val = max(numeros_generados)
    # Evitar división por cero
    if max_val - min_val == 0:
        return [0] * len(numeros_generados)  # Todos los números son iguales, devolver una lista de ceros
    return [(num - min_val) / (max_val - min_val) for num in numeros_generados]

# Pruebas de validación
def prueba_de_medias(numeros):
    n = len(numeros)
    media_observada = np.mean(numeros)
    z0 = 1.96  # Valor crítico para un nivel de confianza del 95%
    
    # Cálculo de los límites inferior y superior del intervalo de confianza
    LI = 0.5 - z0 * (1 / np.sqrt(12 * n))
    LS = 0.5 + z0 * (1 / np.sqrt(12 * n))
    
    cumple = LI <= media_observada <= LS  # Verificar si la media está dentro del intervalo
    
    # Mostrar los resultados en un mensaje
    resultado = f"Media Observada: {media_observada}\nIntervalo: [{LI}, {LS}]\nCumple: {cumple}"
    messagebox.showinfo("Prueba de Medias", resultado)
    return cumple

def prueba_de_varianza(numeros):
    n = len(numeros)
    varianza_observada = np.var(numeros, ddof=1)  # ddof=1 para muestra (VAR.S en Excel)
    
    alfa = 0.05
    chi_a2 = chi2.ppf(alfa / 2, n - 1)  # Valor crítico para alfa/2
    chi_1_a2 = chi2.ppf(1 - alfa / 2, n - 1)  # Valor crítico para 1 - alfa/2
    
    # Cálculo de los límites inferior y superior del intervalo de confianza
    LI = chi_a2 / (12 * (n - 1))
    LS = chi_1_a2 / (12 * (n - 1))
    
    cumple = LI <= varianza_observada <= LS  # Verificar si la varianza está dentro del intervalo
    
    # Mostrar los resultados en un mensaje
    resultado = f"Varianza Observada: {varianza_observada}\nIntervalo: [{LI}, {LS}]\nCumple: {cumple}"
    messagebox.showinfo("Prueba de Varianza", resultado)
    return cumple


# Función para calcular el número de intervalos usando la regla de Sturges
def calcular_numero_intervalos(n):
    return int(1 + 3.322 * np.log10(n))

#Prueba Ks
def prueba_ks(numeros_generados, n_intervalos):
    n_intervalos = calcular_numero_intervalos(len(numeros_generados))

    # Paso 1: Calcular los intervalos
    min_val = min(numeros_generados)
    max_val = max(numeros_generados)
    intervalos = np.linspace(min_val, max_val, n_intervalos + 1)

    # Paso 2: Calcular la frecuencia observada
    frecuencias_observadas, _ = np.histogram(numeros_generados, bins=intervalos)

    # Paso 3: Calcular la frecuencia esperada
    frecuencias_esperadas = [n / n_intervalos for n in range(1, n_intervalos + 1)]
    frecuencias_esperadas = np.array(frecuencias_esperadas) * len(numeros_generados) / n_intervalos

    # Paso 4: Calcular la frecuencia acumulada observada
    frecuencia_acumulada_observada = np.cumsum(frecuencias_observadas) / len(numeros_generados)

    # Paso 5: Calcular la frecuencia acumulada esperada
    frecuencia_acumulada_esperada = np.linspace(0, 1, n_intervalos + 1)[1:]

    # Paso 6: Calcular la diferencia entre las frecuencias acumuladas
    diferencias = np.abs(frecuencia_acumulada_observada - frecuencia_acumulada_esperada)

    # Paso 7: Determinar Dmax
    Dmax = np.max(diferencias)
    
    # Paso 8: Calcular el valor crítico Dcrit
    Dcrit = 0.05 / np.sqrt(len(numeros_generados))

    # Paso 9: Verificar si Dmax cumple con la prueba
    if Dmax < Dcrit:
        resultado_prueba = "La prueba de KS se cumple: no se rechaza la hipótesis nula."
    else:
        resultado_prueba = "La prueba de KS no se cumple: se rechaza la hipótesis nula."
    

    resultado = (
        f"Dmax: {Dmax:.4f}\n"
        f"Dcrit: {Dcrit:.4f}\n"
        f"Resultado: {resultado_prueba}\n\n"
        f"Diferencias: {', '.join(f'{d:.4f}' for d in diferencias)}\n"
        f"Frecuencias Observadas: {', '.join(str(f) for f in frecuencias_observadas)}\n"
        f"Frecuencias Esperadas: {', '.join(f'{fe:.4f}' for fe in frecuencias_esperadas)}"
    )
    # Mostrar el mensaje en un messagebox
    messagebox.showinfo("Prueba de KS", resultado)
    
    return Dmax, diferencias, frecuencias_observadas, frecuencias_esperadas

def prueba_chi_cuadrado(numeros_generados, num_intervals, alpha=0.05):
    """Realiza la prueba de Chi-cuadrado y retorna el valor calculado y el resultado de la prueba."""
    # Normalizar los números si es necesario
    numeros_generados = normalizar_numeros(numeros_generados)
    
    # Calcular la frecuencia observada
    intervalos = np.linspace(0, 1, num_intervals + 1)
    frecuencias_observadas, _ = np.histogram(numeros_generados, bins=intervalos)

    # Calcular la frecuencia esperada
    n = sum(frecuencias_observadas)
    frecuencia_esperada = n / num_intervals  # Asumiendo distribución uniforme

    # Calcular Chi-cuadrado
    chi_cuadrado = 0
    for fo in frecuencias_observadas:
        fe = frecuencia_esperada
        chi_cuadrado += (fo - fe) ** 2 / fe

    # Determinar si se pasa la prueba
    grados_de_libertad = num_intervals - 1
    # Calcular el valor crítico
    valor_critico = chi2.ppf(1 - alpha, grados_de_libertad)

    # Verificar si cumple con la prueba de Chi-Cuadrado
    if chi_cuadrado < valor_critico:
        resultado_prueba = "La prueba de Chi-Cuadrado se cumple: no se rechaza la hipótesis nula."
    else:
        resultado_prueba = "La prueba de Chi-Cuadrado no se cumple: se rechaza la hipótesis nula."
    
    # Crear el mensaje para mostrar
    resultado = (
        f"Chi-Cuadrado Calculado: {chi_cuadrado:.4f}\n"
        f"Valor Crítico: {valor_critico:.4f}\n"
        f"Grados de Libertad: {grados_de_libertad}\n"
        f"Resultado: {resultado_prueba}\n\n"
        f"Frecuencias Observadas: {', '.join(str(f) for f in frecuencias_observadas)}\n"
    )

    # Mostrar el mensaje en un messagebox
    messagebox.showinfo("Prueba de Chi2", resultado)

    return chi_cuadrado, frecuencias_observadas, resultado_prueba


def clasificar_numeros(numeros):
    """Clasifica los números según la prueba de Poker y cuenta la frecuencia de cada letra."""
    clasificaciones = []
    
    for numero in numeros:
        # Convertir el número a cadena, manteniendo un formato fijo (ej: 10 decimales)
        digitos = f"{numero:.5f}".split('.')[1]  # Mantener hasta 10 decimales
        print(digitos)
    
        # Contar la ocurrencia de cada dígito
        conteo = Counter(digitos)
        print(conteo)

        # Determinar la clasificación según los conteos
        valores = sorted(conteo.values(), reverse=True)  # Ordenar las frecuencias de ocurrencia

        if len(conteo) == 5:  # Todos diferentes
            clasificaciones.append('D')
        elif len(conteo) == 4:  # Un par
            clasificaciones.append('O')
        elif len(conteo) == 3:  # Dos pares o tercia
            if valores[0] == 2:
                clasificaciones.append('T')  # Dos pares
            else:
                clasificaciones.append('K')  # Tercia
        elif len(conteo) == 2:  # Full o Poker
            if valores[0] == 3:  # Full
                clasificaciones.append('F')
            else:  # Dos pares
                clasificaciones.append('P')
        elif len(conteo) == 1:  # Todas iguales
            clasificaciones.append('Q')

    # Contar la frecuencia de cada letra
    frecuencia = Counter(clasificaciones)
    print(frecuencia)
    return dict(frecuencia)  # Retorna un diccionario con la frecuencia de cada letra y frecuencias esperadas


def prueba_poker(numeros):
    # Probabilidades asociadas a cada letra
    probabilidades = {
        'D': 0.3024,  # Diferentes
        'O': 0.5040,  # Un par
        'T': 0.1080,  # Dos pares
        'K': 0.0720,  # Tercia
        'F': 0.0090,  # Full House
        'P': 0.0045,  # Póker
        'Q': 0.0001   # Quintilla
    }

    """Realiza la prueba de Poker para verificar la aleatoriedad de los números ingresados."""
    # Normalizar los números
    numeros_normalizados = normalizar_numeros(numeros)

    # Contar las frecuencias observadas de las clasificaciones
    frecuencias_observadas = clasificar_numeros(numeros_normalizados)
    
    # Inicializar chi-cuadrado
    chi_cuadrado = 0
    n = len(numeros_normalizados)
    frecuencias_esperadas = {}

    # Calcular chi-cuadrado y frecuencias esperadas
    for letra, frecuencia_observada in frecuencias_observadas.items():
        frecuencia_esperada = probabilidades[letra] * n
        frecuencias_esperadas[letra] = frecuencia_esperada
        chi_cuadrado += ((frecuencia_observada - frecuencia_esperada) ** 2) / frecuencia_esperada

    # Determinar el valor crítico de chi-cuadrado
    grados_de_libertad = len(probabilidades) - 1
    valor_critico = chi2.ppf(0.95, grados_de_libertad)

    # Verificar si cumple la prueba
    resultado = chi_cuadrado < valor_critico
    resultado_str = "Cumple la prueba de Poker." if resultado else "No cumple la prueba de Poker."

    # Crear el mensaje detallado para mostrar
    mensaje = (
        f"Chi-Cuadrado Calculado: {chi_cuadrado:.4f}\n"
        f"Valor Crítico: {valor_critico:.4f}\n"
        f"Grados de Libertad: {grados_de_libertad}\n"
        f"Resultado: {resultado_str}\n\n"
        f"Frecuencias Observadas:\n"
        + "\n".join(f"{letra}: {frecuencia}" for letra, frecuencia in frecuencias_observadas.items()) +
        "\n\nFrecuencias Esperadas:\n"
        + "\n".join(f"{letra}: {frecuencia_esperada:.4f}" for letra, frecuencia_esperada in frecuencias_esperadas.items())
    )

    print(len(frecuencias_observadas))

    # Mostrar el mensaje en un messagebox
    messagebox.showinfo("Prueba de Poker", mensaje)

    return chi_cuadrado, valor_critico, frecuencias_observadas, frecuencias_esperadas


# Crear la ventana principal
ventana = tk.Tk()
ventana.title("Validación de Números Pseudoaleatorios")

# Crear un marco para los botones
marco_botones = tk.Frame(ventana)
marco_botones.pack(pady=20)

# Botón para cargar archivo
boton_cargar = tk.Button(marco_botones, text="Cargar Números", command=lambda: cargar_archivo())
boton_cargar.pack(side=tk.LEFT, padx=10)

# Botón para realizar prueba de medias
boton_medias = tk.Button(marco_botones, text="Prueba de Medias", command=lambda: prueba_de_medias(cargar_archivo()))
boton_medias.pack(side=tk.LEFT, padx=10)

# Botón para realizar prueba de varianza
boton_varianza = tk.Button(marco_botones, text="Prueba de Varianza", command=lambda: prueba_de_varianza(cargar_archivo()))
boton_varianza.pack(side=tk.LEFT, padx=10)

# Botón para realizar prueba de Kolmogorov-Smirnov
boton_ks = tk.Button(marco_botones, text="Prueba KS", command=lambda: prueba_ks(cargar_archivo()))
boton_ks.pack(side=tk.LEFT, padx=10)

# Botón para realizar prueba de chi-cuadrado
boton_chi2 = tk.Button(marco_botones, text="Prueba Chi2", command=lambda: prueba_chi_cuadrado(cargar_archivo(), 10))
boton_chi2.pack(side=tk.LEFT, padx=10)

# Botón para realizar prueba de poker
boton_poker = tk.Button(marco_botones, text="Prueba Poker", command=lambda: prueba_poker(cargar_archivo()))
boton_poker.pack(side=tk.LEFT, padx=10)

# Ejecutar la aplicación
ventana.mainloop()
