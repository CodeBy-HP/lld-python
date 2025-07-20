
from .elevator_system import ElevatorSystem

class InternalDispatcher:
    def submit_request(self, floor, direction, elevator_id):
        """
        Internal request from inside elevator 'elevator_id'.
        Typically, you just pass it to the same elevator’s controller.
        """
        for e_controller in ElevatorSystem.INSTANCE.get_elevator_controller_list():
            if e_controller.id == elevator_id:
                e_controller.accept_request(floor, direction)
