import pygame
import numpy as np

class Enemigo:
    def __init__(self, x, y, velocidad):
        self.rect = pygame.Rect(x, y, 50, 50)  # Tamaño del enemigo
        self.velocidad = velocidad

    def mover(self):
        num_aleatorio = np.random.uniform(0, 1)
        # Movimientos posibles: izquierda, arriba, abajo con probabilidades
        movimientos = [(-2, 0), (0, -2), (0, 2)]
        probabilidades = [0.4, 0.4, 0.2]

        if num_aleatorio < probabilidades[0]:
            dx, dy = movimientos[0]
        elif num_aleatorio < sum(probabilidades[:2]):
            dx, dy = movimientos[1]
        else:
            dx, dy = movimientos[2]

        self.rect.move_ip(dx, dy)

    def dibujar(self, ventana):
        pygame.draw.rect(ventana, (255, 0, 0), self.rect)