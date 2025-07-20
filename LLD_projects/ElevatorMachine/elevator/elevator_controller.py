
from .elevator_system import ElevatorSystem

class ElevatorController:
    def __init__(self, id, elevator_car):
        self.id = id
        self.elevator_car = elevator_car
    
    def accept_request(self, floor, direction):
        """
        We add this request to the ElevatorSystem's control strategy queue,
        associating it with this controller (so we know which elevator).
        """
        ElevatorSystem.elevator_control_strategy.pending_requests.append(
            (floor, direction, self)
        )
        self.control_car()

    def control_car(self):
        """
        Instruct the system's control strategy to move this elevator if needed.
        """
        ElevatorSystem.elevator_control_strategy.move_elevator(self)
        print("Elevator moving...")
