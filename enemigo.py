import random
import pygame
import numpy as np
from generadorNumeros import congruencial_lineal, verificacionRi

class Enemigo:
    def __init__(self, x, y):
        self.rect = pygame.Rect(x, y, 50, 50)  # Tamaño del enemigo
        self.imagen_normal = pygame.image.load("assets\\enemigos\\sapo.png")  # Imagen estándar
        self.imagen_salto = pygame.image.load("assets\\enemigos\\sapo_salto.png")  # Imagen de salto
        self.imagen_normal = pygame.transform.scale(self.imagen_normal, (50, 40))
        self.imagen_salto = pygame.transform.scale(self.imagen_salto, (50, 50))
        self.imagen_actual = self.imagen_normal  # Empieza con la imagen normal
        self.cambio = 0  # Contador para cambiar entre las imágenes
        
        # Generar lista de números pseudoaleatorios con una semilla diferente
        numerosProbados = False
        AIT = []
        semillasMovEnemigo = [77,13,55,20,90,4434]
        while(numerosProbados == False):
            _, self.num_aleatorios = congruencial_lineal(random.choice(semillasMovEnemigo), 832262, 1013904223, 32, 100)
            numerosProbados = verificacionRi(self.num_aleatorios)
        #    print(self.num_aleatorios)
        #_, self.num_aleatorios = congruencial_lineal(semilla, 2, 1, 5, 100)
        self.indice_actual = 0  # Índice para iterar sobre la lista de num_aleatorios

    def mover(self):
        # Usar el valor actual de num_aleatorios y avanzar el índice
        num_aleatorio = self.num_aleatorios[self.indice_actual]
        self.indice_actual = (self.indice_actual + 1) % len(self.num_aleatorios)  # Reinicia el índice si llega al final

        # Movimientos posibles: izquierda, arriba, abajo con probabilidades
        movimientos = [(-5, 0), (0, -5), (0, 5)]
        probabilidades = [0.4, 0.4, 0.2]

        if num_aleatorio < probabilidades[0]:
            dx, dy = movimientos[0]
        elif num_aleatorio < sum(probabilidades[:2]):
            dx, dy = movimientos[1]
        else:
            dx, dy = movimientos[2]

        self.rect.move_ip(dx, dy)

        # Alterna la imagen en cada movimiento o cada cierto tiempo
        self.cambio += 1
        if self.cambio % 20 == 0:  # Cambia cada 20 movimientos (ajusta según desees)
            self.imagen_actual = self.imagen_salto if self.imagen_actual == self.imagen_normal else self.imagen_normal

    def dibujar(self, ventana):
        ventana.blit(self.imagen_actual, self.rect)  # Dibuja la imagen actual
