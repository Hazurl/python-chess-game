from enum import Enum
import pygame
from typing import Union
from itertools import product

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

class MoveDirection(Enum):
    N = 0
    W = 1
    S = 2
    E = 3
    NE = 4
    NW = 5
    SW = 6
    SE = 7

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
        self.dragged_piece = None
        self.checking_king = False

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

    def get_piece(self, x: int, y: int) -> Union[Piece, None]:
        try:
            return self.board[self.__index_of(x, y)]
        except IndexError:
            return None

    def remove_piece(self, x: int, y: int) -> Union[Piece, None]:
        piece = self.get_piece(x, y)
        self.board[self.__index_of(x, y)] = None
        return piece

    def move_piece(self, old_pos: (int, int), new_pos: (int, int)):
        cells = self.get_valid_cells(old_pos)
        if new_pos in cells:
            self.set_piece(self.remove_piece(*old_pos), *new_pos)

    def set_dragged_piece(self, x: int, y: int):
        self.dragged_piece = x, y

    def reset_dragged_piece(self):
        self.dragged_piece = None

    def is_empty(self, x: int, y: int) -> bool:
        return self.get_piece(x, y) is None

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
                if piece is not None and self.dragged_piece != (x, y):
                    coords = self.__to_screen_coords(screen, x, y)
                    screen.blit(Piece.SPRITE, coords, piece.get_sprite_rect())

    def get_valid_cells(self, from_cell: (int, int)) -> list:
        piece = self.get_piece(*from_cell)
        if piece is None:
            return list()

        ptype = piece.get_type()
        pside = piece.get_side()

        if ptype is PieceType.ROOK:
            return self.__get_valids_cells_direction(from_cell, pside, MoveDirection.N)\
                 + self.__get_valids_cells_direction(from_cell, pside, MoveDirection.W)\
                 + self.__get_valids_cells_direction(from_cell, pside, MoveDirection.E)\
                 + self.__get_valids_cells_direction(from_cell, pside, MoveDirection.S)

        if ptype is PieceType.BISHOP:
            return self.__get_valids_cells_direction(from_cell, pside, MoveDirection.NE)\
                 + self.__get_valids_cells_direction(from_cell, pside, MoveDirection.NW)\
                 + self.__get_valids_cells_direction(from_cell, pside, MoveDirection.SE)\
                 + self.__get_valids_cells_direction(from_cell, pside, MoveDirection.SW)

        if ptype is PieceType.QUEEN:
            return self.__get_valids_cells_direction(from_cell, pside, MoveDirection.N)\
                 + self.__get_valids_cells_direction(from_cell, pside, MoveDirection.W)\
                 + self.__get_valids_cells_direction(from_cell, pside, MoveDirection.E)\
                 + self.__get_valids_cells_direction(from_cell, pside, MoveDirection.S)\
                 + self.__get_valids_cells_direction(from_cell, pside, MoveDirection.NE)\
                 + self.__get_valids_cells_direction(from_cell, pside, MoveDirection.NW)\
                 + self.__get_valids_cells_direction(from_cell, pside, MoveDirection.SE)\
                 + self.__get_valids_cells_direction(from_cell, pside, MoveDirection.SW)

        if ptype is PieceType.KNIGHT:
            x, y = from_cell
            return [c for c in product((x-1, x+1), (y-2, y+2)) if self.__is_not_ally(c, pside)]\
                 + [c for c in product((x-2, x+2), (y-1, y+1)) if self.__is_not_ally(c, pside)]

        if ptype is PieceType.KING:
            x, y = from_cell
            prdct = product((x-1, x, x+1), (y-1, y, y+1))
            old_king = self.remove_piece(*from_cell)
            cells = [(cx, cy) for cx, cy in prdct if self.available_cell_king(cx, cy, pside)]
            self.set_piece(old_king, *from_cell)
            if from_cell in cells:
                cells.remove(from_cell)
            return cells

        if ptype is PieceType.PAWN:
            x, y = from_cell
            if pside is Side.BLACK: # down
                cells = list()
                if self.is_empty(x, y + 1):
                    cells.append((x, y+1))
                    if self.is_empty(x, y+2) and y == 1:
                        cells.append((x, y+2))
                if self.__is_not_ally((x+1, y+1), pside, False):
                    cells.append((x+1, y+1))
                if self.__is_not_ally((x-1, y+1), pside, False):
                    cells.append((x-1, y+1))
                return cells
            else:
                cells = list()
                if self.is_empty(x, y-1):
                    cells.append((x, y-1))
                    if self.is_empty(x, y-2) and y == 6:
                        cells.append((x, y-2))
                if self.__is_not_ally((x+1, y-1), pside, False):
                    cells.append((x+1, y-1))
                if self.__is_not_ally((x-1, y-1), pside, False):
                    cells.append((x-1, y-1))
                return cells

    def available_cell_king(self, x: int, y: int, side: Side) -> bool:
        if not self.__is_not_ally((x, y), side):
            return False
        for px in range(8):
            for py in range(8):
                piece = self.get_piece(px, py)
                if piece is not None and piece.get_side() != side:
                    if (x, y) in self.get_attack_cells((px, py)):
                        return False
        return True

    def get_attack_cells(self, from_cell: (int, int)) -> list:
        piece = self.get_piece(*from_cell)
        if piece is None:
            return list()

        ptype = piece.get_type()
        pside = piece.get_side()

        if ptype is PieceType.ROOK:
            return self.get_cells(from_cell, MoveDirection.N)\
                 + self.get_cells(from_cell, MoveDirection.W)\
                 + self.get_cells(from_cell, MoveDirection.E)\
                 + self.get_cells(from_cell, MoveDirection.S)

        if ptype is PieceType.BISHOP:
            return self.get_cells(from_cell, MoveDirection.NE)\
                 + self.get_cells(from_cell, MoveDirection.NW)\
                 + self.get_cells(from_cell, MoveDirection.SE)\
                 + self.get_cells(from_cell, MoveDirection.SW)

        if ptype is PieceType.QUEEN:
            return self.get_cells(from_cell, MoveDirection.N)\
                 + self.get_cells(from_cell, MoveDirection.W)\
                 + self.get_cells(from_cell, MoveDirection.E)\
                 + self.get_cells(from_cell, MoveDirection.S)\
                 + self.get_cells(from_cell, MoveDirection.NE)\
                 + self.get_cells(from_cell, MoveDirection.NW)\
                 + self.get_cells(from_cell, MoveDirection.SE)\
                 + self.get_cells(from_cell, MoveDirection.SW)

        if ptype is PieceType.KNIGHT:
            x, y = from_cell
            return list(product((x-1, x+1), (y-2, y+2))) + list(product((x-2, x+2), (y-1, y+1)))

        if ptype is PieceType.KING:
            x, y = from_cell
            cells = list(product((x-1, x, x+1), (y-1, y, y+1)))
            cells.remove((x, y))
            return cells

        if ptype is PieceType.PAWN:
            x, y = from_cell
            if pside is Side.BLACK: # down
                return [(x+1, y+1), (x-1, y+1)]
            else:
                return [(x+1, y-1), (x-1, y-1)]

    def __is_not_ally(self, cell: (int, int), side: Side, can_be_empty: bool = True) -> bool:
        piece = self.get_piece(*cell)
        if piece is None:
            return can_be_empty
        return piece.get_side() is not side

    def __get_valids_cells_direction(self, from_cell: (int, int), side: Side, direction: MoveDirection):
        cells = self.get_cells(from_cell, direction)
        if not cells:
            return list()
        last_piece = self.get_piece(*cells[len(cells) - 1])
        if last_piece is not None and last_piece.get_side() is side:
            cells.pop()
        return cells

    def get_cells(self, start: (int, int), direction: MoveDirection) -> list:
        sx, sy = start
        cells = list()
        if direction is MoveDirection.N:
            for y in range(sy - 1, -1, -1): # interval ]sy, 0]
                cells.append((sx, y))
                if not self.is_empty(sx, y):
                    return cells

        if direction is MoveDirection.S:
            for y in range(sy + 1, 8): # interval ]sy, 7]
                cells.append((sx, y))
                if not self.is_empty(sx, y):
                    return cells

        if direction is MoveDirection.W:
            for x in range(sx - 1, -1, -1): # interval ]sx, 0]
                cells.append((x, sy))
                if not self.is_empty(x, sy):
                    return cells

        if direction is MoveDirection.E:
            for x in range(sx + 1, 8): # interval ]sx, 7]
                cells.append((x, sy))
                if not self.is_empty(x, sy):
                    return cells

        if direction is MoveDirection.NW:
            for x, y in zip(range(sx - 1, -1, -1), range(sy - 1, -1, -1)):
                cells.append((x, y))
                if not self.is_empty(x, y):
                    return cells

        if direction is MoveDirection.NE:
            for x, y in zip(range(sx + 1, 8), range(sy - 1, -1, -1)):
                cells.append((x, y))
                if not self.is_empty(x, y):
                    return cells

        if direction is MoveDirection.SE:
            for x, y in zip(range(sx + 1, 8), range(sy + 1, 8)):
                cells.append((x, y))
                if not self.is_empty(x, y):
                    return cells

        if direction is MoveDirection.SW:
            for x, y in zip(range(sx - 1, -1, -1), range(sy + 1, 8)):
                cells.append((x, y))
                if not self.is_empty(x, y):
                    return cells
        return cells
