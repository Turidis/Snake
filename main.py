import pygame
from random import randrange
from collections import deque

RES = 800
SIZE = 50
MOVE_DELAY = 120
FPS = 60

COLOR_BG = pygame.Color("black")
COLOR_SNAKE = pygame.Color("blue")
COLOR_APPLE = pygame.Color("white")
COLOR_SCORE = pygame.Color("silver")
COLOR_GAME_OVER = pygame.Color("red")



def spawn_apple(snake_set):
    """Spawn an apple NOT inside the snake."""
    while True:
        pos = (
            randrange(0, RES, SIZE),
            randrange(0, RES, SIZE),
        )
        if pos not in snake_set:
            return pos


def is_opposite(dir1, dir2):
    """Prevent turning 180 degrees."""
    return dir1[0] == -dir2[0] and dir1[1] == -dir2[1]


def main():
    pygame.init()
    surface = pygame.display.set_mode((RES, RES))
    clock = pygame.time.Clock()
    font_score = pygame.font.SysFont("Arial", 26, bold=True)
    font_end = pygame.font.SysFont("Arial", 66, bold=True)
    img = pygame.image.load('snake.jpg').convert()
        
    def reset_game():
        x = randrange(0, RES, SIZE)
        y = randrange(0, RES, SIZE)
        snake = deque([(x, y)])
        snake_set = {(x, y)}
        apple = spawn_apple(snake_set)
        direction = (0, 0)
        score = 0
        last_move_time = pygame.time.get_ticks()
        return snake, snake_set, apple, direction, score, last_move_time

    snake, snake_set, apple, direction, score, last_move_time = reset_game()
    game_over = False

    while True:
        surface.blit(img, (0, 0))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                exit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    exit()

                if game_over:

                    if event.key == pygame.K_r:
                        snake, snake_set, apple, direction, score, last_move_time = reset_game()
                        game_over = False
                    continue

                if event.key == pygame.K_w:
                    new_dir = (0, -1)
                elif event.key == pygame.K_s:
                    new_dir = (0, 1)
                elif event.key == pygame.K_a:
                    new_dir = (-1, 0)
                elif event.key == pygame.K_d:
                    new_dir = (1, 0)
                else:
                    new_dir = direction

                if not is_opposite(direction, new_dir):
                    direction = new_dir

        if game_over:
            text = font_end.render("GAME OVER", True, COLOR_GAME_OVER)
            surface.blit(text, (RES // 2 - 200, RES // 3))
            sub = font_score.render("Press R to restart", True, COLOR_SCORE)
            surface.blit(sub, (RES // 2 - 140, RES // 2))
            pygame.display.flip()
            clock.tick(FPS)
            continue

        now = pygame.time.get_ticks()
        if direction != (0, 0) and now - last_move_time > MOVE_DELAY:
            last_move_time = now

            x, y = snake[-1]
            dx, dy = direction
            x += dx * SIZE
            y += dy * SIZE

            if x < 0 or x >= RES or y < 0 or y >= RES:
                game_over = True
                continue

            new_head = (x, y)


            if new_head in snake_set:
                game_over = True
                continue


            snake.append(new_head)
            snake_set.add(new_head)


            if new_head == apple:
                score += 1
                apple = spawn_apple(snake_set)
            else:

                tail = snake.popleft()
                snake_set.remove(tail)
                
        for pos in snake:
            pygame.draw.rect(surface, COLOR_SNAKE, (*pos, SIZE - 1, SIZE - 1))

        pygame.draw.rect(surface, COLOR_APPLE, (*apple, SIZE, SIZE))

        text = font_score.render(f"Score: {score}", True, COLOR_SCORE)
        surface.blit(text, (5, 5))

        pygame.display.flip()
        clock.tick(FPS)

if __name__ == "__main__":
    main()
