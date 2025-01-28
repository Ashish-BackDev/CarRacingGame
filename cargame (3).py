import pygame
import random
import sys

# Initialize Pygame
pygame.init()

# Screen dimensions
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Car Racing Game")

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
YELLOW = (255, 255, 0)

# Clock and FPS
clock = pygame.time.Clock()
FPS = 60

# Load assets
restart_button = pygame.image.load("C:/Users/shiva/Downloads/restart.png")
quit_button = pygame.image.load("C:/Users/shiva/Downloads/exitsign.png")
coin_sound = pygame.mixer.Sound("C:/Users/shiva/Downloads/coin-recieved-230517 (online-audio-converter.com).wav")
collision_sound = pygame.mixer.Sound("C:/Users/shiva/Downloads/engine-47745 (online-audio-converter.com).wav")
engine_sound = pygame.mixer.Sound("C:/Users/shiva/Downloads/car-passing-281284.mp3")
car_width, car_height = 50, 100

car_image = pygame.image.load("C:/Users/shiva/Downloads/pngtree-back-view-of-yellow-car-png-image_10009564-removebg-preview.png")
car_image = pygame.transform.scale(car_image, (car_width, car_height))

enemy_car_image = pygame.image.load("C:/Users/shiva/Downloads/pngtree-blue-car-front-concept-view-illustration-vector-png-image_4552974-removebg-preview.png")
enemy_car_image = pygame.transform.scale(enemy_car_image, (car_width, car_height))

road_image = pygame.image.load("C:/Users/shiva/Downloads/background-1.png")
road_image = pygame.transform.scale(road_image, (WIDTH, HEIGHT))

coin_image = pygame.image.load("C:/Users/shiva/OneDrive/Desktop/coin480020.png")
coin_image = pygame.transform.scale(coin_image, (30, 30))

# Start engine sound
engine_sound.play(-1)

# Player variables
player_x = WIDTH // 2
player_y = HEIGHT - 120
player_speed = 8

# Enemy car variables
enemy_cars = []
enemy_speed = 8
for _ in range(3):
    enemy_cars.append([random.randint(150, WIDTH - 150), random.randint(-300, -100)])

# Coin variables
coins = []
coins_collected = 0

# Scrolling road
road_scroll_y = 0
road_scroll_speed = enemy_speed - 2

# Score
score = 0

# Fonts
font = pygame.font.Font(None, 36)

# Functions
def draw_background():
    global road_scroll_y
    road_scroll_y += road_scroll_speed
    if road_scroll_y >= HEIGHT:
        road_scroll_y = 0
    screen.blit(road_image, (0, road_scroll_y - HEIGHT))
    screen.blit(road_image, (0, road_scroll_y))

def draw_player(x, y):
    screen.blit(car_image, (x, y))

def draw_enemy_cars(cars):
    for car in cars:
        screen.blit(enemy_car_image, (car[0], car[1]))

def draw_coins():
    for coin in coins:
        screen.blit(coin_image, (coin[0] - 15, coin[1] - 15))

def check_collision(player_rect, cars):
    for car in cars:
        enemy_rect = pygame.Rect(car[0], car[1], car_width, car_height)
        if player_rect.colliderect(enemy_rect):
            return True
    return False

def check_coin_collision(player_rect):
    global coins_collected, coins
    for coin in coins[:]:
        coin_rect = pygame.Rect(coin[0] - 15, coin[1] - 15, 30, 30)
        if player_rect.colliderect(coin_rect):
            coins_collected += 1
            coins.remove(coin)
            coin_sound.play()

def game_over_screen():
    screen.fill(BLACK)
    text = font.render(f"Game Over! Score: {score}, Coins: {coins_collected}", True, WHITE)
    screen.blit(text, (WIDTH // 2 - text.get_width() // 2, HEIGHT // 2))

    # Display restart and quit buttons
    restart_rect = screen.blit(restart_button, (WIDTH // 2 - 100, HEIGHT // 2 + 50))
    quit_rect = screen.blit(quit_button, (WIDTH // 2 + 50, HEIGHT // 2 + 50))

    pygame.display.flip()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if restart_rect.collidepoint(event.pos):
                    return True
                if quit_rect.collidepoint(event.pos):
                    return False

# Main game loop
running = True
while True:
    while running:
        screen.fill(BLACK)
        draw_background()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        # Increase speed with score
        enemy_speed = 8 + (score // 10)
        road_scroll_speed = enemy_speed - 2

        # Player movement
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] and player_x > 100:
            player_x -= player_speed
        if keys[pygame.K_RIGHT] and player_x < WIDTH - car_width - 100:
            player_x += player_speed

        # Move enemy cars
        for car in enemy_cars:
            car[1] += enemy_speed
            if car[1] > HEIGHT:
                car[1] = random.randint(-300, -100)
                car[0] = random.randint(150, WIDTH - 150)
                score += 1

        # Check collisions
        player_rect = pygame.Rect(player_x, player_y, car_width, car_height)
        if check_collision(player_rect, enemy_cars):
            collision_sound.play()
            running = False

        # Check coin collisions
        check_coin_collision(player_rect)

        # Draw player and game elements
        draw_player(player_x, player_y)
        draw_enemy_cars(enemy_cars)
        draw_coins()

        # Display score and coins
        score_text = font.render(f"Score: {score}", True, WHITE)
        coins_text = font.render(f"Coins: {coins_collected}", True, YELLOW)
        screen.blit(score_text, (10, 10))
        screen.blit(coins_text, (10, 50))

        # Add coins randomly
        if random.randint(0, 100) < 2:
            coin_x = random.randint(150, WIDTH - 150)
            coin_y = random.randint(-500, -100)
            coins.append([coin_x, coin_y])

        # Move coins
        for coin in coins:
            coin[1] += enemy_speed
            if coin[1] > HEIGHT:
                coins.remove(coin)

        pygame.display.flip()
        clock.tick(FPS)

    if not running:
        engine_sound.stop()
        restart = game_over_screen()
        if restart:
            player_x, player_y = WIDTH // 2, HEIGHT - 120
            enemy_cars = []
            for _ in range(3):
                enemy_cars.append([random.randint(150, WIDTH - 150), random.randint(-300, -100)])
            coins = []
            score = 0
            coins_collected = 0
            running = True
            engine_sound.play(-1)
