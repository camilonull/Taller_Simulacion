import pygame

def game_over(ventana, ANCHO, ALTO):
    # Cargar la imagen de fondo de Game Over
    fondo_game_over = pygame.image.load("assets/fondos/game_over.jpg")
    fondo_game_over = pygame.transform.scale(fondo_game_over, (ANCHO, ALTO))

    # Bucle principal de la pantalla de Game Over
    ejecutando = True
    while ejecutando:
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                ejecutando = False
            if evento.type == pygame.KEYDOWN:  # Detectar si se presiona una tecla
                if evento.key == pygame.K_RETURN:  # Verificar si la tecla es Enter
                    ejecutando = False  # Salir del bucle

        # Dibujar el fondo
        ventana.blit(fondo_game_over, (0, 0))

        # Actualizar la pantalla
        pygame.display.update()

    pygame.quit()