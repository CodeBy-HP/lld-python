from abc import ABC, abstractmethod
from enum import Enum
from typing import List, Optional, Deque
from collections import deque

class PieceType(Enum):
    """Represents possible game piece types"""
    X = 'X'
    O = 'O'

class Board:
    """Manages game board state and operations"""
    def __init__(self, size: int):
        self.size = size
        self.grid = [[None for _ in range(size)] for _ in range(size)]
    
    def place_piece(self, row: int, col: int, piece: 'Piece') -> bool:
        """Attempts to place a piece on the board"""
        if self.is_valid_move(row, col):
            self.grid[row][col] = piece
            return True
        return False
    
    def is_valid_move(self, row: int, col: int) -> bool:
        """Checks if a move is within board boundaries and unoccupied"""
        return (0 <= row < self.size and 
                0 <= col < self.size and 
                not self.grid[row][col])
    
    def is_full(self) -> bool:
        """Checks if board has no empty positions"""
        return all(cell for row in self.grid for cell in row)
    
    def display(self) -> None:
        """Prints the current board state"""
        for i, row in enumerate(self.grid):
            print(' | '.join([cell.type.value if cell else ' ' for cell in row]))
            if i < self.size - 1:
                print('-' * (self.size * 4 - 1))

class Piece:
    """Represents a game piece with specific type"""
    def __init__(self, type: PieceType):
        self.type = type

class Player(ABC):
    """Abstract base class for game players"""
    def __init__(self, name: str, piece: Piece):
        self.name = name
        self.piece = piece
    
    @abstractmethod
    def get_move(self, board: Board) -> tuple[int, int]:
        """Retrieve player's next move coordinates"""
        pass

class HumanPlayer(Player):
    """Represents a human player providing console input"""
    def get_move(self, board: Board) -> tuple[int, int]:
        """Gets and validates human player input"""
        while True:
            try:
                move = input(f"{self.name}'s turn ({self.piece.type.value}): Enter row,col >> ")
                row, col = map(int, move.split(','))
                if board.is_valid_move(row, col):
                    return row, col
                print("Invalid move. Try again.")
            except ValueError:
                print("Invalid input. Use format: row,col (e.g., 1,2)")

class GameRules:
    """Contains game rule validation logic"""
    @staticmethod
    def check_victory(board: Board, row: int, col: int) -> bool:
        """Checks if last move resulted in a win"""
        target = board.grid[row][col]
        
        # Check row
        if all(cell == target for cell in board.grid[row]):
            return True
        
        # Check column
        if all(board.grid[i][col] == target for i in range(board.size)):
            return True
        
        # Check diagonals
        if row == col and all(board.grid[i][i] == target for i in range(board.size)):
            return True
        
        if row + col == board.size - 1:
            return all(board.grid[i][board.size-1-i] == target for i in range(board.size))
        
        return False

class TicTacToe:
    """Manages game flow and state"""
    def __init__(self, board_size: int = 3):
        self.board = Board(board_size)
        self.players: Deque[Player] = deque()
        self.setup_players()
    
    def setup_players(self) -> None:
        """Initializes game players"""
        human1 = HumanPlayer("Player 1", Piece(PieceType.X))
        human2 = HumanPlayer("Player 2", Piece(PieceType.O))
        self.players.extend([human1, human2])
    
    def play(self) -> None:
        """Main game loop"""
        while True:
            current_player = self.players[0]
            self.board.display()
            
            row, col = current_player.get_move(self.board)
            self.board.place_piece(row, col, current_player.piece)
            
            if GameRules.check_victory(self.board, row, col):
                self.board.display()
                print(f"{current_player.name} wins!")
                return
                
            if self.board.is_full():
                self.board.display()
                print("Game ends in a tie!")
                return
                
            self.players.rotate()

if __name__ == "__main__":
    game = TicTacToe()
    game.play()

