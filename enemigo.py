import pygame

class Enemigo:
    def __init__(self, x, y, velocidad):
        self.rect = pygame.Rect(x, y, 50, 50)  # Tamaño del enemigo
        self.velocidad = velocidad

    def mover(self):
        self.rect.x -= self.velocidad  # Mover en línea recta hacia la derecha

    def dibujar(self, ventana):
        pygame.draw.rect(ventana, (255, 0, 0), self.rect)  # Dibujar el enemigo (rectángulo rojo)
