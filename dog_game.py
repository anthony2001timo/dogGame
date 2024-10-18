import pygame
import random
import time

# Inicializar Pygame
pygame.init()

# Configuración de la pantalla
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 400
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Perro Blanco Corredor y Destructor")

# Colores
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)

# Cargar el sprite del perro y el fondo
dog_img = pygame.image.load("dog.png")
dog_img = pygame.transform.scale(dog_img, (50, 50))
background_img = pygame.image.load("clouds.png")
background_img = pygame.transform.scale(background_img, (SCREEN_WIDTH, SCREEN_HEIGHT))

# Clase del Perro
class Dog:
    def __init__(self):
        self.image = dog_img
        self.x = 100
        self.y = SCREEN_HEIGHT - 100
        self.vel_y = 0
        self.jump = False
        self.lasers = []  # Almacena los láseres lanzados

    def move(self, keys):
        if keys[pygame.K_LEFT] and self.x > 0:
            self.x -= 5
        if keys[pygame.K_RIGHT] and self.x < SCREEN_WIDTH - 50:
            self.x += 5

    def update(self):
        if self.jump:
            self.vel_y = -10
            self.jump = False

        self.y += self.vel_y
        self.vel_y += 0.5

        if self.y > SCREEN_HEIGHT - 100:
            self.y = SCREEN_HEIGHT - 100
            self.vel_y = 0

    def draw(self):
        screen.blit(self.image, (self.x, self.y))

    def shoot_laser(self):
        laser = Laser(self.x + 50, self.y + 20)
        self.lasers.append(laser)

# Clase del Láser
class Laser:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.speed = 10

    def update(self):
        self.x += self.speed

    def draw(self):
        pygame.draw.rect(screen, RED, (self.x, self.y, 10, 5))

# Clase de Obstáculos
class Obstacle:
    def __init__(self, x):
        self.width = 40
        self.height = 40
        self.x = x
        self.y = SCREEN_HEIGHT - 100
        self.speed = random.randint(5, 8)

    def update(self):
        self.x -= self.speed
        if self.x < -self.width:
            self.x = SCREEN_WIDTH + random.randint(100, 300)

    def draw(self):
        pygame.draw.rect(screen, BLACK, (self.x, self.y, self.width, self.height))

# Función para mostrar mensajes en pantalla
def show_message(text):
    font = pygame.font.Font(None, 50)
    message = font.render(text, True, BLACK)
    screen.blit(message, (SCREEN_WIDTH // 2 - message.get_width() // 2, SCREEN_HEIGHT // 2 - message.get_height() // 2))
    pygame.display.update()
    time.sleep(2)

# Función principal del juego
def game_loop():
    clock = pygame.time.Clock()
    dog = Dog()

    obstacles = [Obstacle(SCREEN_WIDTH + i * 300) for i in range(3)]
    jumped_obstacles = 0  # Obstáculos saltados en el primer nivel
    destroyed_obstacles = 0  # Obstáculos destruidos en el segundo nivel

    level = 1  # Comienza en el nivel 1
    running = True

    while running:
        screen.blit(background_img, (0, 0))  # Dibujar fondo

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if level == 1:  # Nivel 1: saltar obstáculos
                    if event.key == pygame.K_SPACE and dog.y == SCREEN_HEIGHT - 100:
                        dog.jump = True
                elif level == 2:  # Nivel 2: disparar láser
                    if event.key == pygame.K_SPACE:
                        dog.shoot_laser()

        keys = pygame.key.get_pressed()
        dog.move(keys)

        # Nivel 1: Salto de obstáculos
        if level == 1:
            dog.update()
            for obstacle in obstacles:
                obstacle.update()
                obstacle.draw()

                # Verificar colisión en nivel 1
                if pygame.Rect(dog.x, dog.y, 50, 50).colliderect(
                    pygame.Rect(obstacle.x, obstacle.y, obstacle.width, obstacle.height)
                ):
                    print("¡Juego terminado!")
                    running = False

                # Contar obstáculos saltados
                if obstacle.x + obstacle.width < dog.x and not hasattr(obstacle, 'jumped'):
                    jumped_obstacles += 1
                    obstacle.jumped = True

            if jumped_obstacles >= 10:  # Cambiar al segundo nivel
                show_message("You Win! Next Level")
                level = 2  # Cambiar al nivel 2
                obstacles = [Obstacle(SCREEN_WIDTH + i * 200) for i in range(5)]  # Más obstáculos

        # Nivel 2: Disparar y destruir obstáculos
        elif level == 2:
            for laser in dog.lasers:
                laser.update()
                laser.draw()

                for obstacle in obstacles:
                    if pygame.Rect(laser.x, laser.y, 10, 5).colliderect(
                        pygame.Rect(obstacle.x, obstacle.y, obstacle.width, obstacle.height)
                    ):
                        destroyed_obstacles += 1
                        obstacles.remove(obstacle)
                        dog.lasers.remove(laser)
                        break

            if destroyed_obstacles >= 15:  # Completar el segundo nivel
                show_message("You completed the mission! Congratulations")
                running = False  # Terminar el juego

            for obstacle in obstacles:
                obstacle.update()
                obstacle.draw()

        dog.draw()

        pygame.display.update()
        clock.tick(30)  # 30 FPS

    pygame.quit()

# Ejecutar el juego
game_loop()
