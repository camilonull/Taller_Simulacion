import pygame

def win(ventana, ANCHO, ALTO):
    # Cargar la imagen de fondo de Game Over
    fondo = pygame.image.load("assets/fondos/win.jpg")
    fondo = pygame.transform.scale(fondo, (ANCHO, ALTO))

    # Inicializar la fuente para el texto
    pygame.font.init()
    fuente = pygame.font.Font(None, 40)  # Tamaño de fuente: 36
    fuente_win = pygame.font.Font(None, 65)  # Tamaño de fuente: 36
    texto = fuente.render("Presiona Enter para salir", True, (255, 255, 255))  # Texto en color blanco
    texto_win = fuente_win.render("GANASTE !!!", True, (255, 255, 255))  # Texto en color blanco

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
        ventana.blit(fondo, (0, 0))

        # Dibujar el texto en la parte inferior
        ventana.blit(texto, (ANCHO // 2 - texto.get_width() // 2, ALTO - 50))  # Centrar el texto horizontalmente

        ventana.blit(texto_win, (ANCHO // 2 - texto.get_width() // 2, 50))  # Centrar el texto horizontalmente y colocarlo arriba

        # Actualizar la pantalla
        pygame.display.update()

    pygame.quit()
