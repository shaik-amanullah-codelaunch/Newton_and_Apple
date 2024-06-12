import pygame
import random

# Initialize Pygame
pygame.init()

# Screen dimensions
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)

# Create the screen
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Newton and Apple")

# Clock for controlling the frame rate
clock = pygame.time.Clock()

# Load assets
newton_image = pygame.image.load("newton.png")
apple_image = pygame.image.load("apple.png")
background_image = pygame.image.load("background.jpg")

# Scale images if necessary
newton_image = pygame.transform.scale(newton_image, (60, 70))
apple_image = pygame.transform.scale(apple_image, (30, 30))
background_image = pygame.transform.scale(background_image, (SCREEN_WIDTH, SCREEN_HEIGHT))

# Define player class
class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = newton_image
        self.rect = self.image.get_rect()
        self.rect.x = SCREEN_WIDTH // 2
        self.rect.y = SCREEN_HEIGHT - self.rect.height - 10
        self.speed = 2 

    def update(self, keys_pressed):
        if keys_pressed[pygame.K_LEFT] and self.rect.left > 0:
            self.rect.x -= self.speed
        if keys_pressed[pygame.K_RIGHT] and self.rect.right < SCREEN_WIDTH:
            self.rect.x += self.speed
        if keys_pressed[pygame.K_UP] and self.rect.top > 0:
            self.rect.y -= self.speed
        if keys_pressed[pygame.K_DOWN] and self.rect.bottom < SCREEN_HEIGHT:
            self.rect.y += self.speed

# Define apple class
class Apple(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = apple_image
        self.rect = self.image.get_rect()
        self.rect.x = random.randint(0, SCREEN_WIDTH - self.rect.width)
        self.rect.y = random.randint(-100, -40)
        self.speed = random.randint(3, 6)

    def update(self):
        self.rect.y += self.speed
        if self.rect.top > SCREEN_HEIGHT:
            self.rect.x = random.randint(0, SCREEN_WIDTH - self.rect.width)
            self.rect.y = random.randint(-100, -40)
            self.speed = random.randint(3, 6)

# Create sprite groups
all_sprites = pygame.sprite.Group()
apples = pygame.sprite.Group()

# Create player object
player = Player()
all_sprites.add(player)

# Create apples
for _ in range(10):
    apple = Apple()
    all_sprites.add(apple)
    apples.add(apple)

# Game loop
running = True
game_over = False
font = pygame.font.Font(None, 36)
game_over_text = font.render("Newton discovered the 3 laws of physics! Game Over!", True, RED)

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    keys_pressed = pygame.key.get_pressed()
    if not game_over:
        player.update(keys_pressed)
        apples.update()

    # Check for collisions
    if pygame.sprite.spritecollideany(player, apples):
        game_over = True

    # Drawing
    screen.blit(background_image, (0, 0))
    all_sprites.draw(screen)
    if game_over:
        screen.blit(game_over_text, ((SCREEN_WIDTH - game_over_text.get_width()) // 2, SCREEN_HEIGHT // 2))
    pygame.display.flip()

    # Cap the frame rate
    clock.tick(60)

pygame.quit()
