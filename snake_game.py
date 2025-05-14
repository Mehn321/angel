import pygame
import random

pygame.init()
WINDOW_SIZE = 1100
GRID_SIZE = 20
GRID_COUNT = WINDOW_SIZE // GRID_SIZE

screen = pygame.display.set_mode((WINDOW_SIZE, WINDOW_SIZE))
pygame.display.set_caption("Snake Game")
clock = pygame.time.Clock()

# Colors
BLACK = (0, 0, 0)
GREEN = (0, 255, 0)
RED = (255, 0, 0)

# Snake initial position and direction
snake = [(GRID_COUNT // 2, GRID_COUNT // 2)]
snake_dir = (1, 0)
food = (random.randint(0, GRID_COUNT-1), random.randint(0, GRID_COUNT-1))
score = 0

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP and snake_dir != (0, 1):
                snake_dir = (0, -1)
            if event.key == pygame.K_DOWN and snake_dir != (0, -1):
                snake_dir = (0, 1)
            if event.key == pygame.K_LEFT and snake_dir != (1, 0):
                snake_dir = (-1, 0)
            if event.key == pygame.K_RIGHT and snake_dir != (-1, 0):
                snake_dir = (1, 0)

    # Move snake with teleportation
    new_head = (
        (snake[0][0] + snake_dir[0]) % GRID_COUNT,
        (snake[0][1] + snake_dir[1]) % GRID_COUNT
    )
    snake.insert(0, new_head)

    # Check if snake ate food
    if snake[0] == food:
        score += 1
        food = (random.randint(0, GRID_COUNT-1), random.randint(0, GRID_COUNT-1))
        while food in snake:
            food = (random.randint(0, GRID_COUNT-1), random.randint(0, GRID_COUNT-1))
    else:
        snake.pop()

    # Check for self collision
    if snake[0] in snake[1:]:
        running = False

    # Draw everything
    screen.fill(BLACK)
    for segment in snake:
        pygame.draw.rect(screen, GREEN, (segment[0]*GRID_SIZE, segment[1]*GRID_SIZE, GRID_SIZE-2, GRID_SIZE-2))
    pygame.draw.rect(screen, RED, (food[0]*GRID_SIZE, food[1]*GRID_SIZE, GRID_SIZE-2, GRID_SIZE-2))
    
    pygame.display.flip()
    clock.tick(10)

pygame.quit()
print("Game Over! Score: "+str(score))
