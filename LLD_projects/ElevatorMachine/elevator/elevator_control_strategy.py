
from abc import ABC, abstractmethod
from .direction import Direction

class ElevatorControlStrategy(ABC):
    def __init__(self):
        # List of tuples: (floor, direction, elevator_controller)
        self.pending_requests = []

    @abstractmethod
    def move_elevator(self, elevator_controller):
        pass

class LookAlgorithm(ElevatorControlStrategy):
    """
    A simplified 'LOOK'-style algorithm:
      - Elevator continues in its current direction, serving requests on that path.
      - If no requests remain in that direction, it reverses direction (if more requests exist).
    """
    def move_elevator(self, elevator_controller):
        if not self.pending_requests:
            # No pending requests at all
            return

        elevator_car = elevator_controller.elevator_car
        current_floor = elevator_car.current_floor
        current_direction = elevator_car.direction

        # 1) Filter requests for this elevator
        requests_for_this_elevator = [
            (floor, dir_, ctrl)
            for (floor, dir_, ctrl) in self.pending_requests
            if ctrl == elevator_controller
        ]
        if not requests_for_this_elevator:
            return  # No requests for this particular elevator

        # 2) If elevator has no current direction (idle), assume UP to start
        if current_direction == Direction.NONE:
            current_direction = Direction.UP

        # 3) Filter requests that are in the current direction path
        if current_direction == Direction.UP:
            servable_requests = [
                (floor, dir_, ctrl)
                for (floor, dir_, ctrl) in requests_for_this_elevator
                if floor >= current_floor
            ]
            servable_requests.sort(key=lambda x: x[0])  # ascending floors
        else:  # current_direction == Direction.DOWN
            servable_requests = [
                (floor, dir_, ctrl)
                for (floor, dir_, ctrl) in requests_for_this_elevator
                if floor <= current_floor
            ]
            servable_requests.sort(key=lambda x: x[0], reverse=True)

        # 4) If no requests in the current direction, reverse direction
        if not servable_requests:
            current_direction = (
                Direction.DOWN if current_direction == Direction.UP else Direction.UP
            )
            if current_direction == Direction.UP:
                servable_requests = [
                    (floor, dir_, ctrl)
                    for (floor, dir_, ctrl) in requests_for_this_elevator
                    if floor >= current_floor
                ]
                servable_requests.sort(key=lambda x: x[0])
            else:  # DOWN
                servable_requests = [
                    (floor, dir_, ctrl)
                    for (floor, dir_, ctrl) in requests_for_this_elevator
                    if floor <= current_floor
                ]
                servable_requests.sort(key=lambda x: x[0], reverse=True)

            if not servable_requests:
                # Even after reversing direction, there are no requests
                return

        # 5) Take the next request in the sorted list
        next_floor, next_direction, _ = servable_requests[0]

        # Remove it from the global queue
        self.pending_requests.remove((next_floor, next_direction, elevator_controller))

        # 6) Move the elevator
        elevator_car.move(next_direction, next_floor)

        # 7) Update direction for the elevator
        elevator_car.direction = current_direction
