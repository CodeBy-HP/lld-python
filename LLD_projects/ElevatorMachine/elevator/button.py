
from abc import ABC, abstractmethod
from .direction import Direction
from .external_dispatcher import ExternalDispatcher
from .internal_dispatcher import InternalDispatcher

class Button(ABC):
    @abstractmethod
    def press_button(self, floor, direction, elevator_id=None):
        pass

class ExternalButton(Button):
    def __init__(self):
        self.direction = None
        # Singleton ExternalDispatcher
        self.edispatcher = ExternalDispatcher.INSTANCE

    def press_button(self, floor, direction, elevator_id=None):
        self.direction = direction
        print(f"Pressed {direction.name} from floor {floor}")
        self.edispatcher.submit_request(floor, direction)

class InternalButton(Button):
    def __init__(self):
        # Each elevator’s internal dispatcher can be a simple instance
        self.idispatcher = InternalDispatcher()
        self.floors = [] # tracking, monitoring, multiple users can press the button at same time

    def press_button(self, floor, direction, elevator_id):
        self.floors.append(floor)
        print(f"Pressed floor {floor} from elevator {elevator_id}")
        self.idispatcher.submit_request(floor, direction, elevator_id)
