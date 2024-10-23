import pygame
import random

# Cargar imágenes de los power-ups (ajusta las rutas según tus assets)
powerups = {
    "curar": pygame.transform.scale(pygame.image.load("assets/powerups/salud.png"), (100, 100)),
    "escudo": pygame.transform.scale(pygame.image.load("assets/powerups/escudo.png"), (100, 100)),
    "torreta": pygame.transform.scale(pygame.image.load("assets/powerups/torreta.png"), (100, 100))
}

# Variables internas de estado
_ruleta_mostrando = False
_powerup_seleccionado = None
_ruleta_angulo = 0
_tiempo_inicio_ruleta = 0
_tiempo_fin_ruleta = 0  # Tiempo para mostrar el ganador
duracion_ruleta = 3000  # Duración de la ruleta en milisegundos (3 segundos)
duracion_powerup_ganador = 1500  # Duración del power-up ganador en ms (1 segundo)
escudo_activo = False
_indice_powerup_actual = 0  # Índice para iterar sobre los power-ups

# Mostrar la ruleta
def mostrar_ruleta():
    global _ruleta_mostrando, _tiempo_inicio_ruleta
    _ruleta_mostrando = True
    _tiempo_inicio_ruleta = pygame.time.get_ticks()
    _powerup_seleccionado = None  # Resetear selección de power-up

# Aplicar el power-up seleccionado
def aplicar_powerup(powerup, vida_actual_casa, vida_maxima_casa):
    global escudo_activo
    if powerup == "curar":
        vida_actual_casa = min(vida_actual_casa + 300, vida_maxima_casa)  # Curar la casa
    elif powerup == "escudo":
        escudo_activo = True  # Activar el escudo
    return vida_actual_casa


# Nueva función de dibujar_ruleta actualizada
def dibujar_ruleta(ventana, fondo_actual, ANCHO, ALTO, vida_actual_casa, vida_maxima_casa):
    global _powerup_seleccionado, _ruleta_angulo, _ruleta_mostrando, duracion_ruleta, _indice_powerup_actual, _tiempo_fin_ruleta, _tiempo_inicio_ruleta

    # Redibujar el fondo
    ventana.blit(fondo_actual, (0, 0))

    tiempo_actual = pygame.time.get_ticks()
    card_image = pygame.image.load("assets/card/card.png")
    # Escalar la imagen de la carta (hacerla más pequeña)
    escala_card = (150, 200)  # Cambiar tamaño a 100x150 píxeles (puedes ajustar según prefieras)
    card_image_escalada = pygame.transform.scale(card_image, escala_card)

    # Mostrar la carta (card.png) durante los primeros 2 segundos
    if _ruleta_mostrando and _powerup_seleccionado is None:
        if tiempo_actual - _tiempo_inicio_ruleta < duracion_ruleta:
            # Obtener el rectángulo de la carta para centrarla
             
            card_rect = card_image_escalada.get_rect(center=(ANCHO // 2, ALTO // 2))  # Centrar la carta
            ventana.blit(card_image_escalada, card_rect)
        else:
            # Después de 2 segundos, seleccionar aleatoriamente el power-up
            _powerup_seleccionado = random.choice(list(powerups.keys()))
            
            # Guardar el tiempo de selección del power-up
            _tiempo_fin_ruleta = pygame.time.get_ticks()  # Guardar el tiempo actual
            print(f"Power-up ganador: {_powerup_seleccionado}")

    # Mostrar la imagen del power-up ganador por 1 segundo
    if _powerup_seleccionado:
        powerup_ganador = powerups[_powerup_seleccionado]
        ruleta_rect = powerup_ganador.get_rect(center=(ANCHO // 2, ALTO // 2))  # Centrar el power-up
        ventana.blit(powerup_ganador, ruleta_rect)

        # Verificar si ha pasado 1 segundo desde que se seleccionó el ganador
        if tiempo_actual - _tiempo_fin_ruleta > duracion_powerup_ganador:
            _ruleta_mostrando = False  # Ocultar la ruleta
            vida_actual_casa = aplicar_powerup(_powerup_seleccionado, vida_actual_casa, vida_maxima_casa)
            _powerup_seleccionado = None  # Resetear para la próxima vez

    return vida_actual_casa, _powerup_seleccionado

# Función para comprobar si la ruleta está mostrándose
def ruleta_mostrando():
    return _ruleta_mostrando
