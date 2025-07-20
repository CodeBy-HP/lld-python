
from .display import Display
from .button import ExternalButton
from .direction import Direction

class Floor:
    def __init__(self, id):
        self.id = id
        self.display = Display()
        self.button = ExternalButton()

    def press_button(self, direction):
        """
        Simulate someone on this floor pressing the up/down button.
        """
        self.button.press_button(self.id, direction)

    def set_display(self, floor, direction):
        self.display.set_floor(floor)
        self.display.set_direction(direction)
