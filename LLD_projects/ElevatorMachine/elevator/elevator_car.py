
from .door import Door
from .display import Display
from .button import InternalButton
from .direction import Direction

class ElevatorCar:
    def __init__(self, id):
        self.id = id
        self.door = Door()
        self.display = Display()
        self.current_floor = 0
        self.direction = Direction.NONE
        self.button = InternalButton()

    def move(self, direction, floor):
        print(f"Elevator {self.id} moving {direction.name}")
        print(f"Elevator {self.id} stops at floor {floor}")
        self.door.open(self.id)
        self.door.close(self.id)

        self.current_floor = floor
        self.direction = direction
        self.set_display()

    def press_button(self, floor):
        # Determine direction based on requested floor vs. current floor
        direction = Direction.NONE
        if floor > self.current_floor:
            direction = Direction.UP
        elif floor < self.current_floor:
            direction = Direction.DOWN
        self.button.press_button(floor, direction, self.id)

    def set_display(self):
        self.display.set_floor(self.current_floor)
        self.display.set_direction(self.direction)
