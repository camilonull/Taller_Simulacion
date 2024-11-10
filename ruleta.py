import pygame
import random

# Cargar imágenes de los power-ups (ajusta las rutas según tus assets)
powerups = {
    "curar": pygame.transform.scale(pygame.image.load("assets/powerups/salud.png"), (100, 100)),
    "escudo": pygame.transform.scale(pygame.image.load("assets/powerups/escudo.png"), (100, 100)),
    "municion": pygame.transform.scale(pygame.image.load("assets/powerups/bala.png"), (100, 100)),
}

# Variables internas de estado
_ruleta_mostrando = False
_powerup_seleccionado = None
_tiempo_inicio_ruleta = 0
_tiempo_mostrar_powerup = 0  # Nuevo tiempo para mostrar el power-up seleccionado
duracion_ruleta = 3000  # Duración de la ruleta en milisegundos (3 segundos)
duracion_powerup_ganador = 1000  # Duración del power-up ganador en ms (1 segundo)
escudo_activo = False

# Mostrar la ruleta
def mostrar_ruleta():
    global _ruleta_mostrando, _tiempo_inicio_ruleta
    _ruleta_mostrando = True
    _tiempo_inicio_ruleta = pygame.time.get_ticks()
    _powerup_seleccionado = None  # Resetear selección de power-up

# Aplicar el power-up seleccionado
def aplicar_powerup(powerup, vida_actual_casa, vida_maxima_casa, municion_actual):
    global escudo_activo
    if powerup == "curar":
        vida_actual_casa = min(vida_actual_casa + 300, vida_maxima_casa)  # Curar la casa
    elif powerup == "municion":
        municion_actual += 40
    return vida_actual_casa, municion_actual


# Nueva función de dibujar_ruleta actualizada
def dibujar_ruleta(ventana, vida_actual_casa, vida_maxima_casa, municion_actual):
    global _ruleta_mostrando
    # Seleccionar un power-up aleatoriamente
    powerup_seleccionado = random.choice(list(powerups.keys()))
    print(f"Power-up seleccionado: {powerup_seleccionado}")

    # Aplicar el power-up seleccionado
    vida_actual_casa, municion_actual = aplicar_powerup(powerup_seleccionado, vida_actual_casa, vida_maxima_casa, municion_actual)
    powerup_imagen = powerups[powerup_seleccionado]
    ventana.blit(powerup_imagen, (150, 150))
    # Retornar la vida actualizada y el power-up seleccionado
    _ruleta_mostrando = False
    return vida_actual_casa, powerup_seleccionado, municion_actual

# Función para comprobar si la ruleta está mostrándose
def ruleta_mostrando():
    return _ruleta_mostrando
