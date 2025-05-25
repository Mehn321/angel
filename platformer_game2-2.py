import pygame, random, sys, os, math

# Initialize pygame
pygame.init()
pygame.mixer.init()

# Game constants
WIDTH, HEIGHT = 800, 600
PLAYER_SIZE, PLATFORM_WIDTH, PLATFORM_HEIGHT = 40, 120, 20
GRAVITY, JUMP_POWER, PLAYER_SPEED = 0.4, 10, 6
FPS, PLATFORM_GAP = 60, 80

# Colors
WHITE, BLACK = (255, 255, 255), (0, 0, 0)
RED, GREEN, BLUE = (255, 0, 0), (0, 255, 0), (0, 0, 255)
YELLOW, ORANGE = (255, 255, 0), (255, 165, 0)
DARKER_BLUE_PLATFORM = (25, 80, 130)  # Very dark blue
BLUE_HIGHLIGHT = (52, 152, 219)  # Slightly lighter blue for highlight

# Setup
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Platformer Jumper")
clock = pygame.time.Clock()

# Load background image
try:
    background = pygame.image.load(os.path.join("images", "background.jpg")).convert()
    background = pygame.transform.scale(background, (WIDTH, HEIGHT))
except Exception as e:
    print(f"Error loading background image: {e}")
    background = pygame.Surface((WIDTH, HEIGHT))
    background.fill((135, 206, 235))  # Sky blue

# Sound setup
sound_enabled = True
sound_files = ["jump.wav", "boost.wav", "land.wav", "gameover.wav", "background.wav"]
sounds_exist = os.path.exists("sounds") and all(os.path.exists(os.path.join("sounds", f)) for f in sound_files)

if sounds_exist:
    try:
        jump_sound = pygame.mixer.Sound(os.path.join("sounds", "jump.wav"))
        boost_sound = pygame.mixer.Sound(os.path.join("sounds", "boost.wav"))
        land_sound = pygame.mixer.Sound(os.path.join("sounds", "land.wav"))
        game_over_sound = pygame.mixer.Sound(os.path.join("sounds", "gameover.wav"))
        pygame.mixer.music.load(os.path.join("sounds", "background.wav"))
        pygame.mixer.music.set_volume(0.5)
    except Exception as e:
        print(f"Error loading sounds: {e}")
        sound_enabled = False
else:
    print("Sound files not found. Run generate_sounds.py first to create sound effects.")
    sound_enabled = False

# Game variables
player_pos = [WIDTH // 2, HEIGHT - 100]
player_radius = PLAYER_SIZE // 2
platforms = []
player_velocity_y = 0
score, boost_jumps, max_height, platforms_landed, boost_jumps_used, game_time = 0, 3, 0, 0, 0, 0
game_over, on_ground, show_sound_status, game_started = False, False, True, False
visited_platforms, particles = set(), []
sound_status_timer = 180
font = pygame.font.SysFont(None, 36)
title_font = pygame.font.SysFont(None, 64)
small_font = pygame.font.SysFont(None, 24)

# Particle class
class Particle:
    def __init__(self, x, y):
        self.x, self.y = x, y
        self.vx, self.vy = random.uniform(-1, 1), random.uniform(-2, 0)
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

# Helper functions
def create_platforms():
    platforms.clear()
    platforms.append(pygame.Rect(WIDTH // 2 - PLATFORM_WIDTH // 2, HEIGHT - 50, PLATFORM_WIDTH, PLATFORM_HEIGHT))
    for i in range(15):
        x = random.randint(50, WIDTH - PLATFORM_WIDTH - 50)
        y = HEIGHT - 150 - i * PLATFORM_GAP
        platforms.append(pygame.Rect(x, y, PLATFORM_WIDTH, PLATFORM_HEIGHT))

def play_sound(sound):
    if sound_enabled and sound is not None:
        try:
            sound.play()
        except:
            pass

def draw_button(surface, text, rect, color, hover_color=None, text_color=WHITE):
    mouse_pos = pygame.mouse.get_pos()
    is_hovering = rect.collidepoint(mouse_pos)
    button_color = hover_color if hover_color and is_hovering else color
    pygame.draw.rect(surface, button_color, rect)
    pygame.draw.rect(surface, WHITE, rect, 2)
    text_surf = font.render(text, True, text_color)
    text_rect = text_surf.get_rect(center=rect.center)
    surface.blit(text_surf, text_rect)
    return is_hovering

def draw_start_dashboard():
    dashboard = pygame.Surface((WIDTH - 100, HEIGHT - 100), pygame.SRCALPHA)
    dashboard.fill((20, 20, 50, 220))
    pygame.draw.rect(dashboard, WHITE, (0, 0, dashboard.get_width(), dashboard.get_height()), 2)
    
    title = title_font.render("PLATFORMER JUMPER", True, YELLOW)
    dashboard.blit(title, (dashboard.get_width() // 2 - title.get_width() // 2, 30))
    
    start_btn = pygame.Rect(dashboard.get_width() // 2 - 100, 150, 200, 50)
    sound_btn = pygame.Rect(dashboard.get_width() // 2 - 100, 220, 200, 50)
    
    draw_button(dashboard, "START GAME", start_btn, GREEN, (100, 255, 100))
    sound_text = "SOUND: ON" if sound_enabled else "SOUND: OFF"
    draw_button(dashboard, sound_text, sound_btn, BLUE, (100, 100, 255))
    
    controls_title = font.render("Instructions:", True, WHITE)
    dashboard.blit(controls_title, (dashboard.get_width() // 2 - controls_title.get_width() // 2, 300))
    
    controls = [
        "LEFT/RIGHT - Move",
        "SPACE - Boost Jump (when in air)",
        "M - Toggle Sound",
        "R - Restart (when game over)"
    ]
    
    y_offset = 340
    for control in controls:
        control_text = small_font.render(control, True, WHITE)
        dashboard.blit(control_text, (dashboard.get_width() // 2 - control_text.get_width() // 2, y_offset))
        y_offset += 30
    
    dashboard_pos = (50, 50)
    screen.blit(dashboard, dashboard_pos)
    
    return (
        pygame.Rect(start_btn.x + dashboard_pos[0], start_btn.y + dashboard_pos[1], start_btn.width, start_btn.height),
        pygame.Rect(sound_btn.x + dashboard_pos[0], sound_btn.y + dashboard_pos[1], sound_btn.width, sound_btn.height)
    )

def restart_game():
    global player_pos, player_velocity_y, score, game_over, boost_jumps, on_ground
    global visited_platforms, particles, max_height, platforms_landed, boost_jumps_used, game_time
    player_pos = [WIDTH // 2, HEIGHT - 100]
    player_velocity_y, score, game_over, boost_jumps = 0, 0, False, 3
    on_ground, max_height, platforms_landed, boost_jumps_used, game_time = False, 0, 0, 0, 0
    visited_platforms.clear()
    particles.clear()
    create_platforms()
    if sound_enabled and not pygame.mixer.music.get_busy():
        try:
            pygame.mixer.music.play(-1)
        except:
            pass

def start_game():
    global game_started, frame_count
    game_started = True
    frame_count = 0
    restart_game()
    if sound_enabled:
        try:
            pygame.mixer.music.play(-1)
        except:
            pass

# Main game loop
def main():
    global player_velocity_y, score, game_over, boost_jumps, on_ground, visited_platforms, player_pos, particles
    global show_sound_status, sound_status_timer, sound_enabled, game_started
    global max_height, platforms_landed, boost_jumps_used, game_time
    
    running = True
    frame_count = 0
    create_platforms()
    
    while running:
        frame_count += 1
        
        # Update game time every second if game is active
        if game_started and not game_over and frame_count % FPS == 0:
            game_time += 1
        
        # Event handling
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                
            if event.type == pygame.KEYDOWN:
                if game_started:
                    if event.key == pygame.K_r and game_over:
                        restart_game()
                    if event.key == pygame.K_SPACE and not game_over and boost_jumps > 0 and not on_ground:
                        player_velocity_y = -JUMP_POWER
                        boost_jumps -= 1
                        boost_jumps_used += 1
                        particles.extend([Particle(player_pos[0], player_pos[1] + player_radius) for _ in range(20)])
                        play_sound(boost_sound)
                    if event.key == pygame.K_m:
                        sound_enabled = not sound_enabled
                        show_sound_status, sound_status_timer = True, 180
                        try:
                            pygame.mixer.music.play(-1) if sound_enabled else pygame.mixer.music.stop()
                        except:
                            pass
            
            # Check for mouse clicks
            if event.type == pygame.MOUSEBUTTONDOWN and not game_started:
                start_btn_rect, sound_btn_rect = draw_start_dashboard()
                if start_btn_rect.collidepoint(event.pos):
                    start_game()
                elif sound_btn_rect.collidepoint(event.pos):
                    sound_enabled = not sound_enabled
                    try:
                        pygame.mixer.music.play(-1) if sound_enabled else pygame.mixer.music.stop()
                    except:
                        pass
        
        # Update background
        screen.blit(background, (0, 0))
        
        if not game_started:
            # Draw start dashboard
            draw_start_dashboard()
        else:
            # Game is active
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
                
                # Update max height
                current_height = HEIGHT - player_pos[1]
                max_height = max(max_height, current_height)
                
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
                                platforms_landed += 1
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
            
            # Update particles
            for particle in particles[:]:
                particle.update()
                if particle.lifetime <= 0:
                    particles.remove(particle)
            
            # Draw particles behind player
            for particle in particles:
                particle.draw(screen)
            
            # Draw platforms with a single dark blue color
            for platform in platforms:
                pygame.draw.rect(screen, DARKER_BLUE_PLATFORM, platform)
                pygame.draw.line(screen, BLUE_HIGHLIGHT, (platform.left, platform.top), (platform.right, platform.top), 2)
            
            # Draw player as a ball
            pygame.draw.circle(screen, RED, (int(player_pos[0]), int(player_pos[1])), player_radius)
            pygame.draw.circle(screen, (255, 200, 200), (int(player_pos[0] - player_radius * 0.3), int(player_pos[1] - player_radius * 0.3)), int(player_radius * 0.25))
            
            # Draw score and boost jumps
            screen.blit(font.render(f"Score: {score}", True, WHITE), (10, 10))
            screen.blit(font.render("Boosts:", True, WHITE), (WIDTH - 180, 20))
            
            # Draw boost indicators
            for i in range(boost_jumps):
                boost_x, boost_y = WIDTH - 30 - i*25, 20
                pygame.draw.circle(screen, (255, 200, 100), (boost_x + 10, boost_y + 10), 12)  # Outer glow
                pygame.draw.circle(screen, ORANGE, (boost_x + 10, boost_y + 10), 8)  # Inner core
                pygame.draw.circle(screen, (255, 255, 200), (boost_x + 7, boost_y + 7), 3)  # Shine
            
            # Show sound status when toggled
            if show_sound_status:
                status = "ON" if sound_enabled else "OFF"
                screen.blit(font.render(f"Sound: {status}", True, WHITE), (WIDTH // 2 - 50, HEIGHT - 40))
                sound_status_timer -= 1
                if sound_status_timer <= 0:
                    show_sound_status = False
            
            # Draw game over screen
            if game_over:
                # Define how much to move everything up
                y_offset_adjustment = 100
                
                # Semi-transparent overlay
                overlay = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
                overlay.fill((0, 0, 0, 128))
                screen.blit(overlay, (0, 0))
                
                # Game over text and stats
                screen.blit(font.render("GAME OVER! Press R to restart", True, WHITE), 
                           (WIDTH // 2 - 180, HEIGHT // 2 - y_offset_adjustment))
                screen.blit(font.render(f"Final Score: {score}", True, WHITE), 
                           (WIDTH // 2 - 80, HEIGHT // 2 + 40 - y_offset_adjustment))
                screen.blit(font.render("Final Stats:", True, YELLOW), 
                           (WIDTH // 2 - 60, HEIGHT // 2 + 80 - y_offset_adjustment))
                
                stats = [
                    f"Maximum Height: {max_height} units",
                    f"Platforms Landed: {platforms_landed}",
                    f"Boost Jumps Used: {boost_jumps_used}",
                    f"Game Time: {game_time // 60}:{game_time % 60:02d}"
                ]
                
                y_offset = HEIGHT // 2 + 120 - y_offset_adjustment
                for stat in stats:
                    screen.blit(small_font.render(stat, True, WHITE), (WIDTH // 2 - 100, y_offset))
                    y_offset += 25
                
                # Draw return to menu button
                menu_btn = pygame.Rect(WIDTH // 2 - 100, y_offset + 20, 200, 40)
                is_hovering = draw_button(screen, "Return to Menu", menu_btn, BLUE, (100, 100, 255))
                
                # Check for menu button click
                if event.type == pygame.MOUSEBUTTONDOWN and menu_btn.collidepoint(event.pos):
                    game_started = False
                    game_over = False
        
        pygame.display.flip()
        clock.tick(FPS)
    
    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()
