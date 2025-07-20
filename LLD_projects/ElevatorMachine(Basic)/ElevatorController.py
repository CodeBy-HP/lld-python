from Elevator import Elevator
from threading import Thread
from Request import Request


class ElevatorController:
    def __init__(self, num_elevators, capacity):
        self.elevators = []
        for i in range(num_elevators):
            elevator = Elevator(i + 1, capacity)
            self.elevators.append(elevator)
            Thread(target=elevator.run).start()

    def request_elevator(self, source_floor, destination_floor):
        optimal_elevator = self.find_optimal_elevator(source_floor, destination_floor)
        optimal_elevator.add_request(Request(source_floor, destination_floor))

    def find_optimal_elevator(self, source_floor, destination_floor):
        optimal_elevator = None
        min_dis = float("inf")

        for elevator in self.elevators:
            distance = abs(elevator.current_floor - source_floor)
            if distance < min_dis:
                optimal_elevator = elevator
                min_dis = distance
        return optimal_elevator
