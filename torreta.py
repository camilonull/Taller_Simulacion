# torreta.py
import pygame

class Torreta:
    def __init__(self, x, y, imagen, duracion=10000):
        self.x = x
        self.y = y
        self.imagen = pygame.transform.scale(imagen, (100, 100))  # Ajustar el tamaño según sea necesario
        self.activada = False
        self.tiempo_activacion = 0
        self.duracion = duracion  # Duración en milisegundos

    def activar(self):
        self.activada = True
        self.tiempo_activacion = pygame.time.get_ticks()

    def dibujar(self, ventana):
        if self.activada:
            ventana.blit(self.imagen, (self.x, self.y))

    def actualizar(self):
        if self.activada and pygame.time.get_ticks() - self.tiempo_activacion >= self.duracion:
            self.activada = False  # Desactivar la torreta después de la duración

    def esta_activada(self):
        return self.activada
