from abc import ABC
from piece import Piece,PieceType
from board import Board

class Player(ABC):
    def __init__(self, name: str, piece: Piece):
        self._name = name
        self._piece = piece

    @property
    def name(self):
        return self._name


    @property
    def piece(self):
        return self._piece


    def change_piece(self, piece: Piece):
        self._piece = piece

    def change_name(self, name: str):
        self._name = name

class HumanPlayer(Player):
    def get_move(self, board: Board):
        while True:
            try:
                move = input(f"{self.name}'s turn ({self.piece.piece_type_value}): Enter row,col >> ")
                row, col = map(int, move.split(','))
                if board.is_valid_move(row, col):
                    return row, col
                print("Invalid move. Try again.")
            except ValueError:
                print("Invalid input. Use format: row,col (e.g., 1,2)")

if __name__ == "__main__":
    p1 = HumanPlayer("harsh", Piece(PieceType.X))
    p2 = HumanPlayer("patel", Piece(PieceType.O))
    b = Board()
    
    print(p1.get_move(b))