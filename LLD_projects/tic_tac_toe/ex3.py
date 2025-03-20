# Tic Tac Toe LLD Design
# objects -> Board, Player,PlayingPiece,game

# Player(concrete class)
# - name
# - PlayingPiece

# Board(concrete class)
# - size
# - board 2D matrix to hold PlayingPiece
# + add_piece(row,col,piece)
# + is_full()

# PieceType(enum class):
# X = 'X'
# O = 'O'

# PlayingPice(Abstract class)
# - piece_type

# -> XPlayingPiece(child of PlayingPiece)
#     super.__init__(PieceType.X)

# -> OPlayingPice(child of PlayingPiece)
#     super.__init__(PieceType.Y)

# Game(concrete class)
# - Board
# - players (dequeue)

# + start_game
#     player_turn

#     while no_winner:
#         is_full() -> tie
#         add_piece(row,col)
#         is_winner()


from abc import ABC, abstractmethod
from collections import deque
from enum import Enum
from typing import List, Optional, Tuple, Deque


# --------------------------------------------------------------------
# Domain Models & Enums
# --------------------------------------------------------------------

class PieceType(Enum):
    X = "X"
    O = "O"


class PlayingPiece(ABC):
    def __init__(self, piece_type: PieceType) -> None:
        self.piece_type: PieceType = piece_type

    def __str__(self) -> str:
        return self.piece_type.value


class XPlayingPiece(PlayingPiece):
    def __init__(self) -> None:
        super().__init__(PieceType.X)


class OPlayingPiece(PlayingPiece):
    def __init__(self) -> None:
        super().__init__(PieceType.O)


class Player:
    def __init__(self, name: str, playing_piece: PlayingPiece) -> None:
        self.name: str = name
        self.playing_piece: PlayingPiece = playing_piece

    def __str__(self) -> str:
        return self.name


# --------------------------------------------------------------------
# Board Class
# --------------------------------------------------------------------

class Board:
    def __init__(self, size: int) -> None:
        self.size: int = size
        # Create a grid initialized to None
        self._grid: List[List[Optional[PlayingPiece]]] = [
            [None for _ in range(size)] for _ in range(size)
        ]

    def add_piece(self, row: int, col: int, piece: PlayingPiece) -> bool:
        if self._is_valid_position(row, col) and self._grid[row][col] is None:
            self._grid[row][col] = piece
            return True
        return False

    def _is_valid_position(self, row: int, col: int) -> bool:
        return 0 <= row < self.size and 0 <= col < self.size

    def is_full(self) -> bool:
        return all(cell is not None for row in self._grid for cell in row)

    def get_cell(self, row: int, col: int) -> Optional[PlayingPiece]:
        if self._is_valid_position(row, col):
            return self._grid[row][col]
        raise ValueError("Invalid board position")

    def display(self) -> None:
        # Render the board in a clean format.
        for row in self._grid:
            row_str = " | ".join(str(cell) if cell is not None else " " for cell in row)
            print(row_str)
            print("-" * (self.size * 4 - 1))


# --------------------------------------------------------------------
# Win Condition Strategy (Strategy Pattern)
# --------------------------------------------------------------------

class WinConditionStrategy(ABC):
    @abstractmethod
    def check_winner(self, board: Board, last_move: Tuple[int, int], player: Player) -> bool:
        """Determines if the current move resulted in a win."""
        pass


class TicTacToeWinCondition(WinConditionStrategy):
    def check_winner(self, board: Board, last_move: Tuple[int, int], player: Player) -> bool:
        row, col = last_move
        size = board.size
        piece = player.playing_piece

        # Check the row of the last move.
        if all(board.get_cell(row, c) == piece for c in range(size)):
            return True

        # Check the column of the last move.
        if all(board.get_cell(r, col) == piece for r in range(size)):
            return True

        # Check main diagonal if applicable.
        if row == col and all(board.get_cell(i, i) == piece for i in range(size)):
            return True

        # Check anti-diagonal if applicable.
        if row + col == size - 1 and all(board.get_cell(i, size - i - 1) == piece for i in range(size)):
            return True

        return False


# --------------------------------------------------------------------
# Game Engine (Application Layer)
# --------------------------------------------------------------------

class TicTacToeGame:
    def __init__(self, board_size: int = 3, win_strategy: WinConditionStrategy = None) -> None:
        self.board: Board = Board(board_size)
        self.players: Deque[Player] = deque()
        # Use the provided win strategy or default to TicTacToe rules.
        self.win_strategy: WinConditionStrategy = win_strategy or TicTacToeWinCondition()

    def add_players(self) -> None:
        self.players.append(Player("Player 1", XPlayingPiece()))
        self.players.append(Player("Player 2", OPlayingPiece()))

    def play(self) -> None:
        self.add_players()
        tie = False

        while True:
            if self.board.is_full():
                tie = True
                break

            current_player: Player = self.players.popleft()
            self.board.display()

            # Input handling is encapsulated in its own method.
            row, col = self._get_move(current_player)

            if not self.board.add_piece(row, col, current_player.playing_piece):
                print("Invalid move; spot already taken. Try again.")
                self.players.appendleft(current_player)
                continue

            if self.win_strategy.check_winner(self.board, (row, col), current_player):
                self.board.display()
                print(f"Congratulations {current_player.name}! You win!")
                return

            self.players.append(current_player)

        if tie:
            self.board.display()
            print("The game is a tie!")

    def _get_move(self, player: Player) -> Tuple[int, int]:
        """Handles input validation and parsing for player moves."""
        while True:
            try:
                user_input = input(f"{player.name} ({player.playing_piece}), enter row,col: ")
                row_str, col_str = user_input.split(",")
                row, col = int(row_str), int(col_str)
                if 0 <= row < self.board.size and 0 <= col < self.board.size:
                    return (row, col)
                else:
                    print(f"Please enter values between 0 and {self.board.size - 1}.")
            except (ValueError, IndexError):
                print("Invalid input. Please enter row and column separated by a comma.")


# --------------------------------------------------------------------
# Application Entry Point
# --------------------------------------------------------------------

if __name__ == "__main__":
    game = TicTacToeGame(board_size=3)
    game.play()
