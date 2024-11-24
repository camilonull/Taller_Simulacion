import pygame
import random
import math

# Inicializamos Pygame
pygame.init()

# Dimensiones de la pantalla
screen_width = 800
screen_height = 600
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Simulación de Combate con Agentes")

# Colores
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)

# FPS
clock = pygame.time.Clock()

# Personaje del jugador
player_size = 50
player_pos = [screen_width // 2, screen_height // 2]
player_speed = 5
player_health = 100

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

# Función para dibujar el escenario
def draw_game():
    screen.fill(WHITE)
    
    # Dibujar jugador
    pygame.draw.rect(screen, GREEN, (player_pos[0], player_pos[1], player_size, player_size))
    
    # Dibujar enemigos
    for enemy in enemies:
        if enemy["alive"]:
            pygame.draw.rect(screen, RED, (enemy["pos"][0], enemy["pos"][1], enemy_size, enemy_size))

    pygame.display.update()

# Función para mover al jugador
def move_player(keys):
    if keys[pygame.K_LEFT]:
        player_pos[0] -= player_speed
    if keys[pygame.K_RIGHT]:
        player_pos[0] += player_speed
    if keys[pygame.K_UP]:
        player_pos[1] -= player_speed
    if keys[pygame.K_DOWN]:
        player_pos[1] += player_speed

# Función para detectar colisiones entre el jugador y los enemigos
def check_collisions():
    global player_health
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

# Función para atacar al jugador cuerpo a cuerpo
def attack_enemy(enemy, dx, dy):
    angle = math.atan2(dy, dx)
    enemy["pos"][0] += enemy_speed * math.cos(angle)
    enemy["pos"][1] += enemy_speed * math.sin(angle)

# Función para disparar al jugador
def shoot_enemy(enemy, dx, dy):
    global player_health  # Declaramos que usamos la variable global player_health
    # Simulamos disparar un proyectil
    if random.random() < 0.1:  # Probabilidad de disparo
        print("¡Disparo realizado hacia el jugador!")
        player_health -= 5  # El jugador recibe daño por disparo
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
    clock.tick(30)  # Limitar el FPS

    # Manejo de eventos
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    
    # Obtener teclas presionadas
    keys = pygame.key.get_pressed()
    move_player(keys)

    # Verificar colisiones
    check_collisions()

    # Realizar simulación de agentes si hay enemigos vivos
    agent_simulation()

    # Dibujar el juego
    draw_game()

    # Mostrar la vida del jugador
    font = pygame.font.SysFont("Arial", 20)
    text = font.render(f"Salud del Jugador: {player_health}", True, BLACK)
    screen.blit(text, (10, 10))

pygame.quit()
