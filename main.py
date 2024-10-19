import pygame
import math
from pantalla_inicio import pantalla_inicio
# Inicializar Pygame
pygame.init()

# Definir dimensiones de la ventana
ANCHO = 1200
ALTO = 700
ventana = pygame.display.set_mode((ANCHO, ALTO))
pygame.display.set_caption("Final Farm")

# Definir colores
BLANCO = (255, 255, 255)

pygame.mixer.music.load("assets/sonidos/fondo_musica.mp3")  # Reemplaza por la ruta a tu archivo de música
pygame.mixer.music.set_volume(0.2)  # Establecer el volumen de la música (0.0 a 1.0)
pygame.mixer.music.play(-1)

# Cargar la imagen de fondo
fondo = pygame.image.load("assets/fondos/fondo_juego.png")

# Cargar las imágenes de los diferentes fondos
fondo_juego_1 = pygame.image.load("assets/fondos/fondo_juego.png")
fondo_juego_1 = pygame.transform.scale(fondo_juego_1, (ANCHO, ALTO))

fondo_juego_2 = pygame.image.load("assets/fondos/fondo_juego_2.png")
fondo_juego_2 = pygame.transform.scale(fondo_juego_2, (ANCHO, ALTO))

fondo_juego_3 = pygame.image.load("assets/fondos/fondo_juego_3.png")
fondo_juego_3 = pygame.transform.scale(fondo_juego_3, (ANCHO, ALTO))

fondo_juego_4 = pygame.image.load("assets/fondos/fondo_juego_4.png")
fondo_juego_4 = pygame.transform.scale(fondo_juego_4, (ANCHO, ALTO))

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

# Cargar las imágenes de la bala y escalar
bala_imagenes = [
    pygame.transform.scale(pygame.image.load("assets/bala/bala1.png"), (20, 20)),
    pygame.transform.scale(pygame.image.load("assets/bala/bala2.png"), (20, 20))
]

# Escalar todas las imágenes a un tamaño adecuado (si es necesario)
for direccion in imagenes:
    for estado in imagenes[direccion]:
        imagenes[direccion][estado] = pygame.transform.scale(imagenes[direccion][estado], (50, 70))  # Ajustar el tamaño

sonido_click = pygame.mixer.Sound("assets/sonidos/pistol-shot.wav")

def dibujar_barra_vida(ventana, x, y, vida_actual, vida_maxima, ancho_maximo, alto):
    # Calcula el porcentaje de vida actual
    porcentaje_vida = vida_actual / vida_maxima
    # Calcular el ancho actual de la barra basado en el porcentaje de vida
    ancho_actual = int(ancho_maximo * porcentaje_vida)
    
    # Dibujar la barra de vida (color verde)
    pygame.draw.rect(ventana, (0, 255, 0), (x, y, ancho_actual, alto))
    # Dibujar el contorno de la barra de vida (color rojo)
    pygame.draw.rect(ventana, (255, 0, 0), (x, y, ancho_maximo, alto), 2)



def juego_principal():
# Configuración inicial del personaje
    personaje = pygame.Rect(ANCHO // 2, ALTO // 2, 50, 50)
    velocidad = 5
    direccion_actual = "frente"
    estado_actual = "quieto"

    contador_pasos = 0

    # Lista para almacenar las balas disparadas
    balas = []

    vida_maxima_casa = 200  # Vida total máxima de la Casa
    vida_actual_casa = 200  # Vida inicial de la Casa
    ancho_barra_vida_casa = 400  # Ancho máximo de la barra de vida de la Casa
    # Inicializar la fuente
    fuente = pygame.font.Font(None, 36)
    
    # Reloj para controlar los FPS
    reloj = pygame.time.Clock()
    
    ancho_casa = 470
    alto_casa = 210
    x_casa = (ANCHO - ancho_casa) // 2  # Centramos la Casa horizontalmente
    y_casa = 0 

    casa = pygame.Rect(x_casa, y_casa, ancho_casa, alto_casa) 
    
    
    ancho_restriccion = ANCHO  # La mitad del ancho de la ventana
    alto_restriccion = 170  # Altura del área restringida
    x_restriccion = (ANCHO - ancho_restriccion) // 2  # Calcular la posición X para centrar
    y_restriccion = 0  # En la parte superior

    # Crear el rectángulo del área restringida
    margen_superior = pygame.Rect(x_restriccion, y_restriccion, ancho_restriccion, alto_restriccion)

    # Bucle principal del juego
    ejecutando = True
    while ejecutando:
        # Establecer la cantidad de FPS
        reloj.tick(60)

        # Manejar eventos
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                ejecutando = False
            elif evento.type == pygame.MOUSEBUTTONDOWN:
                if evento.button == 1:  # Clic izquierdo
                    sonido_click.play()
                    # Obtener la posición del mouse y calcular el ángulo de disparo
                    pos_mouse = pygame.mouse.get_pos()
                    dx = pos_mouse[0] - (personaje.x + personaje.width // 2)
                    dy = pos_mouse[1] - (personaje.y + personaje.height // 2)
                    angulo_bala = math.degrees(math.atan2(-dy, dx))
                    # Crear una nueva bala
                    nueva_bala = Bala(personaje.x + personaje.width // 2, personaje.y + personaje.height // 2, angulo_bala)
                    balas.append(nueva_bala)

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
        if vida_actual_casa > 75:
            fondo = fondo_juego_1
        elif vida_actual_casa > 50:
            fondo = fondo_juego_2
        elif vida_actual_casa > 10:
            fondo = fondo_juego_3
        else:
            fondo = fondo_juego_4
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
        ventana.blit(fondo, (0, 0))
        
        
        # Dibujar la barra de vida
        dibujar_barra_vida(ventana, 40, 40, vida_actual_casa, vida_maxima_casa, ancho_barra_vida_casa, 20)
        
        
        # Dibujar el texto "Casa" sobre la barra de vida
        texto = fuente.render("Casa Napoles", True, (255, 255, 255))  # El color del texto es blanco
        ventana.blit(texto, (40, 10)) 

        
        ventana.blit(imagenes[direccion_actual][estado_actual], personaje)
        #pygame.draw.rect(ventana, (150, 30, 0), casa)  # Casa de color marrón
        for bala in balas[:]:
            bala.mover()
            bala.dibujar(ventana)
            # Detectar colisiones con la casa
            if casa.collidepoint(bala.x, bala.y):
                vida_actual_casa -= 10  # Reducir la vida de la Casa
                balas.remove(bala)  # Eliminar la bala tras el impacto
                if vida_actual_casa < 0:
                    vida_actual_casa = 0
        # Actualizar la pantalla
        pygame.display.update()
    pygame.quit()

pantalla_inicio(ventana, ANCHO, ALTO)
# Cerrar Pygame
juego_principal()

