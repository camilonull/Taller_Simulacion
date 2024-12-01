import random
import pygame
import numpy as np
from generadorNumeros import congruencial_lineal, verificacionRi

class Enemigo:
    def __init__(self, x, y, imagen_normal, imagen_salto, tipo_enemigo):
        self.rect = pygame.Rect(x, y, 50, 50)  # Tamaño del enemigo
        self.imagen_normal = pygame.image.load(imagen_normal)  # Imagen estándar
        self.imagen_salto = pygame.image.load(imagen_salto)  # Imagen de salto
        self.imagen_normal = pygame.transform.scale(self.imagen_normal, (60, 55))
        self.imagen_salto = pygame.transform.scale(self.imagen_salto, (60, 55))
        self.imagen_actual = self.imagen_normal  # Empieza con la imagen normal
        self.cambio = 0  # Contador para cambiar entre las imágenes
        self.tipo_enemigo = tipo_enemigo
        
        # Generar lista de números pseudoaleatorios con una semilla diferente
        numerosProbados = False
        AIT = []
        semillasMovEnemigo = [77,13,55,20,90,4434]
        while(numerosProbados == False):
            _, self.num_aleatorios = congruencial_lineal(random.choice(semillasMovEnemigo), 832262, 1013904223, 32, 200)
            numerosProbados = verificacionRi(self.num_aleatorios)
        #    print(self.num_aleatorios)
        #_, self.num_aleatorios = congruencial_lineal(semilla, 2, 1, 5, 100)
        self.indice_actual = 0  # Índice para iterar sobre la lista de num_aleatorios

    def mover(self):
        # Usar el valor actual de num_aleatorios y avanzar el índice
        num_aleatorio = self.num_aleatorios[self.indice_actual]
        self.indice_actual = (self.indice_actual + 1) % len(self.num_aleatorios)  # Reinicia el índice si llega al final

        # Movimientos posibles: izquierda, arriba, abajo con probabilidades
        movimientos_sapo = [(-5, 0), (0, -5), (0, 5)]
        probabilidades_sapo = [0.4, 0.4, 0.2]
        movimientos_ave = [(-5, 0), (0, -5), (0, 5)]
        probabilidades_ave = [0.6, 0.2, 0.2]


        if self.tipo_enemigo == "sapo":
            probabilidades = probabilidades_sapo
            movimientos = movimientos_sapo
        else:
            probabilidades = probabilidades_ave
            movimientos = movimientos_ave

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
