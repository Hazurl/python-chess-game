import sys
import pygame
import math
from collections import namedtuple
from board import Board, Side, PieceType, Piece
from dragger import Dragger

SIZE = WIDTH, HEIGHT = 640, 640
ROW_PX = math.floor(HEIGHT / 8)
COLUMN_PX = math.floor(WIDTH / 8)

CLEAR_COLOR = 20, 20, 20

SCREEN = pygame.display.set_mode(SIZE)

PIECES_SPRITE = pygame.image.load("assets/sprites/pieces.png")
PIECES_SPRITE = pygame.transform.scale(PIECES_SPRITE, (500, 167))

BOARD = [
    ["br", "bn", "bb", "bq", "bk", "bb", "bn", "br"],
    ["bp", "bp", "bp", "bp", "bp", "bp", "bp", "bp"],
    ["", "", "", "", "", "", "", ""],
    ["", "", "", "", "", "", "", ""],
    ["", "", "", "", "", "", "", ""],
    ["", "", "", "", "", "", "", ""],
    ["wp", "wp", "wp", "wp", "wp", "wp", "wp", "wp"],
    ["wr", "wn", "wb", "wq", "wk", "wb", "wn", "wr"]
]

PIECES_RECT = {
    "wk" : pygame.Rect(2 + 83 * 0, 3, 75, 75),
    "wq" : pygame.Rect(2 + 83 * 1, 3, 75, 75),
    "wb" : pygame.Rect(2 + 83 * 2, 3, 75, 75),
    "wn" : pygame.Rect(2 + 83 * 3, 3, 75, 75),
    "wr" : pygame.Rect(2 + 83 * 4, 3, 75, 75),
    "wp" : pygame.Rect(2 + 83 * 5, 3, 75, 75),

    "bk" : pygame.Rect(2 + 83 * 0, 86, 75, 75),
    "bq" : pygame.Rect(2 + 83 * 1, 86, 75, 75),
    "bb" : pygame.Rect(2 + 83 * 2, 86, 75, 75),
    "bn" : pygame.Rect(2 + 83 * 3, 86, 75, 75),
    "br" : pygame.Rect(2 + 83 * 4, 86, 75, 75),
    "bp" : pygame.Rect(2 + 83 * 5, 86, 75, 75)
}

def board_at(x, y):
    return BOARD[y][x]

def set_piece_at(x, y, ptype, side):
    BOARD[y][x] = side_to_str(side) + ptype

def remove_at(x, y):
    BOARD[y][x] = ""

def is_empty(x, y):
    return board_at(x, y) == ""

def side_to_str(side):
    if side == -1:
        return "b"
    else:
        return "w"

def get_side_of(piece):
    if len(piece) == 0:
        return 0
    elif piece[0] == "b":
        return -1
    else:
        return 1

def is_side(side, x, y):
    return get_side_of(board_at(x, y)) == side

def get_type_of(piece):
    if len(piece) == 0:
        return ""
    return piece[1]

def position_to_screen(position):
    x, y = position
    return (x * COLUMN_PX, y * ROW_PX)

def draw_pieces():
    for x in range(8):
        for y in range(8):
            name = board_at(x, y)
            if name != "":
                SCREEN.blit(PIECES_SPRITE, position_to_screen((x, y)), PIECES_RECT[name])

def draw_board():
    is_white = True
    white_color = (220, 193, 147)
    black_color = (80, 42, 1)
    for x in range(0, WIDTH, COLUMN_PX):
        for y in range(0, HEIGHT, ROW_PX):
            if is_white:
                pygame.draw.rect(SCREEN, white_color, (x, y, COLUMN_PX, ROW_PX))
            else:
                pygame.draw.rect(SCREEN, black_color, (x, y, COLUMN_PX, ROW_PX))
            is_white = not is_white
        is_white = not is_white

def is_king_in_check(side, nx, ny):
    for x in range(8):
        for y in range(8):
            piece = board_at(x, y)
            if not is_empty(x, y) and get_side_of(piece) != side:
                if x != nx and y != ny and valid_movement(board_at(x, y), (x, y), (nx, ny)):
                    return False
    return True

def closed_interval(a, b):
    a, b = (b + 1, a) if a > b else (a + 1, b)
    return range(a, b)

def valid_move_rook(side, px, py, nx, ny):
    if px != nx and py != ny:
        return False

    for x in closed_interval(px, nx):
        if not is_empty(x, ny):
            return False

    for y in closed_interval(py, ny):
        if not is_empty(nx, y):
            return False
    return not is_side(side, nx, ny)

def valid_move_knight(side, px, py, nx, ny):
    if is_side(side, nx, ny):
        return False

    ax = abs(px - nx)
    ay = abs(py - ny)
    return (ax == 2 and ay == 1) or (ax == 1 and ay == 2)

def valid_move_bishop(side, px, py, nx, ny):
    if abs(px - nx) != abs(py - ny):
        return False

    for x, y in zip(closed_interval(px, nx), closed_interval(py, ny)):
        if not is_empty(x, y):
            return False
    return not is_side(side, nx, ny)

def valid_move_queen(side, px, py, nx, ny):
    ax = abs(px - nx)
    ay = abs(py - ny)

    if ax == 0 or ay == 0:
        return valid_move_rook(side, px, py, nx, ny)
    elif ax == ay:
        return valid_move_bishop(side, px, py, nx, ny)
    else:
        return False

def valid_move_king(side, px, py, nx, ny):
    if is_king_in_check(side, nx, ny):
        return False
    return not is_side(side, nx, ny) and abs(px - nx) <= 1 and abs(py - ny) <= 1

def valid_move_pawn(side, px, py, nx, ny):
    if abs(px - nx) > 1:
        return False
    if side == -1: # black, down
        if abs(px - nx) == 1: # side move eat
            return ny - py == 1 and is_side(-side, nx, ny)
        else:
            return is_empty(nx, ny) and ((ny - py) == 1 or (py == 1 and ny == 3))
    else:
        if abs(px - nx) == 1: # side move eat
            return ny - py == -1 and is_side(-side, nx, ny)
        else:
            return is_empty(nx, ny) and ((ny - py) == -1 or (py == 6 and ny == 4))

def valid_movement(piece, prev_pos, next_pos):
    px, py = prev_pos
    nx, ny = next_pos

    if px == nx and py == ny:
        return False

    piece_type = get_type_of(piece)
    piece_side = get_side_of(piece)

    return {
        "r" : valid_move_rook,
        "n" : valid_move_knight,
        "b" : valid_move_bishop,
        "q" : valid_move_queen,
        "k" : valid_move_king,
        "p" : valid_move_pawn
    }[piece_type](piece_side, px, py, nx, ny)


def startDrag(player_turn):
    mouse_x, mouse_y = pygame.mouse.get_pos()
    cell = cell_x, cell_y = math.floor(mouse_x / COLUMN_PX), math.floor(mouse_y / ROW_PX)
    if is_side(player_turn, cell_x, cell_y):
        piece = board_at(cell_x, cell_y)
        remove_at(cell_x, cell_y)
        return piece, cell
    return None

def endDrag(drag):
    name, prev_pos = drag
    x, y = prev_pos

    mouse_x, mouse_y = pygame.mouse.get_pos()
    cell_x, cell_y = math.floor(mouse_x / COLUMN_PX), math.floor(mouse_y / ROW_PX)

    if valid_movement(name, prev_pos, (cell_x, cell_y)):
        set_piece_at(cell_x, cell_y, get_type_of(name), get_side_of(name))
        return True
    else:
        set_piece_at(x, y, get_type_of(name), get_side_of(name))
        return False

def draw_cell_valid(piece, x, y):
    for nx in range(8):
        for ny in range(8):
            if valid_movement(piece, (x, y), (nx, ny)):
                sx, sy = position_to_screen((nx, ny))
                cell = pygame.Surface((COLUMN_PX, ROW_PX))
                cell.set_alpha(100)
                cell.fill((0, 255, 0))
                SCREEN.blit(cell, position_to_screen((nx, ny)))

def draw_dragged_piece(drag):
    mouse_x, mouse_y = pygame.mouse.get_pos()
    name, pos = drag
    rect = PIECES_RECT[name]
    SCREEN.blit(PIECES_SPRITE, (mouse_x - rect.width / 2, mouse_y - rect.height / 2), rect)
    x, y = pos
    draw_cell_valid(name, x, y)

if __name__ == '__main__':
    pygame.init()

    drag = None
    player_turn = 1 # white
    board = Board()
    valid_cells_dragged_piece = None

    while 1:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                x, y = pygame.mouse.get_pos()
                x, y = x // COLUMN_PX, y // ROW_PX
                piece = board.get_piece(x, y)
                if piece is not None:
                    board.set_dragged_piece(x, y)
                    valid_cells_dragged_piece = board.get_valid_cells((x, y))
                    drag = Dragger(piece, (x, y))
            if event.type == pygame.MOUSEBUTTONUP and drag is not None:
                board.reset_dragged_piece()
                valid_cells_dragged_piece = None
                x, y = pygame.mouse.get_pos()
                x, y = x // COLUMN_PX, y // ROW_PX
                board.move_piece((drag.prev_x, drag.prev_y), (x, y))
                drag = None

        SCREEN.fill(CLEAR_COLOR)

        board.draw(SCREEN)

        if valid_cells_dragged_piece is not None:
            for cell in valid_cells_dragged_piece:
                x, y = cell
                sx, sy = position_to_screen((x, y))
                cell = pygame.Surface((COLUMN_PX, ROW_PX))
                cell.set_alpha(100)
                cell.fill((0, 255, 0))
                SCREEN.blit(cell, (sx, sy))

        if drag is not None:
            drag.draw(SCREEN)

        pygame.display.flip()
