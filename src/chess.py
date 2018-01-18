import sys, pygame, math
pygame.init()

SIZE = WIDTH, HEIGHT = 640, 640
ROW_PX = math.floor(HEIGHT / 8)
COLUMN_PX = math.floor(WIDTH / 8)
CLEAR_COLOR = 20, 20, 20

SCREEN = pygame.display.set_mode(SIZE)

PIECES_SPRITE = pygame.image.load("assets/sprites/pieces.png")
PIECES_SPRITE = pygame.transform.scale(PIECES_SPRITE, (500, 167))

PIECES_POSITION = [
    ("b_rook", 0, 0),
    ("b_knight", 1, 0),
    ("b_bishop", 2, 0),
    ("b_queen", 3, 0),
    ("b_king", 4, 0),
    ("b_bishop", 5, 0),
    ("b_knight", 6, 0),
    ("b_rook", 7, 0),

    ("b_pawn", 0, 1),
    ("b_pawn", 1, 1),
    ("b_pawn", 2, 1),
    ("b_pawn", 3, 1),
    ("b_pawn", 4, 1),
    ("b_pawn", 5, 1),
    ("b_pawn", 6, 1),
    ("b_pawn", 7, 1),

    ("w_rook", 0, 7),
    ("w_knight", 1, 7),
    ("w_bishop", 2, 7),
    ("w_queen", 3, 7),
    ("w_king", 4, 7),
    ("w_bishop", 5, 7),
    ("w_knight", 6, 7),
    ("w_rook", 7, 7),

    ("w_pawn", 0, 6),
    ("w_pawn", 1, 6),
    ("w_pawn", 2, 6),
    ("w_pawn", 3, 6),
    ("w_pawn", 4, 6),
    ("w_pawn", 5, 6),
    ("w_pawn", 6, 6),
    ("w_pawn", 7, 6)
]

PIECES_RECT = {
    "w_king" :   (2 + 83 * 0, 3, 75, 75),
    "w_queen" :  (2 + 83 * 1, 3, 75, 75),
    "w_bishop" : (2 + 83 * 2, 3, 75, 75),
    "w_knight" : (2 + 83 * 3, 3, 75, 75),
    "w_rook" :   (2 + 83 * 4, 3, 75, 75),
    "w_pawn" :   (2 + 83 * 5, 3, 75, 75),

    "b_king" :   (2 + 83 * 0, 86, 75, 75),
    "b_queen" :  (2 + 83 * 1, 86, 75, 75),
    "b_bishop" : (2 + 83 * 2, 86, 75, 75),
    "b_knight" : (2 + 83 * 3, 86, 75, 75),
    "b_rook" :   (2 + 83 * 4, 86, 75, 75),
    "b_pawn" :   (2 + 83 * 5, 86, 75, 75)
}

def position_to_screen(position):
    x, y = position
    return (x * COLUMN_PX, y * ROW_PX)

def draw_pieces():
    for piece in PIECES_POSITION:
        name, x, y = piece
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

while 1:
    for event in pygame.event.get():
        if event.type == pygame.QUIT: sys.exit()

    SCREEN.fill(CLEAR_COLOR)

    draw_board()

    draw_pieces()

    pygame.display.flip()
