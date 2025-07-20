from abc import ABC
from collections import deque
from enum import Enum


class PieceType(Enum):
    X = "X"
    O = "O"


class Piece(ABC):
    def __init__(self, piece_type: str):
        self.piece_type = piece_type


class XPiece(Piece):
    def __init__(self):
        super().__init__(PieceType.X)


class OPiece(Piece):
    def __init__(self):
        super().__init__(PieceType.O)


class Board:
    size = None
    board = None

    def __init__(self, size: int):
        self.size = size
        self.board = [[None for _ in range(size)] for _ in range(size)]

    def display_board(self):
        for row in self.board:
            print(" | ".join(piece.piece_type.value if piece else " " for piece in row))
            print("-" * (self.size * 4 - 1))

    def add_piece(self, row: int, col: int, piece: Piece) -> bool:
        if self.board[row][col] is None:
            self.board[row][col] = piece
            return True
        return False

    def free_cells(self):
        return [
            (i, j)
            for i in range(self.size)
            for j in range(self.size)
            if self.board[i][j] is None
        ]


class Player:
    def __init__(self, name, playing_piece):
        self.name = name
        self.playing_piece = playing_piece


class Game:
    def __init__(self):
        self.players = deque()
        self.board = None

    def initialize(self):
        self.board = Board(3)
        self.players.append(Player("Player 1", XPiece()))
        self.players.append(Player("Player 2", OPiece()))

    def start_game(self):
        no_winner = True
        while no_winner:
            player_turn = self.players.popleft()
            self.board.display_board()
            free_spaces = self.board.free_cells()

            if not free_spaces:
                no_winner = False
                break

            row, col = map(
                int, input(f"{player_turn.name}, enter row,col: ").split(",")
            )
            if (row, col) not in free_spaces:
                self.players.appendleft(player_turn)
                continue

            self.board.add_piece(row, col, player_turn.playing_piece)
            self.players.append(player_turn)
            if self.is_winner(row, col, player_turn.playing_piece.piece_type):
                print(f"{player_turn.name} wins!")  # Print the winner
                return

        print("It's a tie!")  # Print if it's a tie

    def is_winner(self, row, col, piece_type):
        board = self.board.board
        size = self.board.size

        row_match = all(
            board[row][i] and board[row][i].piece_type == piece_type
            for i in range(size)
        )
        col_match = all(
            board[i][col] and board[i][col].piece_type == piece_type
            for i in range(size)
        )
        diag_match = all(
            board[i][i] and board[i][i].piece_type == piece_type for i in range(size)
        )
        anti_diag_match = all(
            board[i][size - 1 - i] and board[i][size - 1 - i].piece_type == piece_type
            for i in range(size)
        )

        return row_match or col_match or diag_match or anti_diag_match


if __name__ == "__main__":
    game = Game()
    game.initialize()
    print(game.start_game())
