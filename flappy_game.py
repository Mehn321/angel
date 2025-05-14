import pygame
import random

pygame.init()
WIDTH = 400
HEIGHT = 600
GRAVITY = 0.25
JUMP_STRENGTH = -7
PIPE_SPEED = 3
PIPE_GAP = 150

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Flappy Game")
clock = pygame.time.Clock()

# Colors
SKY_BLUE = (135, 206, 235)
GREEN = (0, 255, 0)
YELLOW = (255, 255, 0)
WHITE = (255, 255, 255)

class Bird:
    def __init__(self):
        self.x = WIDTH // 3
        self.y = HEIGHT // 2
        self.velocity = 0
        self.size = 30
        
    def jump(self):
        self.velocity = JUMP_STRENGTH
        
    def update(self):
        self.velocity += GRAVITY
        self.y += self.velocity
        
    def draw(self):
        pygame.draw.circle(screen, YELLOW, (self.x, int(self.y)), self.size)

class Pipe:
    def __init__(self):
        self.gap_y = random.randint(150, HEIGHT - 150)
        self.x = WIDTH
        self.width = 50
        
    def update(self):
        self.x -= PIPE_SPEED
        
    def draw(self):
        pygame.draw.rect(screen, GREEN, (self.x, 0, self.width, self.gap_y - PIPE_GAP//2))
        pygame.draw.rect(screen, GREEN, (self.x, self.gap_y + PIPE_GAP//2, self.width, HEIGHT))
        
    def collides_with(self, bird):
        bird_rect = pygame.Rect(bird.x - bird.size, bird.y - bird.size, bird.size * 2, bird.size * 2)
        top_pipe = pygame.Rect(self.x, 0, self.width, self.gap_y - PIPE_GAP//2)
        bottom_pipe = pygame.Rect(self.x, self.gap_y + PIPE_GAP//2, self.width, HEIGHT)
        return bird_rect.colliderect(top_pipe) or bird_rect.colliderect(bottom_pipe)


def main():
    bird = Bird()
    pipes = [Pipe()]
    score = 0
    game_started = False
    
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    if not game_started:
                        game_started = True
                    bird.jump()
        
        if game_started:
            bird.update()
            
            if pipes[-1].x < WIDTH - 200:
                pipes.append(Pipe())
            
            for pipe in pipes:
                pipe.update()
                if pipe.collides_with(bird):
                    running = False
                    
            pipes = [pipe for pipe in pipes if pipe.x > -pipe.width]
            
            for pipe in pipes:
                if pipe.x + pipe.width == bird.x:
                    score += 1
        
        # Draw everything
        screen.fill(SKY_BLUE)
        bird.draw()
        for pipe in pipes:
            pipe.draw()
            
        # Display score
        font = pygame.font.Font(None, 36)
        score_text = font.render(str(score), True, WHITE)
        screen.blit(score_text, (WIDTH//2, 50))
        
        # Show start message if game hasn't started
        if not game_started:
            font = pygame.font.Font(None, 48)
            text = font.render("Press SPACE to Start", True, WHITE)
            text_rect = text.get_rect(center=(WIDTH//2, HEIGHT//2))
            screen.blit(text, text_rect)
        
        pygame.display.flip()
        clock.tick(60)
    
    print("Final Score: " +str(score))
    pygame.quit()

if __name__ == "__main__":
    main()