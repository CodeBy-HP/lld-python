from piece import Piece, PieceType

class Board:
    def __init__(self, size=3):
        self._size = size
        self._grid = [[None for _ in range(size)] for _ in range(size)]

    @property
    def size(self):
        return self._size

    @property
    def grid(self):
        return self._grid

    def display_grid(self):
        for i in range(self.size):
            print("|", end="")
            for j in range(self.size):
                piece = self.grid[i][j]
                if piece:
                    print(f"{piece.piece_type_value}", end="|")
                else:
                    print(" ", end="|")
            print()

    def is_valid_move(self, row: int, col: int) -> bool:
        return row in range(self.size) and col in range(self.size) and self.grid[row][col] is None

    def is_full(self) -> bool:
        return all(cell is not None for row in self.grid for cell in row)

    def place_piece(self, row: int, col: int, piece: Piece) -> bool:
        if self.is_valid_move(row, col):
            self.grid[row][col] = piece
            return True
        return False

    def clear_grid(self):
        for i in range(self.size):
            for j in range(self.size):
                self.grid[i][j] = None

if __name__ == "__main__":
    b = Board()
    p = Piece(PieceType.X)

    print(b.size)
    b.display_grid()
    print(b.grid)

    print(b.is_valid_move(2, 3))
    print(b.is_full())
    print(b.place_piece(2, 2, p))
    b.display_grid()
    b.clear_grid()
    b.display_grid()