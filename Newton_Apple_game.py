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
background_image = pygame.image.load("b3.jpg").convert()
start_background_image = pygame.image.load("start_background.jpeg").convert()
start_button_image = pygame.image.load("start.png").convert_alpha()
quit_button_image = pygame.image.load("quit_button.png").convert_alpha()

# Scale images if necessary
newton_image = pygame.transform.scale(newton_image, (140, 160))
apple_image = pygame.transform.scale(apple_image, (50, 50))
coconut_image = pygame.transform.scale(coconut_image, (130, 90))
background_image = pygame.transform.scale(background_image, (SCREEN_WIDTH, SCREEN_HEIGHT))
start_background_image = pygame.transform.scale(start_background_image, (SCREEN_WIDTH, SCREEN_HEIGHT))
start_button_image = pygame.transform.scale(start_button_image, (400, 300))
quit_button_image = pygame.transform.smoothscale(quit_button_image, (100, 80))

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
        self.reset_position()
        self.speed = random.randint(1, 3)  # Decreased speed range

    def update(self):
        self.rect.y += self.speed
        if self.rect.top > SCREEN_HEIGHT:
            self.reset_position()

    def reset_position(self):
        self.rect.x = random.randint(0, SCREEN_WIDTH - self.rect.width)
        self.rect.y = random.randint(-100, -40)

# Define coconut class
class Coconut(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = coconut_image
        self.rect = self.image.get_rect()
        self.mask = coconut_mask
        self.reset_position()
        self.speed = random.randint(2, 4)  # Decreased speed range

    def update(self):
        self.rect.y += self.speed
        if self.rect.top > SCREEN_HEIGHT:
            self.reset_position()

    def reset_position(self):
        self.rect.x = random.randint(0, SCREEN_WIDTH - self.rect.width)
        self.rect.y = random.randint(-100, -40)

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
game_started = False
font = pygame.font.Font(None, 76)
small_font = pygame.font.Font(None, 36)

# Helper function to draw buttons
def draw_button(image, x, y):
    rect = image.get_rect()
    rect.topleft = (x, y)
    screen.blit(image, rect)
    return rect


while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.MOUSEBUTTONDOWN:
            mouse_x, mouse_y = event.pos
            if not game_started:
                if start_button_rect.collidepoint(mouse_x, mouse_y):
                    game_started = True
                elif quit_button_rect.collidepoint(mouse_x, mouse_y):
                    running = False
            else:
                if quit_button_rect.collidepoint(mouse_x, mouse_y):
                    running = False
                if game_over and replay_button_rect.collidepoint(mouse_x, mouse_y):
                    reset_game()

    if not game_started:
        screen.blit(start_background_image, (0, 0))
        start_button_rect = draw_button(start_button_image, (SCREEN_WIDTH - start_button_image.get_width()) // 2, (SCREEN_HEIGHT - start_button_image.get_height()) // 2)
        quit_button_rect = draw_button(quit_button_image, (SCREEN_WIDTH - quit_button_image.get_width()) // 2, (SCREEN_HEIGHT - quit_button_image.get_height()) // 2 + 120)
    else:
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
                    laws_image = pygame.image.load("newton_laws.jpg").convert_alpha()
                    laws_image = pygame.transform.smoothscale(laws_image, (800, 600))
                    screen.blit(laws_image, ((SCREEN_WIDTH - laws_image.get_width()) // 2, (SCREEN_HEIGHT - laws_image.get_height()) // 2))      
                    pygame.display.flip()  # Update the display to show the image
                    pygame.time.wait(20000)  # Wait for 3000 milliseconds (3 seconds)
                    game_over = True

        # Check for collisions with coconuts
        for coconut in coconuts:
            if pygame.sprite.collide_mask(player, coconut):
                player.health -= 25
                coconut.kill()
                if player.health <= 0:
                    laws_image = pygame.image.load("loose.png").convert_alpha()
                    laws_image = pygame.transform.smoothscale(laws_image, (700, 600))
                    screen.blit(laws_image, ((SCREEN_WIDTH - laws_image.get_width()) // 2, (SCREEN_HEIGHT - laws_image.get_height()) // 2))      
                    pygame.display.flip()  # Update the display to show the image
                    pygame.time.wait(20000)  # Wait for 3000 milliseconds (3 seconds)
                    game_over = True
        # Drawing
        screen.blit(background_image, (0, 0))
        all_sprites.draw(screen)

        # Draw health bar
        pygame.draw.rect(screen, RED, (10, 10, player.health * 2, 25))  # Health bar

        # Display apple hits
        apple_hit_text = font.render(f"Apple Hits: {player.apple_hits}", True, WHITE)
        screen.blit(apple_hit_text, (10, 40))

        # Draw quit button
        quit_button_rect = draw_button(quit_button_image, SCREEN_WIDTH - quit_button_image.get_width() - 20, 20)

        if game_over:
            screen.blit(game_over_text, ((SCREEN_WIDTH - game_over_text.get_width()) // 2, SCREEN_HEIGHT // 2))
            replay_button_rect = draw_button(replay_button_image, SCREEN_WIDTH - quit_button_image.get_width() - 80, 20)
    pygame.display.flip()

    # Cap the frame rate
    clock.tick(60)

pygame.quit()
