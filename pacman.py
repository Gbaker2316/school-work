import pygame
import random
import os
import sys

# Initialize pygame
pygame.init()

# Constants
WIDTH, HEIGHT = 600, 600
GRID_SIZE = 30  # Each cell in the grid is 30x30 pixels
ROWS, COLS = HEIGHT // GRID_SIZE, WIDTH // GRID_SIZE
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
YELLOW = (255, 255, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)

# Maze grid (1 = Wall, 0 = Empty path, 2 = Pellet, 3 = Ghost, 4 = Pac-Man)
# Where ever a ghost start position is, it will be replaced with a 0 in the maze grid. The ghost will be drawn on top of the maze grid.
maze = [
    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
    [1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 3, 1, 1, 1, 1, 1, 1, 1, 1, 1],
    [1, 1, 4, 0, 0, 0, 0, 0, 0, 2, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1],    
    [1, 1, 0, 1, 1, 1, 1, 1, 1, 0, 1, 1, 1, 1, 1, 1, 1, 0, 1, 1],
    [1, 1, 0, 1, 1, 1, 1, 1, 1, 0, 1, 1, 1, 1, 1, 1, 1, 0, 1, 1],
    [1, 1, 0, 1, 1, 1, 1, 1, 0, 0, 0, 1, 1, 1, 1, 1, 1, 0, 1, 1],
    [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2, 0, 1],
    [1, 0, 1, 1, 1, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 1, 1, 0, 1],
    [1, 0, 1, 3, 1, 0, 1, 0, 0, 0, 0, 0, 1, 3, 1, 0, 1, 0, 0, 1],
    [1, 2, 0, 0, 0, 0, 0, 0, 0, 2, 0, 0, 0, 0, 0, 0, 0, 2, 0, 1],
    [1, 0, 1, 3, 1, 0, 1, 0, 0, 0, 0, 0, 1, 3, 1, 0, 1, 0, 0, 1],
    [1, 0, 1, 1, 1, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 1, 1, 0, 1],
    [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
    [1, 1, 0, 1, 1, 1, 1, 1, 1, 0, 1, 1, 1, 1, 1, 1, 1, 0, 1, 1],
    [1, 1, 0, 1, 1, 1, 1, 1, 1, 0, 1, 1, 1, 1, 1, 1, 1, 0, 1, 1],
    [1, 1, 0, 1, 1, 1, 1, 1, 0, 0, 3, 1, 1, 1, 1, 1, 1, 0, 1, 1],
    [1, 1, 0, 0, 0, 0, 0, 0, 0, 2, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1],
    [1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1],
    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
]
# Randomizes maze after round 1.
def randomize_map():
    global maze, pacman_pos, ghost_positions

    # Preserve the current maze dimensions.
    rows, cols = len(maze), len(maze[0])
    ghost_count = len(ghost_positions)
    new_maze = [[1] * cols for _ in range(rows)]

    # Carve connected paths.
    new_maze[1][1] = 0
    stack = [(1, 1)]

    while stack:
        row, col = stack[-1]
        choices = []

        for dr, dc in [(0, 2), (0, -2), (2, 0), (-2, 0)]:
            nr, nc = row + dr, col + dc
            if 0 < nr < rows - 1 and 0 < nc < cols - 1:
                if new_maze[nr][nc] == 1:
                    choices.append((nr, nc))

        if choices:
            nr, nc = random.choice(choices)
            new_maze[(row + nr) // 2][(col + nc) // 2] = 0
            new_maze[nr][nc] = 0
            stack.append((nr, nc))
        else:
            stack.pop()

    # Add occasional openings for alternate routes.
    for row in range(1, rows - 1):
        for col in range(1, cols - 1):
            if new_maze[row][col] != 1:
                continue

            joins_paths = (
                new_maze[row - 1][col] == new_maze[row + 1][col] == 0
                or new_maze[row][col - 1] == new_maze[row][col + 1] == 0
            )

            if joins_paths and random.random() < 0.15:
                new_maze[row][col] = 0

    maze = new_maze

    # Place Pac-Man at the start.
    pacman_pos = [2, 2]
    maze[1][1] = 4

    # Place ghosts away from Pac-Man.
    ghost_spaces = [
        (row, col)
        for row in range(rows)
        for col in range(cols)
        if maze[row][col] == 0 and row + col >= 8
    ]

    ghost_positions = [
        list(position)
        for position in random.sample(
            ghost_spaces, min(ghost_count, len(ghost_spaces))
        )
    ]

    for row, col in ghost_positions:
        maze[row][col] = 3

    # Place five reachable pellets on empty paths.
    empty_spaces = [
        (row, col)
        for row in range(rows)
        for col in range(cols)
        if maze[row][col] == 0
    ]

    pellet_positions[:] = random.sample(empty_spaces, 5)

    for row, col in pellet_positions:
        maze[row][col] = 2
# Store pellet positions separately
pellet_positions = [(row_idx, col_idx) for row_idx, row in enumerate(maze) for col_idx, cell in enumerate(row) if cell == 2]

def display_message(screen, message, color=WHITE):
    font = pygame.font.Font(None, 50)
    text = font.render(message, True, color)
    text_rect = text.get_rect(center=(WIDTH // 2, HEIGHT // 2))
    screen.blit(text, text_rect)
    pygame.display.flip()
    pygame.time.delay(2000)

# Get Pac-Man & Ghost positions
def get_positions():
    pacman_pos = None
    ghost_positions = []
    for row_idx, row in enumerate(maze):
        for col_idx, cell in enumerate(row):
            if cell == 4:
                pacman_pos = [row_idx, col_idx]
            elif cell == 3:
                ghost_positions.append([row_idx, col_idx])
    return pacman_pos, ghost_positions

pacman_pos, ghost_positions = get_positions()
score = 0
lives = 3
def ask_play_again(screen, message):
    screen.fill(BLACK)
    font = pygame.font.Font(None, 40)

    for text, y in [
        (message, HEIGHT // 2 - 30),
        ("Play again? Y / N", HEIGHT // 2 + 30),
    ]:
        label = font.render(text, True, YELLOW)
        screen.blit(
            label, label.get_rect(center=(WIDTH // 2, y))
        )

    pygame.display.flip()

    while True:
        event = pygame.event.wait()

        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_y:
                pygame.quit()
                os.execl(
                    sys.executable,
                    sys.executable,
                    os.path.abspath(__file__),
                )
            elif event.key == pygame.K_n:
                pygame.quit()
                sys.exit()
def check_collision(screen):
    global lives, pacman_pos
    if pacman_pos not in ghost_positions:
        return

    lives -= 1
    if lives <= 0:
        ask_play_again(screen, "Game Over!")
        return

    display_message(screen, "You lost a life!", RED)

    # Keep the ghost visible on the collision tile.
    old_row, old_col = pacman_pos
    maze[old_row][old_col] = 3

    # Respawn at the start, or a free path if a ghost occupies it.
    spawn = [2, 2]
    if spawn in ghost_positions:
        spawn = next(
            [row, col]
            for row in range(len(maze))
            for col in range(len(maze[row]))
            if maze[row][col] == 0
            and [row, col] not in ghost_positions
        )
    pacman_pos = spawn
    maze[spawn[0]][spawn[1]] = 4

def draw_maze(screen):
    for row_idx, row in enumerate(maze):
        for col_idx, cell in enumerate(row):
            x, y = col_idx * GRID_SIZE, row_idx * GRID_SIZE
            if cell == 1:
                pygame.draw.rect(screen, BLUE, (x, y, GRID_SIZE, GRID_SIZE))
            elif cell == 2:
                pygame.draw.circle(screen, WHITE, (x + GRID_SIZE // 2, y + GRID_SIZE // 2), 5)
            elif cell == 3:
                pygame.draw.circle(screen, RED, (x + GRID_SIZE // 2, y + GRID_SIZE // 2), 12)
            elif cell == 4:
                pygame.draw.circle(screen, YELLOW, (x + GRID_SIZE // 2, y + GRID_SIZE // 2), 12)

def move_pacman(direction, screen):
    global pacman_pos, score
    row, col = pacman_pos
    new_row, new_col = row, col
    if direction == "UP":
        new_row -= 1
    elif direction == "DOWN":
        new_row += 1
    elif direction == "LEFT":
        new_col -= 1
    elif direction == "RIGHT":
        new_col += 1
    
    if maze[new_row][new_col] != 1:
        if (new_row, new_col) in pellet_positions:
            pellet_positions.remove((new_row, new_col))
            score += 5
        
        maze[row][col] = 0  # Clear old position
        maze[new_row][new_col] = 4  # Move Pac-Man
        pacman_pos = [new_row, new_col]
        
    check_collision(screen)


def move_ghosts(screen):
    directions = [(0, 1), (0, -1), (1, 0), (-1, 0)]
    for ghost in ghost_positions:
        row, col = ghost
        random.shuffle(directions)
        
        for dr, dc in directions:
            new_row, new_col = row + dr, col + dc
            
            if maze[new_row][new_col] in [0, 2]:
                maze[row][col] = 0  # Restore empty path
                if (row, col) in pellet_positions:
                    maze[row][col] = 2  # Restore pellet if ghost was on one
                
                ghost[0], ghost[1] = new_row, new_col
                maze[new_row][new_col] = 3  # Move ghost
                break
    check_collision(screen)

def main():
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Pac-Man (Beginner Version)")
    clock = pygame.time.Clock()
    last_ghost_move = pygame.time.get_ticks()
    ghost_move_delay = 333

    next_map_score = 25
    while True:
        screen.fill(BLACK)
        draw_maze(screen)
        font = pygame.font.Font(None, 36)
        score_text = font.render(f"Score: {score}", True, WHITE)
        lives_text = font.render(f"Lives: {lives}", True, WHITE)
        screen.blit(score_text, (10, 10))
        screen.blit(lives_text, (WIDTH - 100, 10))
        
        now = pygame.time.get_ticks()
        if now - last_ghost_move >= ghost_move_delay:
            move_ghosts(screen)
            last_ghost_move = now
        pygame.display.flip()
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    move_pacman("UP", screen)
                elif event.key == pygame.K_DOWN:
                    move_pacman("DOWN", screen)
                elif event.key == pygame.K_LEFT:
                    move_pacman("LEFT", screen)
                elif event.key == pygame.K_RIGHT:
                    move_pacman("RIGHT", screen)
        if score >= 100:
            ask_play_again(screen, "You Win!")
        if score >= next_map_score:
            randomize_map()
            next_map_score += 25
            last_ghost_move = pygame.time.get_ticks()
        if not pellet_positions:
            # Find empty paths, excluding Pac-Man and ghosts.
            empty_spaces = [
                (row, col)
                for row in range(len(maze))
                for col in range(len(maze[row]))
                if maze[row][col] == 0
                and [row, col] != pacman_pos
                and [row, col] not in ghost_positions
            ]

            # Spawn up to 10 new pellets.
            pellet_positions[:] = random.sample(
                empty_spaces, min(5, len(empty_spaces))
            )

            for row, col in pellet_positions:
                maze[row][col] = 2
        clock.tick(30)  # Slower ghost movementÍ
if __name__ == "__main__":
    main()