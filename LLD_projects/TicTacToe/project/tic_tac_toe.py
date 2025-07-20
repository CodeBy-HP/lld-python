from collections import deque
from board import Board
from player import HumanPlayer
from piece import Piece, PieceType

class TicTacToe:
    def __init__(self):
        self.board = Board()
        self.players = deque()
        self.initialize_game()

    def initialize_game(self):
        name1, name2 = input("Enter the players' names (separated by space): ").split()
        player1 = HumanPlayer(name1, Piece(PieceType.X))
        player2 = HumanPlayer(name2, Piece(PieceType.O))
        self.players.append(player1)
        self.players.append(player2)
        print(f"{name1} has piece type {player1.piece.piece_type_value}")
        print(f"{name2} has piece type {player2.piece.piece_type_value}")
        print()

    def start_game(self):
        tie = False
        while True:
            player_turn = self.players.popleft()
            self.board.display_grid()
            row, col = player_turn.get_move(self.board)
            self.board.place_piece(row, col, player_turn.piece)
            self.players.append(player_turn)
            if self.board.is_full():
                tie = True
                break

            if self.is_winner(row, col, player_turn.piece.piece_type):
                print(f"{player_turn.name} is the winner!")
                break

        if tie:
            print("The game is a tie")

    def is_winner(self, row, col, piece_type):
        board = self.board.grid
        size = self.board.size

        row_match = all(board[row][i] and board[row][i].piece_type == piece_type for i in range(size))
        col_match = all(board[i][col] and board[i][col].piece_type == piece_type for i in range(size))
        diag_match = all(board[i][i] and board[i][i].piece_type == piece_type for i in range(size))
        anti_diag_match = all(board[i][size - 1 - i] and board[i][size - 1 - i].piece_type == piece_type for i in range(size))

        return row_match or col_match or diag_match or anti_diag_match

if __name__ == "__main__":
    game = TicTacToe()
    game.start_game()