import pygame

# Inicializamos la fuente
pygame.font.init()
font = pygame.font.Font(None, 72)  # Cambia el tamaño según necesites

# Función para mostrar el mensaje con un contador de 3 segundos
def mostrar_mensaje_jefe(screen, texto, screen_width, screen_height):
    # Colores
    white = (255, 255, 255)
    
    # Tiempo de inicio del contador
    tiempo_inicio = pygame.time.get_ticks()
    tiempo_total = 4000  # 3 segundos en milisegundos
    
    # Bucle para el contador
    while True:
        
        
        # Calcular el tiempo restante
        tiempo_transcurrido = pygame.time.get_ticks() - tiempo_inicio
        tiempo_restante = max(0, (tiempo_total - tiempo_transcurrido) // 1000)  # Convertir a segundos
        
        # Renderizar texto
        texto_superficie = font.render(texto, True, white)
        tiempo_superficie = font.render(str(tiempo_restante), True, white)
        
        # Obtener posición centrada
        texto_rect = texto_superficie.get_rect(center=(screen_width // 2, screen_height // 2 - 50))
        tiempo_rect = tiempo_superficie.get_rect(center=(screen_width // 2, screen_height // 2 + 50))
        
        # Dibujar en la pantalla
        screen.blit(texto_superficie, texto_rect)
        #screen.blit(tiempo_superficie, tiempo_rect)
        
        pygame.display.flip()
        pygame.display.update()  # Actualizar la pantalla
        
        # Salir cuando el tiempo se acabe
        if tiempo_restante == 0:
            break
        
        # Controlar el frame rate
        pygame.time.Clock().tick(60)  # 30 FPS

# Usar esta función en tu programa principal, pasando el screen, texto, y las dimensiones de la pantalla.
