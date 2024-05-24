import pygame
import random
import math
import sys

pygame.init()

screen_size = 400
cell_size = screen_size // 4
screen = pygame.display.set_mode((screen_size, screen_size + 40))
pygame.display.set_caption('2048')

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (200, 200, 200)
GREEN = (0, 255, 0)
ORANGE = (255, 165, 0)

font = pygame.font.SysFont(None, 36)

board = [[0 for _ in range(4)] for _ in range(4)]

def add_random_tile():
    empty_cells = [(i, j) for i in range(4) for j in range(4) if board[i][j] == 0]
    if empty_cells:
        i, j = random.choice(empty_cells)
        board[i][j] = 2 if random.random() < 0.9 else 4

def draw_board():
    screen.fill(WHITE)
    for i in range(4):
        for j in range(4):
            color = get_tile_color(board[i][j])
            pygame.draw.rect(screen, color, (j * cell_size, i * cell_size, cell_size, cell_size), border_radius=10)
            if board[i][j] != 0:
                text = font.render(str(board[i][j]), True, BLACK)
                text_rect = text.get_rect(center=(j * cell_size + cell_size // 2, i * cell_size + cell_size // 2))
                screen.blit(text, text_rect)
    pygame.display.flip()

def get_tile_color(value):
    if value == 0:
        return GRAY
    shade = min(255, int(255 - math.log2(value) * 40))
    return (255, shade, 0)

def is_game_over():
    for i in range(4):
        for j in range(4):
            if board[i][j] == 0:
                return False
            if i < 3 and board[i][j] == board[i + 1][j]:
                return False
            if j < 3 and board[i][j] == board[i][j + 1]:
                return False
    return True

def is_game_won():
    for i in range(4):
        for j in range(4):
            if board[i][j] == 2048:
                return True
    return False

def merge_tiles(row):
    merged_row = []
    i = 0
    while i < len(row):
        if i < len(row) - 1 and row[i] == row[i + 1]:
            merged_row.append(row[i] * 2)
            i += 2
        else:
            merged_row.append(row[i])
            i += 1
    merged_row.extend([0] * (4 - len(merged_row)))
    return merged_row

def transpose_board():
    return [list(row) for row in zip(*board)]

def swipe_left():
    moved = False
    for i in range(4):
        new_row = [tile for tile in board[i] if tile != 0]
        new_row = merge_tiles(new_row)
        new_row.extend([0] * (4 - len(new_row)))
        if new_row != board[i]:
            moved = True
            board[i] = new_row
    return moved

def swipe_right():
    moved = False
    for i in range(4):
        new_row = [tile for tile in board[i] if tile != 0]
        new_row = merge_tiles(new_row[::-1])[::-1]
        new_row = [0] * (4 - len(new_row)) + new_row
        if new_row != board[i]:
            moved = True
            board[i] = new_row
    return moved

def swipe_up():
    moved = False
    transposed_board = transpose_board()
    for i in range(4):
        new_row = [tile for tile in transposed_board[i] if tile != 0]
        new_row = merge_tiles(new_row)
        new_row.extend([0] * (4 - len(new_row)))
        if new_row != transposed_board[i]:
            moved = True
            transposed_board[i] = new_row
    if moved:
        for i in range(4):
            for j in range(4):
                board[j][i] = transposed_board[i][j]
    return moved

def swipe_down():
    moved = False
    transposed_board = transpose_board()
    for i in range(4):
        new_row = [tile for tile in transposed_board[i] if tile != 0]
        new_row = merge_tiles(new_row[::-1])[::-1]
        new_row = [0] * (4 - len(new_row)) + new_row
        if new_row != transposed_board[i]:
            moved = True
            transposed_board[i] = new_row
    if moved:
        for i in range(4):
            for j in range(4):
                board[j][i] = transposed_board[i][j]
    return moved

def evaluate_board(board):
    max_tile = max(max(row) for row in board)
    return math.log2(max_tile) if max_tile > 0 else 0

def alpha_beta(board, depth, alpha, beta, max_player):
    if depth == 0 or is_game_over():
        return evaluate_board(board)
    if max_player:
        value = -math.inf
        for move in ["left", "right", "up", "down"]:
            new_board = [row[:] for row in board]
            if make_move(new_board, move):
                value = max(value, alpha_beta(new_board, depth - 1, alpha, beta, False))
                alpha = max(alpha, value)
                if beta <= alpha:
                    break
        return value
    else:
        value = math.inf
        empty_cells = [(i, j) for i in range(4) for j in range(4) if board[i][j] == 0]
        for cell in empty_cells:
            for tile in [2, 4]:
                board[cell[0]][cell[1]] = tile
                value = min(value, alpha_beta(board, depth - 1, alpha, beta, True))
                board[cell[0]][cell[1]] = 0
                beta = min(beta, value)
                if beta <= alpha:
                    break
        return value

def get_best_move(board, depth):
    best_move = None
    best_value = -math.inf
    for move in ["left", "right", "up", "down"]:
        new_board = [row[:] for row in board]
        if make_move(new_board, move):
            value = alpha_beta(new_board, depth - 1, -math.inf, math.inf, False)
            if value > best_value:
                best_value = value
                best_move = move
    return best_move

def make_move(board, move):
    if move == "left":
        return swipe_left()
    elif move == "right":
        return swipe_right()
    elif move == "up":
        return swipe_up()
    elif move == "down":
        return swipe_down()
    return False

def display_end_message(message):
    strip_height = 40
    strip_rect = pygame.Rect(0, screen_size, screen_size, strip_height)
    pygame.draw.rect(screen, WHITE, strip_rect)
    text = font.render(message, True, BLACK)
    text_rect = text.get_rect(center=(screen_size // 2, screen_size + strip_height // 2))
    screen.blit(text, text_rect)
    pygame.display.flip()

def main():
    add_random_tile()
    add_random_tile()
    draw_board()
    autoplay = False
    clock = pygame.time.Clock()
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_s:
                    autoplay = not autoplay
                if not autoplay:
                    moved = False
                    if event.key == pygame.K_LEFT:
                        moved = swipe_left()
                    elif event.key == pygame.K_RIGHT:
                        moved = swipe_right()
                    elif event.key == pygame.K_UP:
                        moved = swipe_up()
                    elif event.key == pygame.K_DOWN:
                        moved = swipe_down()
                    if moved:
                        add_random_tile()
                        draw_board()
        if autoplay and not is_game_over() and not is_game_won():
            best_move = get_best_move(board, 3)
            if best_move:
                make_move(board, best_move)
                add_random_tile()
                draw_board()
                pygame.time.wait(1000)
        if is_game_over():
            display_end_message("Game Over")
        elif is_game_won():
            display_end_message("You won!")
        clock.tick(60)

if __name__ == "__main__":
    main()

