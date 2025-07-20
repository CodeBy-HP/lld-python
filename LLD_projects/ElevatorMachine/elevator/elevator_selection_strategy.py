
from abc import ABC, abstractmethod
from .elevator_system import ElevatorSystem

class ElevatorSelectionStrategy(ABC):
    def __init__(self):
        self.elevator_controller_list = ElevatorSystem.INSTANCE.get_elevator_controller_list()

    @abstractmethod
    def select_elevator(self, floor):
        pass

class OddEvenStrategy(ElevatorSelectionStrategy):
    """
    Example strategy:
      - If the request floor is odd, prefer an elevator with an odd ID.
      - If the request floor is even, prefer an elevator with an even ID.
      - If none match, default to elevator 1.
    """
    def select_elevator(self, floor):
        for e_controller in self.elevator_controller_list:
            if floor % 2 == e_controller.id % 2:
                return e_controller.id
        return 1
