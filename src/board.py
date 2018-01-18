from enum import Enum
import pygame

class PieceType(Enum):
    PAWN = 'P'
    KNIGHT = 'N'
    ROOK = 'R'
    BISHOP = 'B'
    QUEEN = 'Q'
    KING = 'K'

class Side(Enum):
    WHITE = 1
    NEUTRAL = 0
    BLACK = -1

class Piece(object):

    SPRITE = pygame.transform.scale(pygame.image.load("assets/sprites/pieces.png"), (500, 167))
    RECTS = {
        "WK" : pygame.Rect(2 + 83 * 0, 3, 75, 75),
        "WQ" : pygame.Rect(2 + 83 * 1, 3, 75, 75),
        "WB" : pygame.Rect(2 + 83 * 2, 3, 75, 75),
        "WN" : pygame.Rect(2 + 83 * 3, 3, 75, 75),
        "WR" : pygame.Rect(2 + 83 * 4, 3, 75, 75),
        "WP" : pygame.Rect(2 + 83 * 5, 3, 75, 75),

        "BK" : pygame.Rect(2 + 83 * 0, 86, 75, 75),
        "BQ" : pygame.Rect(2 + 83 * 1, 86, 75, 75),
        "BB" : pygame.Rect(2 + 83 * 2, 86, 75, 75),
        "BN" : pygame.Rect(2 + 83 * 3, 86, 75, 75),
        "BR" : pygame.Rect(2 + 83 * 4, 86, 75, 75),
        "BP" : pygame.Rect(2 + 83 * 5, 86, 75, 75)
    }

    def __init__(self, side: Side, piece_type: PieceType):
        if side is Side.NEUTRAL:
            raise "A piece can't be neutral, it's reserved to cell that have no piece"
        self.side = side
        self.piece_type = piece_type

    def get_side(self) -> Side:
        return self.side

    def get_type(self) -> PieceType:
        return self.piece_type

    def __str__(self) -> str:
        side_str = "W" if self.get_side() is Side.WHITE else "B"
        type_str = self.get_type().value
        return side_str + type_str

    def get_sprite_rect(self) -> pygame.Rect:
        return Piece.RECTS[self.__str__()]

class Board(object):
    def __init__(self):
        self.board = [None for _ in range(8*8)]

        self.set_piece(Piece(Side.BLACK, PieceType.ROOK), 0, 0)
        self.set_piece(Piece(Side.BLACK, PieceType.KNIGHT), 1, 0)
        self.set_piece(Piece(Side.BLACK, PieceType.BISHOP), 2, 0)
        self.set_piece(Piece(Side.BLACK, PieceType.QUEEN), 3, 0)
        self.set_piece(Piece(Side.BLACK, PieceType.KING), 4, 0)
        self.set_piece(Piece(Side.BLACK, PieceType.BISHOP), 5, 0)
        self.set_piece(Piece(Side.BLACK, PieceType.KNIGHT), 6, 0)
        self.set_piece(Piece(Side.BLACK, PieceType.ROOK), 7, 0)

        self.set_piece(Piece(Side.BLACK, PieceType.PAWN), 0, 1)
        self.set_piece(Piece(Side.BLACK, PieceType.PAWN), 1, 1)
        self.set_piece(Piece(Side.BLACK, PieceType.PAWN), 2, 1)
        self.set_piece(Piece(Side.BLACK, PieceType.PAWN), 3, 1)
        self.set_piece(Piece(Side.BLACK, PieceType.PAWN), 4, 1)
        self.set_piece(Piece(Side.BLACK, PieceType.PAWN), 5, 1)
        self.set_piece(Piece(Side.BLACK, PieceType.PAWN), 6, 1)
        self.set_piece(Piece(Side.BLACK, PieceType.PAWN), 7, 1)

        self.set_piece(Piece(Side.WHITE, PieceType.ROOK), 0, 7)
        self.set_piece(Piece(Side.WHITE, PieceType.KNIGHT), 1, 7)
        self.set_piece(Piece(Side.WHITE, PieceType.BISHOP), 2, 7)
        self.set_piece(Piece(Side.WHITE, PieceType.QUEEN), 3, 7)
        self.set_piece(Piece(Side.WHITE, PieceType.KING), 4, 7)
        self.set_piece(Piece(Side.WHITE, PieceType.BISHOP), 5, 7)
        self.set_piece(Piece(Side.WHITE, PieceType.KNIGHT), 6, 7)
        self.set_piece(Piece(Side.WHITE, PieceType.ROOK), 7, 7)

        self.set_piece(Piece(Side.WHITE, PieceType.PAWN), 0, 6)
        self.set_piece(Piece(Side.WHITE, PieceType.PAWN), 1, 6)
        self.set_piece(Piece(Side.WHITE, PieceType.PAWN), 2, 6)
        self.set_piece(Piece(Side.WHITE, PieceType.PAWN), 3, 6)
        self.set_piece(Piece(Side.WHITE, PieceType.PAWN), 4, 6)
        self.set_piece(Piece(Side.WHITE, PieceType.PAWN), 5, 6)
        self.set_piece(Piece(Side.WHITE, PieceType.PAWN), 6, 6)
        self.set_piece(Piece(Side.WHITE, PieceType.PAWN), 7, 6)

    def __index_of(self, x: int, y: int) -> int:
        if x in range(8) and y in range(8):
            return x * 8 + y
        raise IndexError()

    def set_piece(self, piece: Piece, x: int, y: int):
        self.board[self.__index_of(x, y)] = piece

    def get_piece(self, x: int, y: int)-> Piece:
        return self.board[self.__index_of(x, y)]

    def remove_piece(self, x: int, y: int):
        piece = self.get_piece(x, y)
        self.board[self.__index_of(x, y)] = None
        return piece

    def __to_screen_coords(self, screen: pygame.Surface, x: int, y: int) -> (int, int):
        return x * screen.get_width() / 8, y * screen.get_height() / 8

    def draw(self, screen: pygame.Surface):
        is_white = True
        white_color = (220, 193, 147)
        black_color = (80, 42, 1)
        for x in range(0, screen.get_width(), screen.get_width() // 8):
            for y in range(0, screen.get_height(), screen.get_height() // 8):
                pygame.draw.rect(
                    screen,
                    white_color if is_white else black_color,
                    (x, y, screen.get_width() // 8, screen.get_height() // 8))
                is_white = not is_white
            is_white = not is_white

        for x in range(8):
            for y in range(8):
                piece = self.get_piece(x, y)
                if piece is not None:
                    screen.blit(Piece.SPRITE, self.__to_screen_coords(screen, x, y), piece.get_sprite_rect())
