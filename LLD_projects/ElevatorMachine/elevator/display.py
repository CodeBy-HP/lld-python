
from .direction import Direction

class Display:
    def __init__(self):
        self.floor = 0
        self.direction = Direction.NONE

    def set_floor(self, floor):
        self.floor = floor

    def set_direction(self, direction):
        self.direction = direction
