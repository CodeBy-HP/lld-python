
class ElevatorSystem:
    INSTANCE = None
    elevator_control_strategy = None
    elevator_selection_strategy = None

    def __init__(self):
        if ElevatorSystem.INSTANCE is not None:
            raise Exception("ElevatorSystem is a singleton!")
        else:
            self.elevator_controller_list = []
            self.floors = []
            ElevatorSystem.INSTANCE = self

    def add_elevator(self, elevator):
        self.elevator_controller_list.append(elevator)

    def remove_elevator(self, elevator):
        self.elevator_controller_list.remove(elevator)

    def set_elevator_control_strategy(self, strategy):
        ElevatorSystem.elevator_control_strategy = strategy

    def set_elevator_selection_strategy(self, strategy):
        ElevatorSystem.elevator_selection_strategy = strategy

    def add_floor(self, floor):
        self.floors.append(floor)

    def get_elevator_controller_list(self):
        return self.elevator_controller_list

    def get_floors(self):
        return self.floors

# Create the ElevatorSystem singleton instance at import time
ElevatorSystem()
