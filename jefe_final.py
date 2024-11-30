import pygame
import random
import math
from gameover import game_over

screen_width = 1200
screen_height = 700
# Cargar imágenes del personaje para cada dirección y estado
imagenes = {
    "frente": {
        "quieto": pygame.image.load("assets/player/frente/frente_quieto.png"),
        "paso1": pygame.image.load("assets/player/frente/frente_paso1.png"),
        "paso2": pygame.image.load("assets/player/frente/frente_paso2.png")
    },
    "atras": {
        "quieto": pygame.image.load("assets/player/atras/atras_quieto.png"),
        "paso1": pygame.image.load("assets/player/atras/atras_paso1.png"),
        "paso2": pygame.image.load("assets/player/atras/atras_paso2.png")
    },
    "izquierda": {
        "quieto": pygame.image.load("assets/player/izquierda/izquierda_quieto.png"),
        "paso1": pygame.image.load("assets/player/izquierda/izquierda_paso1.png"),
        "paso2": pygame.image.load("assets/player/izquierda/izquierda_paso2.png")
    },
    "derecha": {
        "quieto": pygame.image.load("assets/player/derecha/derecha_quieto.png"),
        "paso1": pygame.image.load("assets/player/derecha/derecha_paso1.png"),
        "paso2": pygame.image.load("assets/player/derecha/derecha_paso2.png")
    }
}
# Cargar la imagen de fondo
fondo = pygame.image.load("assets/fondos/fondo_juego_jefe.png")
#Escalar fondo a la pantalla
fondo = pygame.transform.scale(fondo, (screen_width, screen_height)) 
imagen_cursor = pygame.image.load("assets/fondos/mira.png")
imagen_cursor = pygame.transform.scale(imagen_cursor, (35, 35))  # Escala si es necesario
rata = pygame.image.load("assets/enemigos/rata.png")
rata_salto = pygame.image.load("assets/enemigos/rata_salto.png")
rata = pygame.transform.scale(rata, (80, 40))
rata_salto = pygame.transform.scale(rata_salto, (80, 40))



# Escalar todas las imágenes a un tamaño adecuado (si es necesario)
for direccion in imagenes:
    for estado in imagenes[direccion]:
        imagenes[direccion][estado] = pygame.transform.scale(imagenes[direccion][estado], (50, 70))  # Ajustar el tamaño

def dibujar_barra_vida(ventana, x, y, vida_actual, vida_maxima, ancho_maximo,alto):
    # Inicializar la fuente
    fuente = pygame.font.Font(None, 36)
     # Dibujar el texto "Casa" sobre la barra de vida
    texto = fuente.render("Cloud", True, (255, 255, 255))  # El color del texto es blanco
    ventana.blit(texto, (40, 10)) 
  
    color_barra = (255, 165, 0)# Verde para la vida regular

    # Calcular el porcentaje de vida actual y el ancho de la barra
    porcentaje_vida = vida_actual / vida_maxima
    ancho_actual = int(ancho_maximo * porcentaje_vida)

    # Dibujar la barra de fondo (gris)
    pygame.draw.rect(ventana, (128, 128, 128), (x, y, ancho_maximo, alto))

    # Crear una superficie para la barra de vida con un gradiente
    superficie_barra = pygame.Surface((ancho_actual, alto))
    for i in range(ancho_actual):
        verde = int(color_barra[1] * (1 - i / ancho_actual))
        rojo = int(color_barra[0] * (i / ancho_actual))
        superficie_barra.fill((verde, rojo, 0), rect=pygame.Rect(i, 0, 1, alto))

    # Dibujar la barra de vida con el gradiente
    ventana.blit(superficie_barra, (x, y))

    # Dibujar el contorno de la barra de vida (negro)
    pygame.draw.rect(ventana, (0, 0, 0), (x, y, ancho_maximo, alto), 2)

    # Mostrar el valor numérico de la vida
    font = pygame.font.Font(None, 24)
    texto_vida = font.render(str(vida_actual), True, (255, 255, 255))
    ventana.blit(texto_vida, (x + ancho_maximo // 2 - texto_vida.get_width() // 2, y - 20))

    # Indicador de peligro (parpadeo cuando la vida es baja)
    if vida_actual < vida_maxima * 0.25:
        if pygame.time.get_ticks() % 1000 < 500:
            pygame.draw.rect(ventana, (255, 0, 0), (x, y, ancho_maximo, alto), 2)


def start_game():
    # Inicialización de Pygame
    pygame.init()
    # Ocultar el cursor predeterminado
    #pygame.mouse.set_visible(False)
    # Dimensiones de la pantalla
    
    screen = pygame.display.set_mode((screen_width, screen_height))
    pygame.display.set_caption("Simulación de Combate con Agentes")

    # FPS
    clock = pygame.time.Clock()

    # Personaje del jugador
    player_size = 50
    player_pos = pygame.Rect(screen_width // 2, screen_height // 2, player_size, player_size)
    player_speed = 5
    player_health = 100
    player_health_max = 100
    direccion_actual = "frente"  # Dirección inicial
    estado_actual = "quieto"     # Estado inicial del jugador
    contador_animacion = 0       # Contador para alternar las imágenes


    # Enemigos
    enemy_size = 30
    enemy_speed = 3
    enemy_health = 50
    enemies = []

    # Función para crear enemigos
    def create_enemy():
        x = random.randint(0, screen_width - enemy_size)
        y = random.randint(0, screen_height - enemy_size)
        return {"pos": [x, y], "alive": True, "health": enemy_health, "gun_range": 150}

    # Crear algunos enemigos
    for _ in range(5):
        enemies.append(create_enemy())
     # Función para animar al personaje
     
     # Función para calcular la dirección en base al mouse
    def actualizar_direccion():
        nonlocal direccion_actual
        # Coordenadas del mouse
        mouse_x, mouse_y = pygame.mouse.get_pos()

        # Calcular la diferencia entre el jugador y el mouse
        dx = mouse_x - player_pos[0]
        dy = mouse_y - player_pos[1]

        # Calcular el ángulo
        angle = math.atan2(dy, dx)
        angle_deg = math.degrees(angle)

        # Determinar la dirección según el ángulo
        if -45 <= angle_deg <= 45:
            direccion_actual = "derecha"
        elif 45 < angle_deg <= 135:
            direccion_actual = "frente"
        elif -135 <= angle_deg < -45:
            direccion_actual = "atras"
        else:
            direccion_actual = "izquierda"
    # Función para animar al personaje basado en el mouse
    def animar_personaje_mouse(keys):
        nonlocal estado_actual, contador_animacion

        if keys[pygame.K_a] or keys[pygame.K_d] or keys[pygame.K_w] or keys[pygame.K_s]:  # Verificar si alguna tecla de movimiento está presionada
            contador_animacion += 1
            if contador_animacion >= 10:  # Cambiar cada 10 fotogramas
                contador_animacion = 0
                if estado_actual == "paso1":
                    estado_actual = "paso2"
                else:
                    estado_actual = "paso1"
        else:
            estado_actual = "quieto"  # Si no hay movimiento, el personaje está quieto
    # Función para dibujar al jugador
    def draw_player():
        imagen_actual = imagenes[direccion_actual][estado_actual]
        screen.blit(imagen_actual, (player_pos[0], player_pos[1]))

    def game_over_verify():
        if player_health < 0:
            game_over(screen, screen_width, screen_height)
            running = False
    # Función para dibujar el escenario
    def draw_game():
        
        # Dibujar el fondo primero
        screen.blit(fondo, (0, 0))
        #dibujar vida del personaje
        dibujar_barra_vida(screen,10,40,player_health,player_health_max,500,20)
        mouse_x, mouse_y = pygame.mouse.get_pos()
        screen.blit(imagen_cursor, (mouse_x - imagen_cursor.get_width() // 2, mouse_y - imagen_cursor.get_height() // 2))
       # Dibujar jugador
        draw_player()
        
        # Dibujar enemigos
        for enemy in enemies:
            if enemy["alive"]:
                
                # Obtener la imagen actual de la rata
                imagen_rata = enemy.get("frame", rata)

                # Rotar la imagen si es necesario
                if player_pos.x < enemy["pos"][0]:  # Si el jugador está a la izquierda del enemigo
                    imagen_rata = pygame.transform.flip(imagen_rata, True, False)  # Voltear horizontalmente
                    
                screen.blit(imagen_rata, enemy["pos"]) 
                #pygame.draw.rect(screen, RED, (enemy["pos"][0], enemy["pos"][1], enemy_size, enemy_size))


        ancho_restriccion = screen_width  # La mitad del ancho de la ventana
        alto_restriccion = 170  # Altura del área restringida
        x_restriccion = (screen_width - ancho_restriccion) // 2  # Calcular la posición X para centrar
        y_restriccion = 0  # En la parte superior

        # Crear el rectángulo del área restringida
        margen_superior = pygame.Rect(x_restriccion, y_restriccion, ancho_restriccion, alto_restriccion)
        
        if player_pos.colliderect(margen_superior):
            # Empuja al personaje fuera del área restringida
            player_pos.y = margen_superior.bottom
        pygame.display.update()

    # Función para mover al jugador con teclas AWSD
    def move_player(keys):
        if keys[pygame.K_a]:  # Tecla 'A' para moverse a la izquierda
            player_pos[0] -= player_speed
        if keys[pygame.K_d]:  # Tecla 'D' para moverse a la derecha
            player_pos[0] += player_speed
        if keys[pygame.K_w]:  # Tecla 'W' para moverse hacia arriba
            player_pos[1] -= player_speed
        if keys[pygame.K_s]:  # Tecla 'S' para moverse hacia abajo
            player_pos[1] += player_speed
        # Animar el personaje basado en el movimiento del mouse
        
        # Mantener al jugador dentro de la pantalla
        if player_pos.left < 0:
            player_pos.left = 0
        elif player_pos.right > screen_width:
            player_pos.right = screen_width
        if player_pos.top < 0:
            player_pos.top = 0
        elif player_pos.bottom > screen_height:
            player_pos.bottom = screen_height
        animar_personaje_mouse(keys)


    # Función para detectar colisiones entre el jugador y los enemigos
    def check_collisions():
        nonlocal player_health
        for enemy in enemies:
            if enemy["alive"]:
                ex, ey = enemy["pos"]
                if (player_pos[0] < ex + enemy_size and player_pos[0] + player_size > ex and
                    player_pos[1] < ey + enemy_size and player_pos[1] + player_size > ey):
                    enemy["alive"] = False
                    player_health -= 10  # El jugador recibe daño cuando colisiona

    # Función de simulación de agentes (mueve a los enemigos)
    def agent_simulation():
        for enemy in enemies:
            if enemy["alive"]:
                ex, ey = enemy["pos"]
                dx = player_pos[0] - ex
                dy = player_pos[1] - ey
                distance = math.sqrt(dx**2 + dy**2)
                
                # Decisiones basadas en la distancia al jugador
                if distance < 50:  # Muy cerca, el enemigo intenta atacar
                    attack_enemy(enemy, dx, dy)
                elif distance < enemy["gun_range"]:  # Dentro del rango de disparo
                    shoot_enemy(enemy, dx, dy)
                else:  # Si está lejos, se mueve hacia el jugador
                    move_towards_player(enemy, dx, dy)
                
                # Alternar entre imágenes de rata (con contador)
                enemy["frame_count"] = enemy.get("frame_count", 0) + 1  # Incrementar el contador
                if enemy["frame_count"] >= 30:  # Cambiar cada 30 frames (ajusta este valor)
                    enemy["frame_count"] = 0  # Reiniciar el contador
                    if enemy.get("frame", rata) == rata:
                        enemy["frame"] = rata_salto
                    else:
                        enemy["frame"] = rata

    # Función para atacar al jugador cuerpo a cuerpo
    def attack_enemy(enemy, dx, dy):
        angle = math.atan2(dy, dx)
        enemy["pos"][0] += enemy_speed * math.cos(angle)
        enemy["pos"][1] += enemy_speed * math.sin(angle)

    # Función para disparar al jugador
    def shoot_enemy(enemy, dx, dy):
        nonlocal player_health
        # Simulamos disparar un proyectil
        print(random.random())
        if random.random() < 0.1:  # Probabilidad de disparo
            print("¡Disparo realizado hacia el jugador!")
            player_health -= 5  # El jugador recibe daño por disparo
            
            #verificar el game_over
            game_over_verify()
        # El enemigo puede moverse de vuelta después de disparar
        angle = math.atan2(dy, dx)
        enemy["pos"][0] -= enemy_speed * math.cos(angle)
        enemy["pos"][1] -= enemy_speed * math.sin(angle)

    # Función para mover al enemigo hacia el jugador
    def move_towards_player(enemy, dx, dy):
        angle = math.atan2(dy, dx)
        enemy["pos"][0] += enemy_speed * math.cos(angle)
        enemy["pos"][1] += enemy_speed * math.sin(angle)

    # Bucle principal del juego
    running = True
    while running:
        clock.tick(60)  # Limitar el FPS

        # Manejo de eventos
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        
        # Obtener teclas presionadas
        keys = pygame.key.get_pressed()
        # Animar el personaje
        
        move_player(keys)
        # Actualizar la dirección según el mouse
        actualizar_direccion()

        
        # Verificar colisiones
        check_collisions()

        # Realizar simulación de agentes si hay enemigos vivos
        agent_simulation()

        # Dibujar el juego
        draw_game()
        
        

    pygame.quit()
