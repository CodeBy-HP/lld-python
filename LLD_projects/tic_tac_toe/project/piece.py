from enum import Enum


class PieceType(Enum):
    X = "X"
    O = "O"


class Piece:
    def __init__(self, piece_type: PieceType):
        self._type = piece_type

    @property
    def piece_type(self):
        return self._type

    @property
    def piece_type_value(self):
        return self._type.value


if __name__ == "__main__":
    p1 = Piece(PieceType.X)
    print(p1)
    print(p1.piece_type)
    print(p1.piece_type_value)
