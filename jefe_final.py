import random
import pygame
import math
import numpy as np

def combate_boss(personaje_vida, boss_vida, ventana):
    en_combate = True
    fuente_combate = pygame.font.Font(None, 36)
    
    while en_combate:
        ventana.fill(255, 255, 255)  # Limpia la pantalla
        texto_personaje = fuente_combate.render(f"Vida del personaje: {personaje_vida}", True, 255, 255, 255)
        texto_boss = fuente_combate.render(f"Vida del Boss: {boss_vida}", True, (255, 0, 0))
        
        ventana.blit(texto_personaje, (50, 50))
        ventana.blit(texto_boss, (50, 100))
        
        # Detecta eventos
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                exit()
            elif evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_a:  # Tecla para atacar
                    boss_vida -= random.randint(10, 20)
                elif evento.key == pygame.K_d:  # Tecla para defender
                    personaje_vida -= random.randint(5, 10) // 2
                else:
                    personaje_vida -= random.randint(10, 15)

        # Revisión de fin de combate
        if boss_vida <= 0:
            print("¡Victoria!")
            en_combate = False
        elif personaje_vida <= 0:
            print("Has sido derrotado.")
            en_combate = False
        
        pygame.display.flip()
        pygame.time.delay(500)
