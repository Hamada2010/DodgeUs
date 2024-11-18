# Importing required libraries
import pygame
import random
import sys

# Initialize Pygame
pygame.init()

# Screen dimensions
SCREEN_WIDTH = 600
SCREEN_HEIGHT = 400

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)

# Player settings
PLAYER_WIDTH = 50
PLAYER_HEIGHT = 10

# Falling object settings
OBJECT_WIDTH = 20
OBJECT_HEIGHT = 20
OBJECT_SPEED = 4
OBJECT_INCREASE = 0.1

# Setup screen and clock
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Dodge the Falling Objects")
clock = pygame.time.Clock()

# Player class
class Player:
    def __init__(self):
        self.x = SCREEN_WIDTH // 2
        self.y = SCREEN_HEIGHT - 50
        self.width = PLAYER_WIDTH
        self.height = PLAYER_HEIGHT
        self.color = BLUE

    def draw(self):
        pygame.draw.rect(screen, self.color, (self.x, self.y, self.width, self.height))

    def move(self):
        # Get the current mouse position
        mouse_x = pygame.mouse.get_pos()[0]
        # Center the block around the mouse position and ensure it stays within bounds
        self.x = max(0, min(mouse_x - self.width // 2, SCREEN_WIDTH - self.width))

# FallingObject class
class FallingObject:
    def __init__(self):
        self.x = random.randint(0, SCREEN_WIDTH - OBJECT_WIDTH)
        self.y = -OBJECT_HEIGHT
        self.width = OBJECT_WIDTH
        self.height = OBJECT_HEIGHT
        self.speed = OBJECT_SPEED
        self.color = RED

    def draw(self):
        pygame.draw.rect(screen, self.color, (self.x, self.y, self.width, self.height))

    def move(self):
        self.y += self.speed

# Game over screen
def game_over_screen(score):
    screen.fill(WHITE)
    font = pygame.font.SysFont(None, 48)
    game_over_text = font.render("Game Over!", True, RED)
    score_text = font.render(f"Your Score: {score}", True, BLACK)
    play_again_text = font.render("Press R to Restart or Q to Quit", True, BLACK)

    screen.blit(game_over_text, (SCREEN_WIDTH // 2 - game_over_text.get_width() // 2, SCREEN_HEIGHT // 3))
    screen.blit(score_text, (SCREEN_WIDTH // 2 - score_text.get_width() // 2, SCREEN_HEIGHT // 2))
    screen.blit(play_again_text, (SCREEN_WIDTH // 2 - play_again_text.get_width() // 2, SCREEN_HEIGHT // 1.5))
    pygame.display.flip()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:
                    return True
                if event.key == pygame.K_q:
                    pygame.quit()
                    sys.exit()

# Main game loop
def main():
    player = Player()
    objects = [FallingObject()]
    score = 0
    run_game = True

    while run_game:
        screen.fill(WHITE)
        clock.tick(60)

        # Check for events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        # Move player
        player.move()

        # Update objects
        for obj in objects:
            obj.move()
            obj.draw()
            # Check for collision
            if (obj.y + obj.height > player.y and
                obj.x < player.x + player.width and
                obj.x + obj.width > player.x):
                run_game = False

        # Remove objects that are off-screen and add new ones
        objects = [obj for obj in objects if obj.y < SCREEN_HEIGHT]
        if random.random() < 0.02:  # Spawn new objects occasionally
            objects.append(FallingObject())

        # Increase object speed over time
        for obj in objects:
            obj.speed += OBJECT_INCREASE

        # Draw player and update score
        player.draw()
        score += 1
        font = pygame.font.SysFont(None, 36)
        score_text = font.render(f"Score: {score}", True, BLACK)
        screen.blit(score_text, (10, 10))

        # Update the display
        pygame.display.flip()

    # Show game over screen and restart or quit
    if game_over_screen(score):
        main()

# Run the game
main()
