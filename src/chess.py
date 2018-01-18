import sys, pygame, math
from collections import namedtuple

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
    ["wp", "wp", "wp", "", "wp", "wp", "wp", "wp"],
    ["wr", "wn", "wb", "wq", "wk", "wb", "wn", "wr"]
]

PIECES_RECT = {
    "wk" :   (2 + 83 * 0, 3, 75, 75),
    "wq" :  (2 + 83 * 1, 3, 75, 75),
    "wb" : (2 + 83 * 2, 3, 75, 75),
    "wn" : (2 + 83 * 3, 3, 75, 75),
    "wr" :   (2 + 83 * 4, 3, 75, 75),
    "wp" :   (2 + 83 * 5, 3, 75, 75),

    "bk" :   (2 + 83 * 0, 86, 75, 75),
    "bq" :  (2 + 83 * 1, 86, 75, 75),
    "bb" : (2 + 83 * 2, 86, 75, 75),
    "bn" : (2 + 83 * 3, 86, 75, 75),
    "br" :   (2 + 83 * 4, 86, 75, 75),
    "bp" :   (2 + 83 * 5, 86, 75, 75)
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

def valid_move_rook(side, px, py, nx, ny):
    if px != nx and py != ny:
        return False

    if px != nx:
        for x in range(px, nx, -1 if px > nx else 1):
            if not is_empty(x, ny):
                return False
        return not is_side(side, nx, ny)

    else:
        for y in range(py, ny, -1 if py > ny else 1):
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

    rangex = range(px, nx, -1 if px > nx else 1)
    rangey = range(py, ny, -1 if py > ny else 1)
    for x, y in zip(rangex, rangey):
        if not is_empty(x, y):
            return False
    return not is_side(side, nx, ny)

def valid_move_queen(side, px, py, nx, ny):
    ax = abs(px - nx)
    ay = abs(py - ny)
    if ax != ay and ax != 0 and ay != 0:  
        return False

    if ax == 0 or ay == 0:
        return valid_move_rook(side, px, py, nx, ny)
    else:
        return valid_move_bishop(side, px, py, nx, ny)

def valid_move_king(side, px, py, nx, ny):
    # TODO : check for check
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


def startDrag():
    mouse_x, mouse_y = pygame.mouse.get_pos()
    cell = cell_x, cell_y = math.floor(mouse_x / COLUMN_PX), math.floor(mouse_y / ROW_PX)
    if not is_empty(cell_x, cell_y):
        piece = board_at(cell_x, cell_y)
        remove_at(cell_x, cell_y)
        return piece, cell, ((cell_x * COLUMN_PX - mouse_x), (cell_y * ROW_PX - mouse_y))
    return None

def endDrag(drag):
    name, prev_pos, _ = drag
    x, y = prev_pos

    mouse_x, mouse_y = pygame.mouse.get_pos()
    cell_x, cell_y = math.floor(mouse_x / COLUMN_PX), math.floor(mouse_y / ROW_PX)

    if valid_movement(name, prev_pos, (cell_x, cell_y)):
        set_piece_at(cell_x, cell_y, get_type_of(name), get_side_of(name))
    else:
        set_piece_at(x, y, get_type_of(name), get_side_of(name))

def draw_cell_valid(piece, x, y):
    for nx in range(8):
        for ny in range(8):
            if valid_movement(piece, (x, y), (nx, ny)):
                sx, sy = position_to_screen((nx, ny))
                cell = pygame.Surface((COLUMN_PX, ROW_PX))
                cell.set_alpha(100)
                cell.fill((0,255,0))
                SCREEN.blit(cell, position_to_screen((nx, ny)))

def draw_dragged_piece(drag):
    mouse_x, mouse_y = pygame.mouse.get_pos()
    name, pos, offset = drag
    off_x, off_y = offset
    SCREEN.blit(PIECES_SPRITE, (mouse_x + off_x, mouse_y + off_y), PIECES_RECT[name])
    x, y = pos
    draw_cell_valid(name, x, y)

if __name__ == '__main__':
    pygame.init()

    on_drag = None

    while 1:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                on_drag = startDrag()
            if event.type == pygame.MOUSEBUTTONUP and on_drag is not None:
                endDrag(on_drag)
                on_drag = None

        SCREEN.fill(CLEAR_COLOR)

        draw_board()

        draw_pieces()

        if on_drag is not None:
            draw_dragged_piece(on_drag)

        pygame.display.flip()
