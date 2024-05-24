import pygame
import random
import sys
import math

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

    for i in range(1, 4):
        pygame.draw.line(screen, BLACK, (i * cell_size, 0), (i * cell_size, screen_size))

    for i in range(1, 4):
        pygame.draw.line(screen, BLACK, (0, i * cell_size), (screen_size, i * cell_size))

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

def merge_tiles(row):
    merged_row = []
    skip = False
    for i in range(4):
        if skip:
            skip = False
            continue
        if i < 3 and row[i] == row[i + 1] and row[i] != 0:
            merged_row.append(row[i] * 2)
            skip = True
        else:
            merged_row.append(row[i])
    while len(merged_row) < 4:
        merged_row.append(0)
    return merged_row

def transpose_board(board):
    return [list(row) for row in zip(*board)]

def swipe_left():
    moved = False
    global board
    for i in range(4):
        new_row = [tile for tile in board[i] if tile != 0]
        while len(new_row) < 4:
            new_row.append(0)
        new_row = merge_tiles(new_row)
        if new_row != board[i]:
            moved = True
            board[i] = new_row
    return moved

def swipe_right():
    moved = False
    global board
    for i in range(4):
        new_row = [tile for tile in board[i] if tile != 0]
        while len(new_row) < 4:
            new_row.insert(0, 0)
        new_row = merge_tiles(new_row[::-1])[::-1]
        if new_row != board[i]:
            moved = True
            board[i] = new_row
    return moved

def swipe_up():
    moved = False
    global board
    transposed_board = transpose_board(board)
    for i in range(4):
        new_row = [tile for tile in transposed_board[i] if tile != 0]
        while len(new_row) < 4:
            new_row.append(0)
        new_row = merge_tiles(new_row)
        if new_row != transposed_board[i]:
            moved = True
            transposed_board[i] = new_row
    if moved:
        board = transpose_board(transposed_board)
    return moved

def swipe_down():
    moved = False
    global board
    transposed_board = transpose_board(board)
    for i in range(4):
        new_row = [tile for tile in transposed_board[i] if tile != 0]
        while len(new_row) < 4:
            new_row.insert(0, 0)
        new_row = merge_tiles(new_row[::-1])[::-1]
        if new_row != transposed_board[i]:
            moved = True
            transposed_board[i] = new_row
    if moved:
        board = transpose_board(transposed_board)
    return moved

def is_game_won():
    for i in range(4):
        for j in range(4):
            if board[i][j] == 2048:
                return True
    return False

def display_end_message(message):
    strip_height = 40
    strip_rect = pygame.Rect(0, screen_size, screen_size, strip_height)
    pygame.draw.rect(screen, WHITE, strip_rect)
    text = font.render(message, True, BLACK)
    text_rect = text.get_rect(center=(screen_size // 2, screen_size + strip_height // 2))
    screen.blit(text, text_rect)
    pygame.display.flip()

add_random_tile()
add_random_tile()
draw_board()
while not is_game_over():
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == pygame.KEYDOWN:
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

            if is_game_over():
                display_end_message("Game Over")
                pygame.quit()
                sys.exit()
            elif is_game_won():
                display_end_message("You won!")
                pygame.quit()
                sys.exit()
