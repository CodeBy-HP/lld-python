
from elevator.elevator_system import ElevatorSystem
from elevator.elevator_controller import ElevatorController
from elevator.floor import Floor
from elevator.direction import Direction
from elevator.elevator_selection_strategy import OddEvenStrategy
from elevator.elevator_control_strategy import LookAlgorithm
from elevator.elevator_car import ElevatorCar

def main():
    # 1) Get the singleton ElevatorSystem instance
    elevator_system = ElevatorSystem.INSTANCE

    # 2) Create and set the strategies
    selection_strategy = OddEvenStrategy()
    elevator_system.set_elevator_selection_strategy(selection_strategy)

    control_strategy = LookAlgorithm()
    elevator_system.set_elevator_control_strategy(control_strategy)

    # 3) Create ElevatorCars and Controllers
    elevator1_car = ElevatorCar(1)
    elevator2_car = ElevatorCar(2)

    elevator1_controller = ElevatorController(1, elevator1_car)
    elevator2_controller = ElevatorController(2, elevator2_car)

    # 4) Register elevators with the system
    elevator_system.add_elevator(elevator1_controller)
    elevator_system.add_elevator(elevator2_controller)

    # 5) Create floors (1 through 10)
    for i in range(1, 11):
        floor = Floor(i)
        elevator_system.add_floor(floor)

    print("\n===== Testing OddEvenStrategy and LookAlgorithm =====")

    # Scenario 1: External request from Floor 3 (UP)
    print("\nScenario 1: External request from Floor 3 (UP)")
    elevator_system.get_floors()[2].press_button(Direction.UP)  # Floor index 2 = Floor 3

    # Scenario 2: Internal request in Elevator 1 to go to floor 7
    print("\nScenario 2: Internal request in Elevator 1 to Floor 7")
    elevator1_car.press_button(7)

    # Scenario 3: Multiple external requests
    print("\nScenario 3: Multiple external requests")
    elevator_system.get_floors()[4].press_button(Direction.DOWN)  # Floor 5
    elevator_system.get_floors()[8].press_button(Direction.UP)    # Floor 9

    # Scenario 4: Mixed internal and external requests
    print("\nScenario 4: Mixed internal and external requests")
    elevator_system.get_floors()[1].press_button(Direction.UP)  # Floor 2
    elevator1_car.press_button(6)

if __name__ == "__main__":
    main()
