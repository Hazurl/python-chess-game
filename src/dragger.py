from board import Piece 
import pygame

class Dragger(object):
    def __init__(self, piece: Piece, prev_pos: (int, int)):
        self.piece = piece
        self.prev_x, self.prev_y = prev_pos

    def get_piece(self) -> Piece:
        return self.piece

    def draw(self, screen: pygame.Surface):
        x, y = pygame.mouse.get_pos()
        piece_rect = self.piece.get_sprite_rect()
        coords = x - piece_rect.width / 2, y - piece_rect.height / 2
        screen.blit(Piece.SPRITE, coords, self.piece.get_sprite_rect())
