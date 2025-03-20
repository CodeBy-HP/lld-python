from abc import ABC
from collections import deque
from enum import Enum

class PieceType(Enum):
    X = "X"
    O = "O"

class PlayingPiece(ABC):
    def __init__(self, piece_type: PieceType):
        self.piece_type = piece_type

class PlayingPieceX(PlayingPiece):
    def __init__(self):
        super().__init__(PieceType.X)

class PlayingPieceO(PlayingPiece):
    def __init__(self):
        super().__init__(PieceType.O)

class Player:
    def __init__(self, name, playing_piece: PlayingPiece):
        self.name = name
        self.playing_piece = playing_piece

class Board:
    def __init__(self, size: int):
        self.size = size
        self.board = [[None for _ in range(size)] for _ in range(size)]

    def add_piece(self, row: int, col: int, playing_piece: PlayingPiece) -> bool:
        if self.board[row][col] is not None:
            return False
        self.board[row][col] = playing_piece
        return True

    def get_free_cells(self):
        return [(i, j) for i in range(self.size) for j in range(self.size) if self.board[i][j] is None]

    def print_board(self):
        for row in self.board:
            print(" | ".join(piece.piece_type.value if piece else " " for piece in row))
            print("-" * (self.size * 4 - 1))

class TicTacToeGame:
    def __init__(self):
        self.players = deque()
        self.game_board = None

    def initialize_game(self):
        self.players.append(Player("Player1", PlayingPieceX()))
        self.players.append(Player("Player2", PlayingPieceO()))
        self.game_board = Board(3)

    def start_game(self):
        no_winner = True
        while no_winner:
            player_turn = self.players.popleft()
            self.game_board.print_board()
            free_spaces = self.game_board.get_free_cells()
            if not free_spaces:
                no_winner = False
                break
            
            row, col = map(int, input(f"{player_turn.name}, enter row,column: ").split(","))
            if not self.game_board.add_piece(row, col, player_turn.playing_piece):
                print("Incorrect position chosen, try again")
                self.players.appendleft(player_turn)
                continue
            
            self.players.append(player_turn)
            if self.is_there_winner(row, col, player_turn.playing_piece.piece_type):
                return f"{player_turn.name} wins!"
        return "It's a tie!"

    def is_there_winner(self, row: int, col: int, piece_type: PieceType) -> bool:
        board = self.game_board.board
        size = self.game_board.size
        
        row_match = all(board[row][i] and board[row][i].piece_type == piece_type for i in range(size))
        col_match = all(board[i][col] and board[i][col].piece_type == piece_type for i in range(size))
        diag_match = all(board[i][i] and board[i][i].piece_type == piece_type for i in range(size))
        anti_diag_match = all(board[i][size-1-i] and board[i][size-1-i].piece_type == piece_type for i in range(size))
        
        return row_match or col_match or diag_match or anti_diag_match


# if __name__ == "__main__":
#     game = TicTacToeGame()
#     game.initialize_game()
#     print(game.start_game())

