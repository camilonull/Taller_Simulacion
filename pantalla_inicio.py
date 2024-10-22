import pygame

# Dimensiones de la ventana
ANCHO = 1200
ALTO = 700

# Cargar imagen de fondo
fondo = pygame.image.load("assets/fondos/pantalla_principal1.jpg")
fondo = pygame.transform.scale(fondo, (ANCHO, ALTO))  # Escalar fondo a la pantalla

# Cargar imágenes del botón play1 y play2
boton_play1 = pygame.image.load("assets/botones/play1.png")  # Imagen normal
boton_play2 = pygame.image.load("assets/botones/play2.png")  # Imagen al pasar el mouse
boton_play1 = pygame.transform.scale(boton_play1, (200, 200))  # Ajustar tamaño del botón
boton_play2 = pygame.transform.scale(boton_play2, (200, 200)) 
# Ajustar tamaño del botón

boton_musica_pause = pygame.image.load("assets/botones/play_music.png")
boton_musica_play = pygame.image.load("assets/botones/pause_music.png")

boton_musica_play = pygame.transform.scale(boton_musica_play, (50, 50))
boton_musica_pause = pygame.transform.scale(boton_musica_pause, (50, 50))

x_boton_musica = ANCHO - 60  # En la esquina superior derecha
y_boton_musica = 10



imagenes_frente = [
    pygame.image.load("assets/player/frente/frente_quieto.png"),
    pygame.image.load("assets/player/frente/frente_paso1.png"),
    pygame.image.load("assets/player/frente/frente_paso2.png")
]

for i in range(len(imagenes_frente)):
    imagenes_frente[i] = pygame.transform.scale(imagenes_frente[i], (50, 70))  # Ajustar el tamaño del personaje

# Posición del personaje en la esquina inferior derecha
pos_x_personaje = ANCHO - 60  # Ajustar para posicionar el personaje en la esquina derecha
pos_y_personaje = ALTO - 80 

musica_reproduciendo = True

imagen_cursor = pygame.image.load("assets/fondos/mira.png")
imagen_cursor = pygame.transform.scale(imagen_cursor, (35, 35))  # Escala si es necesario

# Función para dibujar y manejar el botón de música
def dibujar_boton_musica(ventana):
    global musica_reproduciendo
    
    mouse = pygame.mouse.get_pos()  # Obtener posición del mouse
    click = pygame.mouse.get_pressed()  # Obtener si se hizo clic
    
    # Verificar si el mouse está sobre el botón de música
    if x_boton_musica + boton_musica_play.get_width() > mouse[0] > x_boton_musica and y_boton_musica + boton_musica_play.get_height() > mouse[1] > y_boton_musica:
        if click[0] == 1:  # Si se hace clic en el botón
            if musica_reproduciendo:
                pygame.mixer.music.pause()
                musica_reproduciendo = False
            else:
                pygame.mixer.music.unpause()
                musica_reproduciendo = True
    
    # Dibujar el botón de música correspondiente (play o pause)
    if musica_reproduciendo:
        ventana.blit(boton_musica_pause, (x_boton_musica, y_boton_musica))  # Mostrar el botón de pausa
    else:
        ventana.blit(boton_musica_play, (x_boton_musica, y_boton_musica)) 

def mostrar_personaje_animado(ventana, contador_pasos):
    # Alternar entre las 3 imágenes de frente según el contador de pasos
    imagen_personaje = imagenes_frente[contador_pasos // 40 % 3]
  # Cambiar de imagen cada 10 frames
    ventana.blit(imagen_personaje, (pos_x_personaje, pos_y_personaje))

# Función para dibujar el botón con imagen que cambia al pasar el mouse
def dibujar_boton_cambiable(ventana, x, y):
    mouse = pygame.mouse.get_pos()  # Obtener posición del mouse
    click = pygame.mouse.get_pressed()  # Obtener si se hizo clic
    
    # Verificar si el mouse está sobre el botón
    if x + boton_play1.get_width() > mouse[0] > x and y + boton_play1.get_height() > mouse[1] > y:
        ventana.blit(boton_play2, (x, y))  # Dibujar el botón con la imagen "hover"
        pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_HAND)  # Cambiar el cursor a mano
        if click[0] == 1:  # Si se hace clic en el botón
            return True
    else:
        ventana.blit(boton_play1, (x, y))  # Dibujar el botón con la imagen normal
        pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_ARROW)  # Cambiar el cursor al normal
    return False

# Pantalla de inicio
def pantalla_inicio(ventana, ANCHO, ALTO):
    # Inicializar la fuente
    pygame.mixer.music.load("assets/sonidos/fondo_musica.mp3")
    pygame.mixer.music.set_volume(0.2)
    pygame.mixer.music.play(-1)  # Reproducir en bucle
    contador_pasos = 0
    iniciar = True
    while iniciar:
        ventana.blit(fondo, (0, 0))
      
        pos_mouse = pygame.mouse.get_pos()
        # Dibujar botón que cambia de imagen al pasar el mouse
        if dibujar_boton_cambiable(ventana, ANCHO // 2 - boton_play1.get_width() // 2, ALTO // 1.5):
            iniciar = False  # Salir de la pantalla de inicio e iniciar el juego

        mostrar_personaje_animado(ventana, contador_pasos)

        # Aumentar el contador para cambiar la animación
        contador_pasos += 1
        if contador_pasos >= 360:  # Reiniciar después de recorrer las 3 imágenes
            contador_pasos = 0
        
        dibujar_boton_musica(ventana)
        ventana.blit(imagen_cursor, (pos_mouse[0] - imagen_cursor.get_width() // 2, pos_mouse[1] - imagen_cursor.get_height() // 2))
        # Actualizar la pantalla
        pygame.display.update()

        # Manejar eventos
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                quit()
