import pygame
import random

# Initialize Pygame
pygame.init()

# Screen dimensions
SCREEN_WIDTH = 1060
SCREEN_HEIGHT = 780

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)

# Create the screen
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Newton and Apple")

# Clock for controlling the frame rate
clock = pygame.time.Clock()

# Load assets
newton_image = pygame.image.load("newton.png").convert_alpha()
apple_image = pygame.image.load("apple.png").convert_alpha()
coconut_image = pygame.image.load("coconut.png").convert_alpha()
background_image = pygame.image.load("background.jpg").convert()

# Scale images if necessary
newton_image = pygame.transform.scale(newton_image, (90, 90))
apple_image = pygame.transform.scale(apple_image, (50, 50))
coconut_image = pygame.transform.scale(coconut_image, (120, 90))
background_image = pygame.transform.scale(background_image, (SCREEN_WIDTH, SCREEN_HEIGHT))

# Generate masks
newton_mask = pygame.mask.from_surface(newton_image)
apple_mask = pygame.mask.from_surface(apple_image)
coconut_mask = pygame.mask.from_surface(coconut_image)

# Define player class
class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = newton_image
        self.rect = self.image.get_rect()
        self.rect.x = SCREEN_WIDTH // 2
        self.rect.y = SCREEN_HEIGHT - self.rect.height - 10
        self.mask = newton_mask
        self.speed = 5
        self.health = 100
        self.apple_hits = 0

    def update(self, keys_pressed):
        if keys_pressed[pygame.K_LEFT] and self.rect.left > 0:
            self.rect.x -= self.speed
        if keys_pressed[pygame.K_RIGHT] and self.rect.right < SCREEN_WIDTH:
            self.rect.x += self.speed

# Define apple class
class Apple(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = apple_image
        self.rect = self.image.get_rect()
        self.mask = apple_mask
        self.rect.x = random.randint(0, SCREEN_WIDTH - self.rect.width)
        self.rect.y = random.randint(-100, -40)
        self.speed = random.randint(1, 3)  # Decreased speed range

    def update(self):
        self.rect.y += self.speed
        if self.rect.top > SCREEN_HEIGHT:
            self.rect.x = random.randint(0, SCREEN_WIDTH - self.rect.width)
            self.rect.y = random.randint(-100, -40)
            self.speed = random.randint(1, 3)  # Decreased speed range

# Define coconut class
class Coconut(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = coconut_image
        self.rect = self.image.get_rect()
        self.mask = coconut_mask
        self.rect.x = random.randint(0, SCREEN_WIDTH - self.rect.width)
        self.rect.y = random.randint(-100, -40)
        self.speed = random.randint(2, 4)  # Decreased speed range

    def update(self):
        self.rect.y += self.speed
        if self.rect.top > SCREEN_HEIGHT:
            self.rect.x = random.randint(0, SCREEN_WIDTH - self.rect.width)
            self.rect.y = random.randint(-100, -40)
            self.speed = random.randint(2, 4)  # Decreased speed range

# Create sprite groups
all_sprites = pygame.sprite.Group()
apples = pygame.sprite.Group()
coconuts = pygame.sprite.Group()

# Create player object
player = Player()
all_sprites.add(player)

# Create apples (less frequent)
for _ in range(1):  # Reduced number of apples
    apple = Apple()
    all_sprites.add(apple)
    apples.add(apple)

# Create coconuts (more frequent)
for _ in range(3):  # Increased number of coconuts
    coconut = Coconut()
    all_sprites.add(coconut)
    coconuts.add(coconut)


# Ensure no overlap at spawn time
def avoid_overlap(sprite, group):
    for other in group:
        if pygame.sprite.collide_rect(sprite, other):
            return False
    return True

# Ensure apples and coconuts don't overlap when spawning
for apple in apples:
    while not avoid_overlap(apple, coconuts):
        apple.reset_position()


for coconut in coconuts:
    while not avoid_overlap(coconut, apples):
        coconut.reset_position()

# Game loop
running = True
game_over = False
font = pygame.font.Font(None, 76)

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    keys_pressed = pygame.key.get_pressed()
    if not game_over:
        player.update(keys_pressed)

        # Update apples and coconuts
        apples.update()
        coconuts.update()

        # Check if the number of apples or coconuts is too high
        if len(apples) < 5:  # Limit apples to 5 on screen
            apple = Apple()
            if avoid_overlap(apple, coconuts):  # Ensure no initial overlap
                all_sprites.add(apple)
                apples.add(apple)

        if len(coconuts) < 7:  # Limit coconuts to 7 on screen
            coconut = Coconut()
            if avoid_overlap(coconut, apples):  # Ensure no initial overlap
                all_sprites.add(coconut)
                coconuts.add(coconut)

    # Check for collisions with apples
    for apple in apples:
        if pygame.sprite.collide_mask(player, apple):
            player.apple_hits += 1
            apple.kill()
            if player.apple_hits >= 3:
                game_over = True
                game_over_text = font.render("Newton discovered gravity! Game Over!", True, GREEN)

    # Check for collisions with coconuts
    for coconut in coconuts:
        if pygame.sprite.collide_mask(player, coconut):
            player.health -= 25
            coconut.kill()
            if player.health <= 0:
                game_over = True
                game_over_text = font.render("Newton's mind is broken! Discover the laws yourself!", True, RED)

    # Drawing
    screen.blit(background_image, (0, 0))
    all_sprites.draw(screen)

    # Draw health bar
    pygame.draw.rect(screen, RED, (10, 10, player.health * 2, 30))  # Health bar

    # Display apple hits
    apple_hit_text = font.render(f"Apple Hits: {player.apple_hits}", True, BLACK)
    screen.blit(apple_hit_text, (10, 40))

    if game_over:
        screen.blit(game_over_text, ((SCREEN_WIDTH - game_over_text.get_width()) // 2, SCREEN_HEIGHT // 2))

    pygame.display.flip()

    # Cap the frame rate
    clock.tick(60)

pygame.quit()
