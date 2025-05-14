import pygame
import random
import sys
import os
import math

# Initialize pygame
pygame.init()
pygame.mixer.init()  # Initialize the mixer for sound

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
DARK_BLUE = (5, 5, 30)
LIGHT_BLUE = (25, 25, 100)

# Create the game window
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Platformer Jumper")
clock = pygame.time.Clock()

# Background elements
stars = []
for _ in range(100):  # Create 100 stars
    x = random.randint(0, WIDTH)
    y = random.randint(0, HEIGHT)
    size = random.randint(1, 3)
    brightness = random.randint(100, 255)
    twinkle_speed = random.uniform(0.01, 0.05)
    twinkle_offset = random.uniform(0, 2 * math.pi)
    stars.append([x, y, size, brightness, twinkle_speed, twinkle_offset])

# Create background gradient surface
background = pygame.Surface((WIDTH, HEIGHT))
for y in range(HEIGHT):
    # Calculate gradient color
    ratio = y / HEIGHT
    r = int((DARK_BLUE[0] * (1 - ratio) + LIGHT_BLUE[0] * ratio))
    g = int((DARK_BLUE[1] * (1 - ratio) + LIGHT_BLUE[1] * ratio))
    b = int((DARK_BLUE[2] * (1 - ratio) + LIGHT_BLUE[2] * ratio))
    pygame.draw.line(background, (r, g, b), (0, y), (WIDTH, y))

# Sound variables
sound_enabled = True
jump_sound = None
boost_sound = None
land_sound = None
game_over_sound = None

# Check if sound files exist, if not, suggest generating them
sound_files = ["jump.wav", "boost.wav", "land.wav", "gameover.wav", "background.wav"]
sounds_exist = os.path.exists("sounds")
all_files_exist = sounds_exist and all(os.path.exists(os.path.join("sounds", f)) for f in sound_files)

if not all_files_exist:
    print("Sound files not found. Run generate_sounds.py first to create sound effects.")
    print("Continuing without sound...")
    sound_enabled = False
else:
    # Load sound effects
    try:
        jump_sound = pygame.mixer.Sound(os.path.join("sounds", "jump.wav"))
        jump_sound.set_volume(0.7)
        
        boost_sound = pygame.mixer.Sound(os.path.join("sounds", "boost.wav"))
        boost_sound.set_volume(0.8)
        
        land_sound = pygame.mixer.Sound(os.path.join("sounds", "land.wav"))
        land_sound.set_volume(0.6)
        
        game_over_sound = pygame.mixer.Sound(os.path.join("sounds", "gameover.wav"))
        game_over_sound.set_volume(0.9)
        
        # Load and play background music
        pygame.mixer.music.load(os.path.join("sounds", "background.wav"))
        pygame.mixer.music.set_volume(0.5)
        pygame.mixer.music.play(-1)  # -1 means loop indefinitely
        
        sound_enabled = True
        print("Sound effects loaded successfully!")
    except Exception as e:
        print(f"Error loading sounds: {e}")
        sound_enabled = False

# Game variables
player_pos = [WIDTH // 2, HEIGHT - 100]  # Center position of the player
player_radius = PLAYER_SIZE // 2
platforms = []
player_velocity_y = 0
score = 0
game_over = False
font = pygame.font.SysFont(None, 36)
boost_jumps = 3  # Limited number of boost jumps
on_ground = False  # Track if player is on a platform
visited_platforms = set()  # Track platforms the player has already visited
show_sound_status = True  # Show sound status at start
sound_status_timer = 180  # Show for 3 seconds (60 FPS * 3)

# Particle system for boost jump effect
particles = []

class Particle:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.vx = random.uniform(-1, 1)
        self.vy = random.uniform(-2, 0)
        self.radius = random.randint(2, 6)
        self.color = (random.randint(200, 255), random.randint(100, 200), 0)
        self.lifetime = random.randint(20, 40)
    
    def update(self):
        self.x += self.vx
        self.y += self.vy
        self.vy += 0.05  # Gravity effect on particles
        self.lifetime -= 1
        # Fade out effect
        if self.lifetime < 10:
            self.radius *= 0.9
    
    def draw(self, surface):
        if self.radius > 0.5:
            pygame.draw.circle(surface, self.color, (int(self.x), int(self.y)), int(self.radius))

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

# Function to play a sound safely
def play_sound(sound):
    if sound_enabled and sound is not None:
        try:
            sound.play()
        except:
            pass

# Function to update and draw the background
def update_background(time):
    # Draw the gradient background
    screen.blit(background, (0, 0))
    
    # Update and draw stars with twinkling effect
    for star in stars:
        x, y, size, base_brightness, twinkle_speed, twinkle_offset = star
        # Calculate twinkling effect
        brightness = base_brightness + int(50 * math.sin(time * twinkle_speed + twinkle_offset))
        brightness = max(min(brightness, 255), 50)  # Keep brightness in valid range
        
        # Draw the star
        pygame.draw.circle(screen, (brightness, brightness, brightness), (int(x), int(y)), size)

# Game loop
def main():
    global player_velocity_y, score, game_over, boost_jumps, on_ground, visited_platforms, player_pos, particles
    global show_sound_status, sound_status_timer, sound_enabled
    
    running = True
    time_passed = 0
    while running:
        time_passed += 0.1  # Increment time for animations
        
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
                    
                    # Create boost jump particles
                    for _ in range(20):
                        particles.append(Particle(player_pos[0], player_pos[1] + player_radius))
                    
                    # Play boost sound
                    play_sound(boost_sound)
                
                # Toggle sound with M key
                if event.key == pygame.K_m:
                    sound_enabled = not sound_enabled
                    show_sound_status = True
                    sound_status_timer = 180
                    
                    if sound_enabled:
                        try:
                            pygame.mixer.music.play(-1)
                        except:
                            pass
                    else:
                        try:
                            pygame.mixer.music.stop()
                        except:
                            pass
        
        if not game_over:
            # Player movement
            keys = pygame.key.get_pressed()
            if keys[pygame.K_LEFT]:
                player_pos[0] -= PLAYER_SPEED
            if keys[pygame.K_RIGHT]:
                player_pos[0] += PLAYER_SPEED
            
            # Wrap around screen edges (teleport from one side to the other)
            if player_pos[0] - player_radius > WIDTH:
                player_pos[0] = -player_radius
            elif player_pos[0] + player_radius < 0:
                player_pos[0] = WIDTH + player_radius
            
            # Apply gravity
            player_velocity_y += GRAVITY
            player_pos[1] += player_velocity_y
            
            # Reset on_ground status
            on_ground = False
            
            # Check for platform collisions (only when falling)
            if player_velocity_y > 0:
                for platform in platforms:
                    # Check if the bottom of the ball is touching the platform
                    if (player_pos[1] + player_radius >= platform.top and 
                        player_pos[1] + player_radius <= platform.top + 15 and  # More forgiving collision
                        player_pos[0] + player_radius > platform.left + 5 and    # More forgiving collision
                        player_pos[0] - player_radius < platform.right - 5):      # More forgiving collision
                        player_pos[1] = platform.top - player_radius
                        player_velocity_y = -JUMP_POWER
                        on_ground = True
                        
                        # Play jump sound
                        play_sound(jump_sound)
                        
                        # Only increment score for platforms not visited before
                        platform_id = id(platform)
                        if platform_id not in visited_platforms:
                            visited_platforms.add(platform_id)
                            score += 1
                            
                            # Play landing sound for new platforms
                            play_sound(land_sound)
                            
                            # Replenish boost jumps when landing on a new platform
                            if score % 5 == 0:  # Every 5 platforms, get a boost jump
                                boost_jumps = min(boost_jumps + 1, 3)  # Max 3 boost jumps
            
            # Check if player fell off the bottom
            if player_pos[1] - player_radius > HEIGHT:
                game_over = True
                # Play game over sound
                play_sound(game_over_sound)
                try:
                    pygame.mixer.music.stop()  # Stop background music
                except:
                    pass
            
            # Scroll the screen when player reaches upper half
            if player_pos[1] < HEIGHT // 2:
                scroll_speed = 4  # Slightly slower scrolling
                player_pos[1] += scroll_speed
                for platform in platforms:
                    platform.y += scroll_speed
                    # Remove platforms that have gone off screen
                    if platform.top > HEIGHT:
                        # Remove from visited set if it exists there
                        platform_id = id(platform)
                        if platform_id in visited_platforms:
                            visited_platforms.remove(platform_id)
                        
                        platforms.remove(platform)
                        # Create a new platform at the top
                        x = random.randint(50, WIDTH - PLATFORM_WIDTH - 50)
                        y = min([p.y for p in platforms]) - PLATFORM_GAP  # Place consistently above highest platform
                        platforms.append(pygame.Rect(x, y, PLATFORM_WIDTH, PLATFORM_HEIGHT))
                
                # Scroll stars with parallax effect (stars move slower than platforms)
                for star in stars:
                    star[1] += scroll_speed * 0.7  # Stars move at 70% of platform speed
                    if star[1] > HEIGHT:
                        star[1] = 0
                        star[0] = random.randint(0, WIDTH)
        
        # Update particles
        for particle in particles[:]:
            particle.update()
            if particle.lifetime <= 0:
                particles.remove(particle)
        
        # Drawing - start with background
        update_background(time_passed)
        
        # Draw particles behind player
        for particle in particles:
            particle.draw(screen)
        
        # Draw player as a ball
        pygame.draw.circle(screen, RED, (int(player_pos[0]), int(player_pos[1])), player_radius)
        
        # Add a shine effect to the ball
        shine_pos = (int(player_pos[0] - player_radius * 0.3), int(player_pos[1] - player_radius * 0.3))
        shine_radius = int(player_radius * 0.25)
        pygame.draw.circle(screen, (255, 200, 200), shine_pos, shine_radius)
        
        # Draw platforms with different colors based on height
        for platform in platforms:
            # Ensure color values are integers between 0-255
            color_value = max(0, min(255, int(255 - (platform.y * 255 // HEIGHT))))
            platform_color = (0, color_value, color_value)
            pygame.draw.rect(screen, platform_color, platform)
            
            # Add a highlight to the top of the platform
            pygame.draw.line(screen, (min(255, color_value + 50), min(255, color_value + 50), min(255, color_value + 50)), 
                            (platform.left, platform.top), (platform.right, platform.top), 2)
        
        # Draw score
        score_text = font.render(f"Score: {score}", True, WHITE)
        screen.blit(score_text, (10, 10))
        
        # Draw boost jumps remaining
        boost_text = font.render("Boosts:", True, WHITE)
        screen.blit(boost_text, (WIDTH - 120, 20))
        
        for i in range(boost_jumps):
            # Draw boost indicators as small glowing orbs
            boost_x = WIDTH - 30 - i*25
            boost_y = 20
            # Outer glow
            pygame.draw.circle(screen, (255, 200, 100), (boost_x + 10, boost_y + 10), 12)
            # Inner core
            pygame.draw.circle(screen, ORANGE, (boost_x + 10, boost_y + 10), 8)
            # Shine
            pygame.draw.circle(screen, (255, 255, 200), (boost_x + 7, boost_y + 7), 3)
        
        # Draw instructions
        if score < 3:
            instructions = font.render("Use LEFT/RIGHT to move, SPACE for boost jump", True, YELLOW)
            screen.blit(instructions, (WIDTH // 2 - 250, 40))
            
            # Add sound control instructions
            sound_instructions = font.render("Press M to toggle sound", True, YELLOW)
            screen.blit(sound_instructions, (WIDTH // 2 - 100, 70))
        
        # Show sound status when toggled
        if show_sound_status:
            status = "ON" if sound_enabled else "OFF"
            status_text = font.render(f"Sound: {status}", True, WHITE)
            screen.blit(status_text, (WIDTH // 2 - 50, HEIGHT - 40))
            sound_status_timer -= 1
            if sound_status_timer <= 0:
                show_sound_status = False
        
        # Draw game over
        if game_over:
            # Semi-transparent overlay
            overlay = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
            overlay.fill((0, 0, 0, 128))
            screen.blit(overlay, (0, 0))
            
            game_over_text = font.render("GAME OVER! Press R to restart", True, WHITE)
            screen.blit(game_over_text, (WIDTH // 2 - 180, HEIGHT // 2))
            final_score = font.render(f"Final Score: {score}", True, WHITE)
            screen.blit(final_score, (WIDTH // 2 - 80, HEIGHT // 2 + 40))
        
        pygame.display.flip()
        clock.tick(FPS)
    
    pygame.quit()
    sys.exit()

def restart_game():
    global player_pos, platforms, player_velocity_y, score, game_over, boost_jumps, on_ground, visited_platforms, particles
    player_pos = [WIDTH // 2, HEIGHT - 100]
    platforms = []
    player_velocity_y = 0
    score = 0
    game_over = False
    boost_jumps = 3
    on_ground = False
    visited_platforms = set()  # Reset visited platforms
    particles = []  # Clear particles
    create_platforms()
    
    # Restart music if it was stopped
    if sound_enabled:
        try:
            if not pygame.mixer.music.get_busy():
                pygame.mixer.music.play(-1)
        except:
            pass

if __name__ == "__main__":
    main()
    