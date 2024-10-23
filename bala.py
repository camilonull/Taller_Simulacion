import math

import pygame

bala_imagenes = [
    pygame.transform.scale(pygame.image.load("assets/bala/bala1.png"), (20, 20)),
    pygame.transform.scale(pygame.image.load("assets/bala/bala2.png"), (20, 20))
]

class Bala:
    def __init__(self, x, y, angulo):
        self.x = x
        self.y = y
        self.velocidad = 10
        self.angulo = angulo
        self.imagen_actual = 0

    def mover(self):
        # Calcular el movimiento basado en el ángulo
        self.x += self.velocidad * math.cos(math.radians(self.angulo))
        self.y -= self.velocidad * math.sin(math.radians(self.angulo))

    def dibujar(self, ventana):
        # Alternar la imagen de la bala para la animación
        ventana.blit(bala_imagenes[self.imagen_actual], (self.x, self.y))
        self.imagen_actual = (self.imagen_actual + 1) % 2  # Cambia entre bala1 y bala2
