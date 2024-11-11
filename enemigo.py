import pygame
import numpy as np

class Enemigo:
    def __init__(self, x, y):
        self.rect = pygame.Rect(x, y, 50, 50)  # Tamaño del enemigo
        self.imagen_normal = pygame.image.load("assets\enemigos\sapo.png")  # Imagen estándar
        self.imagen_salto = pygame.image.load("assets\enemigos\sapo_salto.png")  # Imagen de salto
        self.imagen_normal = pygame.transform.scale(self.imagen_normal, (50, 40))
        self.imagen_salto = pygame.transform.scale(self.imagen_salto, (50, 50))
        self.imagen_actual = self.imagen_normal  # Empieza con la imagen normal
        self.cambio = 0  # Contador para cambiar entre las imágenes

    def mover(self):
        num_aleatorio = np.random.uniform(0, 1)
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
        if self.cambio % 20 == 0:  # Cambia cada 10 movimientos (ajusta según desees)
            self.imagen_actual = self.imagen_salto if self.imagen_actual == self.imagen_normal else self.imagen_normal
    def dibujar(self, ventana):
         ventana.blit(self.imagen_actual, self.rect)  # Dibuja la imagen actual