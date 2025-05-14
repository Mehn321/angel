import pygame
import random
import sys
import os
import math

# Initialize pygame
pygame.init()
pygame.mixer.init()

# Game constants
WIDTH, HEIGHT = 800, 600
PLAYER_SIZE = 40
PLATFORM_WIDTH, PLATFORM_HEIGHT = 120, 20
GRAVITY, JUMP_POWER, PLAYER_SPEED = 0.4, 10, 6
FPS, PLATFORM_GAP = 60, 80

# Colors
WHITE, BLACK = (255, 255, 255), (0, 0, 0)
RED, GREEN, BLUE = (255, 0, 0), (0, 255, 0), (0, 0, 255)
YELLOW, PURPLE, ORANGE = (255, 255, 0), (128, 0, 128), (255, 165, 0)
DARK_BLUE, LIGHT_BLUE = (5, 5, 30), (25, 25, 100)

# Setup
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Platformer Jumper")
clock = pygame.time.Clock()

# Background elements
stars = [[random.randint(0, WIDTH), random.randint(0, HEIGHT), 
          random.randint(1, 3), random.randint(100, 255),
          random.uniform(0.01, 0.05), random.uniform(0, 2 * math.pi)] 
         for _ in range(100)]

# Create background gradient
background = pygame.Surface((WIDTH, HEIGHT))
for y in range(HEIGHT):
    ratio = y / HEIGHT
    r = int((DARK_BLUE[0] * (1 - ratio) + LIGHT_BLUE[0] * ratio))
    g = int((DARK_BLUE[1] * (1 - ratio) + LIGHT_BLUE[1] * ratio))
    b = int((DARK_BLUE[2] * (1 - ratio) + LIGHT_BLUE[2] * ratio))
    pygame.draw.line(background, (r, g, b), (0, y), (WIDTH, y))

# Sound setup
sound_enabled = True
sound_files = ["jump.wav", "boost.wav", "land.wav", "gameover.wav", "background.wav"]
sounds_exist = os.path.exists("sounds") and all(os.path.exists(os.path.join("sounds", f)) for f in sound_files)

if not sounds_exist:
    print("Sound files not found. Run generate_sounds.py first to create sound effects.")
    sound_enabled = False
else:
    try:
        jump_sound = pygame.mixer.Sound(os.path.join("sounds", "jump.wav"))
        jump_sound.set_volume(0.7)
        boost_sound = pygame.mixer.Sound(os.path.join("sounds", "boost.wav"))
        boost_sound.set_volume(0.8)
        land_sound = pygame.mixer.Sound(os.path.join("sounds", "land.wav"))
        land_sound.set_volume(0.6)
        game_over_sound = pygame.mixer.Sound(os.path.join("sounds", "gameover.wav"))
        game_over_sound.set_volume(0.9)
        pygame.mixer.music.load(os.path.join("sounds", "background.wav"))
        pygame.mixer.music.set_volume(0.5)
        pygame.mixer.music.play(-1)
    except Exception as e:
        print(f"Error loading sounds: {e}")
        sound_enabled = False

# Game variables
player_pos = [WIDTH // 2, HEIGHT - 100]
player_radius = PLAYER_SIZE // 2
platforms = []
player_velocity_y = 0
score = 0
game_over = False
font = pygame.font.SysFont(None, 36)
boost_jumps = 3
on_ground = False
visited_platforms = set()
show_sound_status = True
sound_status_timer = 180
particles = []

class Particle:
    def __init__(self, x, y):
        self.x, self.y = x, y
        self.vx = random.uniform(-1, 1)
        self.vy = random.uniform(-2, 0)
        self.radius = random.randint(2, 6)
        self.color = (random.randint(200, 255), random.randint(100, 200), 0)
        self.lifetime = random.randint(20, 40)
    
    def update(self):
        self.x += self.vx
        self.y += self.vy
        self.vy += 0.05
        self.lifetime -= 1
        if self.lifetime < 10:
            self.radius *= 0.9
    
    def draw(self, surface):
        if self.radius > 0.5:
            pygame.draw.circle(surface, self.color, (int(self.x), int(self.y)), int(self.radius))

def create_platforms():
    platforms.append(pygame.Rect(WIDTH // 2 - PLATFORM_WIDTH // 2, HEIGHT - 50, PLATFORM_WIDTH, PLATFORM_HEIGHT))
    for i in range(15):
        x = random.randint(50, WIDTH - PLATFORM_WIDTH - 50)
        y = HEIGHT - 150 - i * PLATFORM_GAP
        platforms.append(pygame.Rect(x, y, PLATFORM_WIDTH, PLATFORM_HEIGHT))

create_platforms()

def play_sound(sound):
    if sound_enabled and sound is not None:
        try:
            sound.play()
        except:
            pass

def update_background(time):
    screen.blit(background, (0, 0))
    for star in stars:
        x, y, size, base_brightness, twinkle_speed, twinkle_offset = star
        brightness = max(min(base_brightness + int(50 * math.sin(time * twinkle_speed + twinkle_offset)), 255), 50)
        pygame.draw.circle(screen, (brightness, brightness, brightness), (int(x), int(y)), size)

def restart_game():
    global player_pos, platforms, player_velocity_y, score, game_over, boost_jumps, on_ground, visited_platforms, particles
    player_pos = [WIDTH // 2, HEIGHT - 100]
    platforms = []
    player_velocity_y = 0
    score = 0
    game_over = False
    boost_jumps = 3
    on_ground = False
    visited_platforms = set()
    particles = []
    create_platforms()
    if sound_enabled:
        try:
            if not pygame.mixer.music.get_busy():
                pygame.mixer.music.play(-1)
        except:
            pass

def main():
    global player_velocity_y, score, game_over, boost_jumps, on_ground, visited_platforms, player_pos, particles
    global show_sound_status, sound_status_timer, sound_enabled
    
    running = True
    time_passed = 0
    
    while running:
        time_passed += 0.1
        
        # Event handling
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r and game_over:
                    restart_game()
                if event.key == pygame.K_SPACE and not game_over and boost_jumps > 0 and not on_ground:
                    player_velocity_y = -JUMP_POWER
                    boost_jumps -= 1
                    particles.extend([Particle(player_pos[0], player_pos[1] + player_radius) for _ in range(20)])
                    play_sound(boost_sound)
                if event.key == pygame.K_m:
                    sound_enabled = not sound_enabled
                    show_sound_status = True
                    sound_status_timer = 180
                    try:
                        pygame.mixer.music.play(-1) if sound_enabled else pygame.mixer.music.stop()
                    except:
                        pass
        
        if not game_over:
            # Player movement
            keys = pygame.key.get_pressed()
            if keys[pygame.K_LEFT]:
                player_pos[0] -= PLAYER_SPEED
            if keys[pygame.K_RIGHT]:
                player_pos[0] += PLAYER_SPEED
            
            # Screen wrapping
            if player_pos[0] - player_radius > WIDTH:
                player_pos[0] = -player_radius
            elif player_pos[0] + player_radius < 0:
                player_pos[0] = WIDTH + player_radius
            
            # Physics
            player_velocity_y += GRAVITY
            player_pos[1] += player_velocity_y
            on_ground = False
            
            # Platform collision
            if player_velocity_y > 0:
                for platform in platforms:
                    if (player_pos[1] + player_radius >= platform.top and 
                        player_pos[1] + player_radius <= platform.top + 15 and
                        player_pos[0] + player_radius > platform.left + 5 and
                        player_pos[0] - player_radius < platform.right - 5):
                        player_pos[1] = platform.top - player_radius
                        player_velocity_y = -JUMP_POWER
                        on_ground = True
                        play_sound(jump_sound)
                        
                        platform_id = id(platform)
                        if platform_id not in visited_platforms:
                            visited_platforms.add(platform_id)
                            score += 1
                            play_sound(land_sound)
                            if score % 5 == 0:
                                boost_jumps = min(boost_jumps + 1, 3)
            
            # Game over check
            if player_pos[1] - player_radius > HEIGHT:
                game_over = True
                play_sound(game_over_sound)
                try:
                    pygame.mixer.music.stop()
                except:
                    pass
            
            # Screen scrolling
            if player_pos[1] < HEIGHT // 2:
                scroll_speed = 4
                player_pos[1] += scroll_speed
                
                # Update platforms
                for platform in platforms[:]:
                    platform.y += scroll_speed
                    if platform.top > HEIGHT:
                        platform_id = id(platform)
                        if platform_id in visited_platforms:
                            visited_platforms.remove(platform_id)
                        platforms.remove(platform)
                        x = random.randint(50, WIDTH - PLATFORM_WIDTH - 50)
                        y = min([p.y for p in platforms]) - PLATFORM_GAP
                        platforms.append(pygame.Rect(x, y, PLATFORM_WIDTH, PLATFORM_HEIGHT))
                
                # Update stars with parallax
                for star in stars:
                    star[1] += scroll_speed * 0.7
                    if star[1] > HEIGHT:
                        star[1] = 0
                        star[0] = random.randint(0, WIDTH)
        
        # Update particles
        for particle in particles[:]:
            particle.update()
            if particle.lifetime <= 0:
                particles.remove(particle)
        
        # Drawing
        update_background(time_passed)
        
        # Draw particles
        for particle in particles:
            particle.draw(screen)
        
        # Draw player
        pygame.draw.circle(screen, RED, (int(player_pos[0]), int(player_pos[1])), player_radius)
        pygame.draw.circle(screen, (255, 200, 200), 
                          (int(player_pos[0] - player_radius * 0.3), int(player_pos[1] - player_radius * 0.3)), 
                          int(player_radius * 0.25))
        
        # Draw platforms
        for platform in platforms:
            color_value = max(0, min(255, int(255 - (platform.y * 255 // HEIGHT))))
            platform_color = (0, color_value, color_value)
            pygame.draw.rect(screen, platform_color, platform)
            pygame.draw.line(screen, (min(255, color_value + 50), min(255, color_value + 50), min(255, color_value + 50)), 
                            (platform.left, platform.top), (platform.right, platform.top), 2)
        
        # Draw UI
        screen.blit(font.render(f"Score: {score}", True, WHITE), (10, 10))
        screen.blit(font.render("Boosts:", True, WHITE), (WIDTH - 120, 20))
        
        for i in range(boost_jumps):
            boost_x = WIDTH - 30 - i*25
            boost_y = 20
            pygame.draw.circle(screen, (255, 200, 100), (boost_x + 10, boost_y + 10), 12)
            pygame.draw.circle(screen, ORANGE, (boost_x + 10, boost_y + 10), 8)
            pygame.draw.circle(screen, (255, 255, 200), (boost_x + 7, boost_y + 7), 3)
        
        # Instructions
        if score < 3:
            screen.blit(font.render("Use LEFT/RIGHT to move, SPACE for boost jump", True, YELLOW), (WIDTH // 2 - 250, 40))
            screen.blit(font.render("Press M to toggle sound", True, YELLOW), (WIDTH // 2 - 100, 70))
        
        # Sound status
        if show_sound_status:
            status = "ON" if sound_enabled else "OFF"
            screen.blit(font.render(f"Sound: {status}", True, WHITE), (WIDTH // 2 - 50, HEIGHT - 40))
            sound_status_timer -= 1
            if sound_status_timer <= 0:
                show_sound_status = False
        
        # Game over screen
        if game_over:
            overlay = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
            overlay.fill((0, 0, 0, 128))
            screen.blit(overlay, (0, 0))
            screen.blit(font.render("GAME OVER! Press R to restart", True, WHITE), (WIDTH // 2 - 180, HEIGHT // 2))
            screen.blit(font.render(f"Final Score: {score}", True, WHITE), (WIDTH // 2 - 80, HEIGHT // 2 + 40))
        
        pygame.display.flip()
        clock.tick(FPS)
    
    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()
