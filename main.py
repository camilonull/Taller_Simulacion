import random
import pygame
import math
import numpy as np
from gameover import game_over
from pantalla_inicio import pantalla_inicio
from ruleta import mostrar_ruleta, dibujar_ruleta, ruleta_mostrando 
from bala import Bala
from enemigo import Enemigo
from generar_tiempos import generar_tiempos_entre_llegadas
from jefe_final import start_game
from mensaje import mostrar_mensaje_jefe
# Inicializar Pygame
pygame.init()

# Definir dimensiones de la ventad
ANCHO = 1200
ALTO = 700
ventana = pygame.display.set_mode((ANCHO, ALTO))
pygame.display.set_caption("Final Farm IX")

# Definir colores
BLANCO = (255, 255, 255)
VERDE = (11, 60, 10)
font_balas = pygame.font.Font(None, 36) 

#SIMULACION ENEMIGOS SAPOS
lambd_sapos = 1.5  # Tasa de llegada (lambda)
num_enemigos = 140  # Número de enemigos
AIT = generar_tiempos_entre_llegadas(num_enemigos, lambd_sapos)
AIT_ms_sapos = [int(a * 1000) for a in AIT]  # Convertir a milisegundos
print(AIT_ms_sapos)

# Crear lista de tiempos acumulados de aparición
tiempo_aparicion = [sum(AIT_ms_sapos[:i+1]) for i in range(len(AIT_ms_sapos))]

#SIMULACION ENEMIGOS AVES
lambd_aves = 1  # Tasa de llegada (lambda) para los enemigos de la esquina superior derecha
num_enemigos_2 = 100  # Número de enemigos para la segunda oleada
AIT_aves = generar_tiempos_entre_llegadas(num_enemigos_2, lambd_aves)
AIT_ms = [int(a * 1000) for a in AIT_aves]  # Convertir a milisegundos

# Crear lista de tiempos acumulados de aparición para la segunda oleada
tiempo_aparicion_2 = [sum(AIT_ms[:i + 1]) for i in range(len(AIT_ms))]

# Cargar imagenes enemigos 
sapo_normal = "assets\\enemigos\\sapo.png"
sapo_salto = "assets\\enemigos\\sapo_salto.png"
ave_normal = "assets\\enemigos\\ave.png"
ave_vuelo = "assets\\enemigos\\ave_vuelo.png"

# Cargar la imagen de fondo
fondo = pygame.image.load("assets/fondos/fondo_juego_1.png")

# Cargar las imágenes de los diferentes fondos
fondo_juego_1 = pygame.image.load("assets/fondos/fondo_juego_2.png")
fondo_juego_1 = pygame.transform.scale(fondo_juego_1, (ANCHO, ALTO))

fondo_juego_2 = pygame.image.load("assets/fondos/fondo_juego_3.png")
fondo_juego_2 = pygame.transform.scale(fondo_juego_2, (ANCHO, ALTO))

fondo_juego_3 = pygame.image.load("assets/fondos/fondo_juego_4.png")
fondo_juego_3 = pygame.transform.scale(fondo_juego_3, (ANCHO, ALTO))

#Escalar fondo a la pantalla
fondo = pygame.transform.scale(fondo, (ANCHO, ALTO)) 


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

imagen_cursor = pygame.image.load("assets/fondos/mira.png")
imagen_cursor = pygame.transform.scale(imagen_cursor, (35, 35))  # Escala si es necesario

# Ocultar el cursor predeterminado
pygame.mouse.set_visible(False)

# Cargar la imagen de la letra "E"
imagen_e = pygame.image.load("assets/botones/E.jpg")
imagen_e = pygame.transform.scale(imagen_e, (50, 50))  # Escalarla al tamaño que quieras


# Cargar las imágenes de la mata
imagenes_mata = [
    pygame.image.load("assets/fondos/mata_mari.png"),
    pygame.image.load("assets/fondos/mata_mari2.png"),
    pygame.image.load("assets/fondos/mata_mari3.png")
]



# Escalar las imágenes si es necesario
for i in range(len(imagenes_mata)):
    imagenes_mata[i] = pygame.transform.scale(imagenes_mata[i], (200, 200))  # Escalar al tamaño que necesites


# Escalar todas las imágenes a un tamaño adecuado (si es necesario)
for direccion in imagenes:
    for estado in imagenes[direccion]:
        imagenes[direccion][estado] = pygame.transform.scale(imagenes[direccion][estado], (50, 70))  # Ajustar el tamaño

sonido_click = pygame.mixer.Sound("assets/sonidos/pistol-shot.wav")

def mostrar_contador_balas(balas_restantes):
    texto_balas = font_balas.render(f"Balas: {balas_restantes}", True, VERDE)
    ventana.blit(texto_balas, (ventana.get_width() - 150, 20))  # Posición en la esquina superior derecha


def dibujar_barra_vida(ventana, x, y, vida_actual, vida_maxima, ancho_maximo,alto,con_escudo=False):
    # Si el escudo está activo, cambia los parámetros de vida y color de barra
    if con_escudo:
        color_barra = (10, 180, 100)# Color naranja para el escudo
    else:
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

    # Dibujar imagen de escudo si está activos
    if con_escudo:
        imagen_escudo = pygame.image.load("assets\powerups\escudo.png")  # Carga tu imagen de escudo
        imagen_escudo = pygame.transform.scale(imagen_escudo, (60, 60))  # Ajusta el tamaño del escudo
        ventana.blit(imagen_escudo, (x + ancho_maximo + 10, y-30))

    # Indicador de peligro (parpadeo cuando la vida es baja)
    if vida_actual < vida_maxima * 0.25:
        if pygame.time.get_ticks() % 1000 < 500:
            pygame.draw.rect(ventana, (255, 0, 0), (x, y, ancho_maximo, alto), 2)


def juego_principal():

    # Variables adicionales
    mostrar_mensaje = False
    tiempo_mensaje = 0
    duracion_mensaje = 2000  # Duración del mensaje en milisegundos (2 segundos)


    # Definir el número inicial de balas
    balas_restantes = 60

    # Parámetros de simulación
    
    enemigos = []  
    tiempo_inicial = pygame.time.get_ticks()

    enemigos_aves = []  # Lista para los enemigos de la segunda oleada
    tiempo_inicial_aves = pygame.time.get_ticks()  # Tiempo inicial para los enemigos de la segunda oleada


    personaje = pygame.Rect(ANCHO // 2, ALTO // 2, 50, 50)
    velocidad = 5
  
    estado_actual = "quieto"
    
    
    tiempo_ultima_interaccion = 0  # Tiempo de la última interacción
    contador_activo = True  # Estado del contador
    tiempo_restante = 3  # Contador inicial en segundos

    contador_pasos = 0
    # Lista para almacenar las balas disparadas
    balas = []

    vida_maxima_casa = 300  # Vida total máxima de la Casa
    vida_actual_casa = 300  # Vida inicial de la Casa
    ancho_barra_vida_casa = 500  # Ancho máximo de la barra de vida de la Casa
    
    con_escudo = False
    vida_maxima_escudo = 70
    vida_escudo = 70
    # Inicializar la fuente
    fuente = pygame.font.Font(None, 36)
    
     # Fondo inicial
    fondo_actual = fondo  # Mostrar fondo inicial
    
    # Reloj para controlar los FPS
    reloj = pygame.time.Clock()
    
    ancho_casa = 300
    alto_casa = 180
    x_casa = 0  # Centramos la Casa horizontalmente
    y_casa = 80 

    casa = pygame.Rect(x_casa, y_casa, ancho_casa, alto_casa) 
    
    
    ancho_restriccion = ANCHO  # La mitad del ancho de la ventana
    alto_restriccion = 170  # Altura del área restringida
    x_restriccion = (ANCHO - ancho_restriccion) // 2  # Calcular la posición X para centrar
    y_restriccion = 0  # En la parte superior

    # Crear el rectángulo del área restringida
    margen_superior = pygame.Rect(x_restriccion, y_restriccion, ancho_restriccion, alto_restriccion)
    
    
    tiempo_cambio_mata = pygame.time.get_ticks()
    indice_imagen_mata = 0

    # Posición de la mata
    x_mata = 5
    y_mata = 350
    # Bucle principal del juego
    ejecutando = True
    while ejecutando:

        
        # Establecer la cantidad de FPS
        reloj.tick(60)
        current_time = pygame.time.get_ticks()
            
        centro_personaje_x = personaje.x + personaje.width // 2
        centro_personaje_y = personaje.y + personaje.height // 2

        centro_mata_x = x_mata + imagenes_mata[indice_imagen_mata].get_width() // 2
        centro_mata_y = y_mata + imagenes_mata[indice_imagen_mata].get_height() // 2
        
        if contador_activo:
            # Calcular el tiempo restante
            tiempo_restante = 3 - (current_time - tiempo_ultima_interaccion) // 1000  # Convertir a segundos

            if tiempo_restante <= 0:
                contador_activo = False  # Desactivar el contador si ha llegado a 0
                tiempo_restante = 0  # Asegúrate de que no se muestre un valor negativo
                
        distancia_mata = math.sqrt((centro_personaje_x - centro_mata_x) ** 2 + (centro_personaje_y - centro_mata_y) ** 2)

        
        # Manejar eventos
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                ejecutando = False
            elif evento.type == pygame.MOUSEBUTTONDOWN:
                if evento.button == 1 and balas_restantes > 0:  # Clic izquierdo
                    sonido_click.play()
                    # Obtener la posición del mouse y calcular el ángulo de daisparo
                    pos_mouse = pygame.mouse.get_pos()
                    dx = pos_mouse[0] - (personaje.x + personaje.width // 2)
                    dy = pos_mouse[1] - (personaje.y + personaje.height // 2)
                    angulo_bala = math.degrees(math.atan2(-dy, dx))
                    balas_restantes -= 1
                    # Crear una nueva bala
                    nueva_bala = Bala(personaje.x + personaje.width // 2, personaje.y + personaje.height // 2, angulo_bala)
                    balas.append(nueva_bala)
                    #print(len(balas), "# de balas")
         # Tiempo actual
        tiempo_actual = pygame.time.get_ticks()

        spawnsEnemigos_sapos = [(1150, 550), (1000, 550), (900, 550),(800, 550),(1150, 450), (1000, 450), (900, 450),(800, 450),(1150, 650),(1150, 600),(1150, 620)]
        spawnsEnemigos_aves = [(1150, 150), (1150, 120), (1000, 100),(1000, 150),(800, 100), (800, 150)]


        # Generar enemigos según tiempos de aparición
        if tiempo_aparicion and tiempo_actual >= tiempo_aparicion[0]:
            spawn = random.choice(spawnsEnemigos_sapos)
            enemigo = Enemigo(spawn[0], spawn[1], sapo_normal, sapo_salto, "sapo")
            enemigos.append(enemigo)
            tiempo_aparicion.pop(0)
       
        # Manejo de la oleada de enemigos aves
        if tiempo_aparicion_2 and tiempo_actual >= tiempo_aparicion_2[0]:
            spawn = random.choice(spawnsEnemigos_aves)
            enemigo_ave = Enemigo(1150, 100, ave_normal, ave_vuelo, "ave")
            enemigos_aves.append(enemigo_ave)
            tiempo_aparicion_2.pop(0)

        
        # Obtener todas las teclas presionadas
        teclas = pygame.key.get_pressed()

        # Resetear estado a "quieto" si no se está moviendo
        movimiento = False

        # Movimiento del personaje usando WASD
        if teclas[pygame.K_a]:  # Mover a la izquierda (tecla 'A')
            personaje.x -= velocidad
            movimiento = True
        if teclas[pygame.K_d]:  # Mover a la derecha (tecla 'D')
            personaje.x += velocidad
            movimiento = True
        if teclas[pygame.K_w]:  # Mover hacia arriba (tecla 'W')
            personaje.y -= velocidad
            movimiento = True
        if teclas[pygame.K_s]:  # Mover hacia abajo (tecla 'S')
            personaje.y += velocidad
            movimiento = True

        if personaje.colliderect(margen_superior):
            # Empuja al personaje fuera del área restringida
            personaje.y = margen_superior.bottom
        
        # Actualizar la animación según el movimiento
        if movimiento:
            contador_pasos += 1
            if contador_pasos > 10:
                contador_pasos = 0
                # Alternar entre paso1 y paso2
                if estado_actual == "paso1":
                    estado_actual = "paso2"
                else:
                    estado_actual = "paso1"
        else:
            estado_actual = "quieto"

        # Limitar el movimiento del personaje a los bordes de la ventana
        if personaje.x < 0:
            personaje.x = 0
        if personaje.x > ANCHO - personaje.width:
            personaje.x = ANCHO - personaje.width
        if personaje.y < 0:
            personaje.y = 0
        if personaje.y > ALTO - personaje.height:
            personaje.y = ALTO - personaje.height

        
          # Actualizar el fondo según la vida de la Casa
        if vida_actual_casa > 100:  # Más del 50% de la vida
            fondo_actual = fondo
        elif 50 < vida_actual_casa <= 100:  # Entre 50% y 25%
            fondo_actual = fondo_juego_1
        elif 25 < vida_actual_casa <= 50:  # Entre 25% y 10%
            fondo_actual = fondo_juego_2
        elif vida_actual_casa <= 25:  # Menos del 10%
            fondo_actual = fondo_juego_3
      
        # Obtener la posición del mouse
        pos_mouse = pygame.mouse.get_pos()

        # Calcular el ángulo entre el personaje y el mouse
        dx = pos_mouse[0] - (personaje.x + personaje.width // 2)
        dy = pos_mouse[1] - (personaje.y + personaje.height // 2)
        angulo = math.degrees(math.atan2(-dy, dx))  # El ángulo entre el personaje y el mouse

        # Determinar la dirección del personaje basada en el ángulo
        if -45 <= angulo <= 45:
            direccion_actual = "derecha"
        elif 45 < angulo <= 135:
            direccion_actual = "atras"
        elif -135 <= angulo < -45:
            direccion_actual = "frente"
        else:
            direccion_actual = "izquierda"

        # Dibujar el fondo y el personaje
        ventana.blit(fondo_actual, (0, 0))
        if distancia_mata < 100:  # Si la distancia es menor a 100 píxeles
           ventana.blit(imagen_e, (centro_mata_x - imagen_e.get_width() // 2, centro_mata_y - 100))  # Mostrar la imagen 'E' sobre la mata


        
      
        # Manejar la entrada de la tecla 'E'
        if teclas[pygame.K_e] and distancia_mata < 100 and not ruleta_mostrando():
            # Verificar si han pasado 10 segundos desde la última interacción
            if tiempo_actual - tiempo_ultima_interaccion > 3000:  # 10000 ms = 10 segundos
                mostrar_ruleta()
                tiempo_ultima_interaccion = tiempo_actual  # Actualiza la última interacción
                contador_activo = True  # Activa el contador
        if ruleta_mostrando():
            vida_actual_casa, powerup_obtenido, municion_nueva = dibujar_ruleta(ventana, vida_actual_casa, vida_maxima_casa, balas_restantes)

            if powerup_obtenido:  # Si hay un power-up obtenido
                # Aquí puedes manejar el power-up, como activar la torreta
                if powerup_obtenido == "municion":
                    balas_restantes = municion_nueva
                elif powerup_obtenido == "escudo":
                    vida_escudo = vida_maxima_escudo
                    con_escudo = True
                 # Preparar para mostrar el mensaje
                mostrar_mensaje = True
                tiempo_mensaje = pygame.time.get_ticks()
                mensaje_texto = f"Power-up ganado: {powerup_obtenido}"
                x_mata = random.randint(5, 1000)
                y_mata = random.randint(150, 370)
        
        # Comprobar si debe mostrarse el mensaje
        if mostrar_mensaje:
            tiempo_actual = pygame.time.get_ticks()
            if tiempo_actual - tiempo_mensaje <= duracion_mensaje:
                fuente = pygame.font.Font(None, 50)
                texto = fuente.render(mensaje_texto, True, (255, 255, 255))
                texto_rect = texto.get_rect(center=(ventana.get_width() // 2, ventana.get_height() - 50))
                ventana.blit(texto, texto_rect)
            else:
                # Ocultar el mensaje después de 2 segundos
                mostrar_mensaje = False
              
        # Dibuja el contador en pantalla
        if contador_activo:
            fuente = pygame.font.SysFont(None, 48)  # Crea una fuente
            texto_contador = fuente.render(f"{tiempo_restante}s", True, (255, 255, 255))  # Texto en blanco
            ventana.blit(texto_contador, (x_mata + 90, y_mata + 180))  # Dibuja el contador en la esquina superior izquierda
        # Dibujar la barra de vida
        if con_escudo == False:
            dibujar_barra_vida(ventana, 40, 40, vida_actual_casa, vida_maxima_casa, ancho_barra_vida_casa, 20, con_escudo=False)
        else:
            dibujar_barra_vida(ventana, 40, 40, vida_escudo, vida_maxima_escudo, ancho_barra_vida_casa, 20, con_escudo=True)
       
        mostrar_contador_balas(balas_restantes)
        
        # Dibujar el texto "Casa" sobre la barra de vida
        texto = fuente.render("Casa Napoles", True, (255, 255, 255))  # El color del texto es blanco
        ventana.blit(texto, (40, 10)) 

        
        ventana.blit(imagenes[direccion_actual][estado_actual], personaje)
        
        #Dibujar collaider de la casa
        #pygame.draw.rect(ventana, (sa255, 0, 0), casa) 
        tiempo_actual = pygame.time.get_ticks()

        # Cambiar la imagen cada 1000 milisegundos (1 segundo)
        if tiempo_actual - tiempo_cambio_mata > 1000:
            indice_imagen_mata = (indice_imagen_mata + 1) % len(imagenes_mata)  # Alternar entre 0, 1 y 2
            tiempo_cambio_mata = tiempo_actual  # Reiniciar el tiempo

        # Dibujar la imagen actual de la mata en la pantalla
        ventana.blit(imagenes_mata[indice_imagen_mata], (x_mata, y_mata))
        #ventana.blit(escudo, (0, 70))
        
        for enemigo in enemigos[:]:
            enemigo.mover()
            enemigo.dibujar(ventana)
            
            # Detectar si el enemigo está fuera de la pantalla
            if (enemigo.rect.right < 0 or enemigo.rect.left > ANCHO or 
                enemigo.rect.bottom < 0 or enemigo.rect.top > ALTO):
                enemigos.remove(enemigo)  # Eliminar enemigo si está fuera de los límites
                continue  # Saltar el resto del bucle para este enemigo
            
            # Detectar colisiones con la casa u otros elementos, y remover si es necesario
            if enemigo.rect.colliderect(casa):
                if con_escudo == False: 
                    vida_actual_casa -= 10
                else:
                    vida_escudo -= 10# Reducir la vida de la casa al colisionar
                enemigos.remove(enemigo)
                if vida_escudo <= 0:
                    con_escudo = False
                if vida_actual_casa <= 0:
                   game_over(ventana, ANCHO, ALTO)
                   ejecutando = False
        
        for enemigo in enemigos_aves[:]:
            enemigo.mover()
            enemigo.dibujar(ventana)

              # Detectar si el enemigo está fuera de la pantalla
            if (enemigo.rect.right < 0 or enemigo.rect.left > ANCHO or 
                enemigo.rect.bottom < 0 or enemigo.rect.top > ALTO):
                enemigos_aves.remove(enemigo)  # Eliminar enemigo si está fuera de los límites
                continue  # Saltar el resto del bucle para este enemigo
            # Detectar colisiones con la casa u otros elementos, y remover si es necesario
            if enemigo.rect.colliderect(casa):
                if con_escudo == False: 
                    vida_actual_casa -= 10
                else:
                    vida_escudo -= 10# Reducir la vida de la casa al colisionar
                enemigos_aves.remove(enemigo)
                if vida_escudo <= 0:
                    con_escudo = False
                if vida_actual_casa <= 0:
                   game_over(ventana, ANCHO, ALTO)
                   ejecutando = False
              
        for bala in balas[:]:
            bala.mover()
            bala.dibujar(ventana)

            # Comprobar colisión con cada enemigo
            for enemigo in enemigos[:]:
                if bala.rect.colliderect(enemigo.rect):  # Detecta colisión
                    if bala in balas:
                        balas.remove(bala)  # Elimina la bala
                    enemigos.remove(enemigo)  # Elimina el enemigo
                    break  # Sale del bucle interno para evitar errores de modificación de lista
            
            for enemigo in enemigos_aves[:]:
                if bala.rect.colliderect(enemigo.rect):  # Detecta colisión
                    if bala in balas:
                        balas.remove(bala)  # Elimina la bala
                    enemigos_aves.remove(enemigo)  # Elimina el enemigo
                    break  # Sale del bucle interno para evitar errores de modificación de lista
            # Opcional: eliminar balas fuera dew la pantalsla
            if bala.x < 0 or bala.x > ANCHO or bala.y < 0 or bala.y > ALTO:
                if bala in balas:
                        balas.remove(bala)  # Elimina la bala

        ventana.blit(imagen_cursor, (pos_mouse[0] - imagen_cursor.get_width() // 2, pos_mouse[1] - imagen_cursor.get_height() // 2))
        
        if not enemigos and not enemigos_aves and not tiempo_aparicion and not tiempo_aparicion_2:      
            mostrar_mensaje_jefe(ventana, "!! Yendo al jefe final !!", ANCHO, ALTO)
            start_game()
            
            break  # Sal del bucle principal tras el combate
        # Actualizar la pantalla
        pygame.display.update()
        
    pygame.quit()

pantalla_inicio(ventana, ANCHO, ALTO)
# Cerrar Pygame
   
juego_principal()