from enum import Enum
import random
from collections import deque

# Direction enum
class Direction(Enum):
    UP = 1
    DOWN = 2
    NONE = 3

# Display class
class Display:
    def __init__(self):
        self.floor = 0
        self.dir = Direction.NONE
    
    def set_floor(self, floor):
        self.floor = floor
    
    def set_dir(self, dir):
        self.dir = dir

# Door class
class Door:
    def open(self, id):
        print(f"Door opens for elevator {id}")
    
    def close(self, id):
        print(f"Door closes for elevator {id}")

# Button base class
class Button:
    def press_button(self, floor, dir):
        pass
    
    def press_button_with_id(self, floor, dir, elevator_id):
        pass

# PendingRequests class
class PendingRequests:
    def __init__(self, floor, dir):
        self.floor = floor
        self.dir = dir

# ElevatorSystem singleton
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

# Create the ElevatorSystem singleton instance
ElevatorSystem()

# ExternalDispatcher singleton
class ExternalDispatcher:
    INSTANCE = None
    
    def __init__(self):
        if ExternalDispatcher.INSTANCE is not None:
            raise Exception("ExternalDispatcher is a singleton!")
        else:
            ExternalDispatcher.INSTANCE = self
    
    def submit_request(self, floor, dir):
        elevator_id = ElevatorSystem.elevator_selection_strategy.select_elevator(floor, dir)
        print(f"Selected elevator {elevator_id}")
        
        for e_controller in ElevatorSystem.INSTANCE.get_elevator_controller_list():
            if e_controller.id == elevator_id:
                e_controller.accept_request(floor, dir)

# Create the ExternalDispatcher singleton instance
ExternalDispatcher()

# InternalDispatcher class
class InternalDispatcher:
    def submit_request(self, floor, dir, elevator_id):
        for e_controller in ElevatorSystem.INSTANCE.get_elevator_controller_list():
            if e_controller.id == elevator_id:
                e_controller.accept_request(floor, dir)

# Button implementations
class ExternalButton(Button):
    def __init__(self):
        self.direction = None
        self.edispatcher = ExternalDispatcher.INSTANCE
    
    def press_button(self, floor, dir):
        self.direction = dir
        print(f"Pressed {dir.name} from floor {floor}")
        self.edispatcher.submit_request(floor, dir)

class InternalButton(Button):
    def __init__(self):
        self.floors = []
        self.idispatcher = InternalDispatcher()
    
    def press_button_with_id(self, floor, dir, elevator_id):
        self.floors.append(floor)
        print(f"Pressed floor {floor} from elevator {elevator_id}")
        self.idispatcher.submit_request(floor, dir, elevator_id)

# Floor class
class Floor:
    def __init__(self, id):
        self.id = id
        self.display = Display()
        self.button = ExternalButton()
    
    def press_button(self, dir):
        self.button.press_button(self.id, dir)
    
    def set_display(self, floor, dir):
        self.display.set_floor(floor)
        self.display.set_dir(dir)

# ElevatorCar class
class ElevatorCar:
    def __init__(self, id):
        self.id = id
        self.door = Door()
        self.display = Display()
        self.current_floor = 0
        self.dir = Direction.NONE
        self.button = InternalButton()
    
    def move(self, dir, floor):
        print(f"Elevator {self.id} moving {dir.name}")
        print(f"Elevator {self.id} stops at floor {floor}")
        self.door.open(self.id)
        self.door.close(self.id)
        
        # Update current floor and direction
        self.current_floor = floor
        self.dir = dir
        
        # Update display
        self.set_display()
    
    def press_button(self, floor):
        dir = Direction.NONE
        if floor > self.current_floor:
            dir = Direction.UP
        elif floor < self.current_floor:
            dir = Direction.DOWN
        
        self.button.press_button_with_id(floor, dir, self.id)
    
    def set_display(self):
        self.display.set_floor(self.current_floor)
        self.display.set_dir(self.dir)

# ElevatorController class
class ElevatorController:
    def __init__(self, id):
        self.id = id
        self.elevator_car = ElevatorCar(id)
    
    def accept_request(self, floor, dir):
        ElevatorSystem.elevator_control_strategy.pending_request_list.append(PendingRequests(floor, dir))
        self.control_car()
    
    def control_car(self):
        ElevatorSystem.elevator_control_strategy.move_elevator(self)
        print("Elevator request processed...")

# Strategy base classes
class ElevatorSelectionStrategy:
    def __init__(self):
        self.elevator_controller_list = ElevatorSystem.INSTANCE.get_elevator_controller_list()
    
    def select_elevator(self, floor, dir):
        return 0  # Base implementation

class ElevatorControlStrategy:
    def __init__(self):
        self.pending_request_list = []
    
    def move_elevator(self, elevator_controller):
        pass  # Base implementation

# ZoneStrategy implementation
class ZoneStrategy(ElevatorSelectionStrategy):
    def __init__(self):
        super().__init__()
        # Example: Elevator 1 serves floors 1-5, Elevator 2 serves floors 6-10
        self.zone_assignments = {
            1: range(1, 6),  # Floors 1-5
            2: range(6, 11)  # Floors 6-10
        }
    
    def select_elevator(self, floor, dir):
        # Check if the floor is in any zone
        for elevator_id, floor_range in self.zone_assignments.items():
            if floor in floor_range:
                return elevator_id
        
        # If no specific zone assignment, choose a random elevator
        if self.elevator_controller_list:
            return random.randint(1, len(self.elevator_controller_list))
        return 1  # Default to first elevator

# Control Strategy implementations
class FirstComeFirstServe(ElevatorControlStrategy):
    def move_elevator(self, elevator_controller):
        if not self.pending_request_list:
            return
        
        # Take the first request (FIFO)
        request = self.pending_request_list.pop(0)
        floor = request.floor
        
        elevator_car = elevator_controller.elevator_car
        current_floor = elevator_car.current_floor
        
        # Determine direction
        if floor > current_floor:
            move_dir = Direction.UP
        elif floor < current_floor:
            move_dir = Direction.DOWN
        else:
            move_dir = Direction.NONE
        
        # Move elevator to the requested floor
        elevator_car.move(move_dir, floor)

class ShortestSeekTime(ElevatorControlStrategy):
    def move_elevator(self, elevator_controller):
        if not self.pending_request_list:
            return
        
        elevator_car = elevator_controller.elevator_car
        current_floor = elevator_car.current_floor
        
        # Find the request that minimizes elevator movement
        closest_request = None
        min_distance = float('inf')
        closest_idx = -1
        
        for idx, request in enumerate(self.pending_request_list):
            floor = request.floor
            distance = abs(floor - current_floor)
            
            if distance < min_distance:
                min_distance = distance
                closest_request = request
                closest_idx = idx
        
        if closest_request:
            # Remove the selected request
            self.pending_request_list.pop(closest_idx)
            floor = closest_request.floor
            
            # Determine direction
            if floor > current_floor:
                move_dir = Direction.UP
            elif floor < current_floor:
                move_dir = Direction.DOWN
            else:
                move_dir = Direction.NONE
            
            # Move elevator to the requested floor
            elevator_car.move(move_dir, floor)

class ScanAlgorithm(ElevatorControlStrategy):
    def move_elevator(self, elevator_controller):
        if not self.pending_request_list:
            return
        
        elevator_car = elevator_controller.elevator_car
        current_floor = elevator_car.current_floor
        current_dir = elevator_car.dir
        
        # If elevator is not moving, decide direction based on first request
        if current_dir == Direction.NONE:
            first_request = self.pending_request_list[0]
            if first_request.floor > current_floor:
                current_dir = Direction.UP
            else:
                current_dir = Direction.DOWN
        
        # Find all requests that can be served in the current direction
        requests_in_direction = []
        
        for request in self.pending_request_list:
            floor = request.floor
            
            if current_dir == Direction.UP and floor >= current_floor:
                requests_in_direction.append(request)
            elif current_dir == Direction.DOWN and floor <= current_floor:
                requests_in_direction.append(request)
        
        # Sort requests based on direction
        if current_dir == Direction.UP:
            requests_in_direction.sort(key=lambda x: x.floor)
        else:
            requests_in_direction.sort(key=lambda x: x.floor, reverse=True)
        
        # If no requests in current direction, reverse direction
        if not requests_in_direction:
            current_dir = Direction.DOWN if current_dir == Direction.UP else Direction.UP
            return
        
        # Process the next request in the current direction
        next_request = requests_in_direction[0]
        self.pending_request_list.remove(next_request)
        
        floor = next_request.floor
        elevator_car.move(current_dir, floor)

# Main function to test the elevator system
def main():
    # Create elevator system
    elevator_system = ElevatorSystem.INSTANCE
    
    # Create control strategy
    control_strategy = FirstComeFirstServe()
    elevator_system.set_elevator_control_strategy(control_strategy)
    
    # Create selection strategy (ZoneStrategy)
    selection_strategy = ZoneStrategy()
    elevator_system.set_elevator_selection_strategy(selection_strategy)
    
    # Create elevators
    elevator1 = ElevatorController(1)
    elevator2 = ElevatorController(2)
    
    # Add elevators to system
    elevator_system.add_elevator(elevator1)
    elevator_system.add_elevator(elevator2)
    
    # Create floors (10 floors)
    for i in range(1, 11):
        floor = Floor(i)
        elevator_system.add_floor(floor)
    
    print("\n===== Testing FirstComeFirstServe Strategy =====")
    
    # Test scenario 1: External request from Floor 3 (UP)
    print("\nScenario 1: External request from Floor 3 (UP)")
    elevator_system.get_floors()[2].press_button(Direction.UP)  # Floor 3 (index 2)
    
    # Test scenario 2: Internal request in Elevator 1 to go to floor 7
    print("\nScenario 2: Internal request in Elevator 1 to Floor 7")
    elevator1.elevator_car.press_button(7)
    
    # Change to ShortestSeekTime strategy
    print("\n===== Testing ShortestSeekTime Strategy =====")
    control_strategy = ShortestSeekTime()
    elevator_system.set_elevator_control_strategy(control_strategy)
    
    # Test scenario 3: Multiple external requests
    print("\nScenario 3: Multiple external requests")
    elevator_system.get_floors()[4].press_button(Direction.DOWN)  # Floor 5
    elevator_system.get_floors()[8].press_button(Direction.UP)    # Floor 9
    
    # Test ScanAlgorithm
    print("\n===== Testing ScanAlgorithm Strategy =====")
    control_strategy = ScanAlgorithm()
    elevator_system.set_elevator_control_strategy(control_strategy)
    
    # Test scenario 4: Mixed internal and external requests
    print("\nScenario 4: Mixed internal and external requests")
    elevator_system.get_floors()[1].press_button(Direction.UP)  # Floor 2
    elevator1.elevator_car.press_button(6)

if __name__ == "__main__":
    main()
