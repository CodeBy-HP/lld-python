
from .elevator_system import ElevatorSystem

class ExternalDispatcher:
    INSTANCE = None

    def __init__(self):
        if ExternalDispatcher.INSTANCE is not None:
            raise Exception("ExternalDispatcher is a singleton!")
        ExternalDispatcher.INSTANCE = self

    def submit_request(self, floor, direction):
        """
        Use the system's elevator selection strategy to pick an elevator,
        then pass the request to that elevator's controller.
        """
        elevator_id = ElevatorSystem.elevator_selection_strategy.select_elevator(floor)
        print(f"Selected elevator {elevator_id}")

        for e_controller in ElevatorSystem.INSTANCE.get_elevator_controller_list():
            if e_controller.id == elevator_id:
                e_controller.accept_request(floor, direction)

# Create the ExternalDispatcher singleton instance
ExternalDispatcher()
