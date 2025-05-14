import pygame
import random
import sys

# Initialize pygame
pygame.init()

# Game constants
WIDTH, HEIGHT = 800, 600
PLAYER_SIZE = 50
ENEMY_SIZE = 30
BULLET_SIZE = 5
PLAYER_SPEED = 8
ENEMY_SPEED = 3
BULLET_SPEED = 10
FPS = 60

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)

# Create the game window
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Space Shooter")
clock = pygame.time.Clock()

# Player setup
player = pygame.Rect(WIDTH // 2 - PLAYER_SIZE // 2, HEIGHT - PLAYER_SIZE - 20, PLAYER_SIZE, PLAYER_SIZE)
bullets = []
enemies = []
score = 0
game_over = False
font = pygame.font.SysFont(None, 36)

# Game loop
def main():
    global score, game_over
    
    # Create initial enemies
    for _ in range(5):
        create_enemy()
    
    running = True
    while running:
        # Event handling
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE and not game_over:
                    # Create a bullet
                    bullet = pygame.Rect(player.centerx - BULLET_SIZE // 2, player.top, BULLET_SIZE, BULLET_SIZE * 2)
                    bullets.append(bullet)
                if event.key == pygame.K_r and game_over:
                    # Restart game
                    restart_game()
        
        if not game_over:
            # Player movement
            keys = pygame.key.get_pressed()
            if keys[pygame.K_LEFT] and player.left > 0:
                player.x -= PLAYER_SPEED
            if keys[pygame.K_RIGHT] and player.right < WIDTH:
                player.x += PLAYER_SPEED
            
            # Update bullets
            for bullet in bullets[:]:
                bullet.y -= BULLET_SPEED
                if bullet.y < 0:
                    bullets.remove(bullet)
            
            # Update enemies
            if random.random() < 0.02:  # 2% chance each frame to create a new enemy
                create_enemy()
                
            for enemy in enemies[:]:
                enemy.y += ENEMY_SPEED
                if enemy.y > HEIGHT:
                    enemies.remove(enemy)
                    
                # Check for collisions with bullets
                for bullet in bullets[:]:
                    if enemy.colliderect(bullet):
                        enemies.remove(enemy)
                        bullets.remove(bullet)
                        score += 10
                        break
                
                # Check for collision with player
                if enemy.colliderect(player):
                    game_over = True
        
        # Drawing
        screen.fill(BLACK)
        
        # Draw player (as a triangle spaceship)
        if not game_over:
            pygame.draw.polygon(screen, GREEN, [
                (player.centerx, player.top),
                (player.left, player.bottom),
                (player.right, player.bottom)
            ])
        
        # Draw bullets
        for bullet in bullets:
            pygame.draw.rect(screen, BLUE, bullet)
        
        # Draw enemies
        for enemy in enemies:
            pygame.draw.rect(screen, RED, enemy)
        
        # Draw score
        score_text = font.render(f"Score: {score}", True, WHITE)
        screen.blit(score_text, (10, 10))
        
        # Draw game over
        if game_over:
            game_over_text = font.render("GAME OVER! Press R to restart", True, WHITE)
            screen.blit(game_over_text, (WIDTH // 2 - 180, HEIGHT // 2))
        
        pygame.display.flip()
        clock.tick(FPS)
    
    pygame.quit()
    sys.exit()

def create_enemy():
    x = random.randint(0, WIDTH - ENEMY_SIZE)
    enemy = pygame.Rect(x, -ENEMY_SIZE, ENEMY_SIZE, ENEMY_SIZE)
    enemies.append(enemy)

def restart_game():
    global player, bullets, enemies, score, game_over
    player = pygame.Rect(WIDTH // 2 - PLAYER_SIZE // 2, HEIGHT - PLAYER_SIZE - 20, PLAYER_SIZE, PLAYER_SIZE)
    bullets = []
    enemies = []
    score = 0
    game_over = False
    for _ in range(5):
        create_enemy()

if __name__ == "__main__":
    main()
