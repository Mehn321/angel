import pygame
import random
import sys

# Initialize pygame
pygame.init()

# Game constants
WIDTH, HEIGHT = 800, 600
PLAYER_SIZE = 40
PLATFORM_WIDTH = 120  # Wider platforms
PLATFORM_HEIGHT = 20
GRAVITY = 0.4  # Reduced gravity
JUMP_POWER = 10
PLAYER_SPEED = 6  # Slightly faster movement
FPS = 60
PLATFORM_GAP = 80  # Consistent gap between platforms

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
PURPLE = (128, 0, 128)
ORANGE = (255, 165, 0)

# Create the game window
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Platformer Jumper")
clock = pygame.time.Clock()

# Game variables
player = pygame.Rect(WIDTH // 2, HEIGHT - 100, PLAYER_SIZE, PLAYER_SIZE)
platforms = []
player_velocity_y = 0
score = 0
game_over = False
font = pygame.font.SysFont(None, 36)
boost_jumps = 3  # Limited number of boost jumps
on_ground = False  # Track if player is on a platform

# Create initial platforms
def create_platforms():
    # Starting platform directly under the player
    platforms.append(pygame.Rect(WIDTH // 2 - PLATFORM_WIDTH // 2, HEIGHT - 50, PLATFORM_WIDTH, PLATFORM_HEIGHT))
    
    # Create platforms with more consistent spacing
    for i in range(15):  # More platforms
        x = random.randint(50, WIDTH - PLATFORM_WIDTH - 50)  # Keep away from edges
        y = HEIGHT - 150 - i * PLATFORM_GAP  # Consistent vertical spacing
        platforms.append(pygame.Rect(x, y, PLATFORM_WIDTH, PLATFORM_HEIGHT))

create_platforms()

# Game loop
def main():
    global player_velocity_y, score, game_over, boost_jumps, on_ground
    
    running = True
    while running:
        # Event handling
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r and game_over:
                    restart_game()
                # Boost jump with limited uses
                if event.key == pygame.K_SPACE and not game_over and boost_jumps > 0 and not on_ground:
                    player_velocity_y = -JUMP_POWER
                    boost_jumps -= 1
        
        if not game_over:
            # Player movement
            keys = pygame.key.get_pressed()
            if keys[pygame.K_LEFT] and player.left > 0:
                player.x -= PLAYER_SPEED
            if keys[pygame.K_RIGHT] and player.right < WIDTH:
                player.x += PLAYER_SPEED
            
            # Wrap around screen edges (teleport from one side to the other)
            if player.right < 0:
                player.left = WIDTH
            elif player.left > WIDTH:
                player.right = 0
            
            # Apply gravity
            player_velocity_y += GRAVITY
            player.y += player_velocity_y
            
            # Reset on_ground status
            on_ground = False
            
            # Check for platform collisions (only when falling)
            if player_velocity_y > 0:
                for platform in platforms:
                    if (player.bottom >= platform.top and 
                        player.bottom <= platform.top + 15 and  # More forgiving collision
                        player.right > platform.left + 5 and    # More forgiving collision
                        player.left < platform.right - 5):      # More forgiving collision
                        player.bottom = platform.top
                        player_velocity_y = -JUMP_POWER
                        score += 1
                        on_ground = True
                        
                        # Replenish boost jumps when landing on a platform
                        if score % 5 == 0:  # Every 5 platforms, get a boost jump
                            boost_jumps = min(boost_jumps + 1, 3)  # Max 3 boost jumps
            
            # Check if player fell off the bottom
            if player.top > HEIGHT:
                game_over = True
            
            # Scroll the screen when player reaches upper half
            if player.top < HEIGHT // 2:
                scroll_speed = 4  # Slightly slower scrolling
                player.y += scroll_speed
                for platform in platforms:
                    platform.y += scroll_speed
                    # Remove platforms that have gone off screen
                    if platform.top > HEIGHT:
                        platforms.remove(platform)
                        # Create a new platform at the top
                        x = random.randint(50, WIDTH - PLATFORM_WIDTH - 50)
                        y = min([p.y for p in platforms]) - PLATFORM_GAP  # Place consistently above highest platform
                        platforms.append(pygame.Rect(x, y, PLATFORM_WIDTH, PLATFORM_HEIGHT))
        
        # Drawing
        screen.fill(BLACK)
        
        # Draw player
        pygame.draw.rect(screen, RED, player)
        
        # Draw platforms with different colors based on height
        for platform in platforms:
            # Ensure color values are integers between 0-255
            color_value = max(0, min(255, int(255 - (platform.y * 255 // HEIGHT))))
            platform_color = (0, color_value, color_value)
            pygame.draw.rect(screen, platform_color, platform)
        
        # Draw score
        score_text = font.render(f"Score: {score}", True, WHITE)
        screen.blit(score_text, (10, 10))
        
        # Draw boost jumps remaining
        for i in range(boost_jumps):
            pygame.draw.rect(screen, ORANGE, (WIDTH - 30 - i*25, 20, 20, 20))
        boost_text = font.render("Boosts:", True, WHITE)
        screen.blit(boost_text, (WIDTH - 120, 20))
        
        # Draw instructions
        if score < 3:
            instructions = font.render("Use LEFT/RIGHT to move, SPACE for boost jump", True, YELLOW)
            screen.blit(instructions, (WIDTH // 2 - 250, 40))
        
        # Draw game over
        if game_over:
            game_over_text = font.render("GAME OVER! Press R to restart", True, WHITE)
            screen.blit(game_over_text, (WIDTH // 2 - 180, HEIGHT // 2))
            final_score = font.render(f"Final Score: {score}", True, WHITE)
            screen.blit(final_score, (WIDTH // 2 - 80, HEIGHT // 2 + 40))
        
        pygame.display.flip()
        clock.tick(FPS)
    
    pygame.quit()
    sys.exit()

def restart_game():
    global player, platforms, player_velocity_y, score, game_over, boost_jumps, on_ground
    player = pygame.Rect(WIDTH // 2, HEIGHT - 100, PLAYER_SIZE, PLAYER_SIZE)
    platforms = []
    player_velocity_y = 0
    score = 0
    game_over = False
    boost_jumps = 3
    on_ground = False
    create_platforms()

if __name__ == "__main__":
    main()
