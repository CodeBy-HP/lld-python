from abc import ABC, abstractmethod
from enum import Enum
from datetime import datetime
import uuid

# Enum for Vehicle Type
class VehicleType(Enum):
    BIKE = 1
    CAR = 2
    TRUCK = 3

# Abstract Parking Spot Class
class ParkingSpot(ABC):
    def __init__(self, spot_id: int, price_per_hour: float):
        self.spot_id = spot_id
        self.is_empty = True
        self.vehicle = None
        self.price_per_hour = price_per_hour

    def assign_vehicle(self, vehicle):
        if self.is_empty:
            self.vehicle = vehicle
            self.is_empty = False
            return True
        return False

    def remove_vehicle(self):
        self.vehicle = None
        self.is_empty = True

# Concrete Parking Spot Classes
class TwoWheelerSpot(ParkingSpot):
    def __init__(self, spot_id: int):
        super().__init__(spot_id, price_per_hour=2.0)

class FourWheelerSpot(ParkingSpot):
    def __init__(self, spot_id: int):
        super().__init__(spot_id, price_per_hour=5.0)

# Abstract Strategy Pattern for Parking Allocation
class ParkingStrategy(ABC):
    @abstractmethod
    def find_parking_spot(self, available_spots):
        pass

class FirstAvailableStrategy(ParkingStrategy):
    def find_parking_spot(self, available_spots):
        for spot in available_spots:
            if spot.is_empty:
                return spot
        return None

# Abstract Parking Spot Manager
class ParkingSpotManager(ABC):
    def __init__(self, available_spots, parking_strategy):
        self.available_spots = available_spots
        self.parking_strategy = parking_strategy

    def find_parking_space(self):
        return self.parking_strategy.find_parking_spot(self.available_spots)

    def park_vehicle(self, vehicle):
        spot = self.find_parking_space()
        if spot:
            spot.assign_vehicle(vehicle)
            # Remove spot from available list since it's now occupied
            self.available_spots.remove(spot)
            return spot
        return None

    def release_spot(self, spot):
        spot.remove_vehicle()
        # Add the spot back into the available list
        self.available_spots.append(spot)

# Concrete Parking Spot Managers
class TwoWheelerParkingManager(ParkingSpotManager):
    def __init__(self, available_spots):
        super().__init__(available_spots, FirstAvailableStrategy())

class FourWheelerParkingManager(ParkingSpotManager):
    def __init__(self, available_spots):
        super().__init__(available_spots, FirstAvailableStrategy())

# Vehicle Class
class Vehicle(ABC):
    def __init__(self, vehicle_no: str, vehicle_type: VehicleType):
        self.vehicle_no = vehicle_no
        self.vehicle_type = vehicle_type

class Bike(Vehicle):
    def __init__(self, vehicle_no: str):
        super().__init__(vehicle_no, VehicleType.BIKE)

class Car(Vehicle):
    def __init__(self, vehicle_no: str):
        super().__init__(vehicle_no, VehicleType.CAR)

class Truck(Vehicle):
    def __init__(self, vehicle_no: str):
        super().__init__(vehicle_no, VehicleType.TRUCK)

# Ticket Class
class Ticket:
    def __init__(self, vehicle, parking_spot):
        self.ticket_id = str(uuid.uuid4())
        self.vehicle = vehicle
        self.entry_time = datetime.now()
        self.parking_spot = parking_spot

# Parking Spot Factory
class ParkingSpotFactory:
    @staticmethod
    def get_parking_manager(vehicle_type, available_spots):
        if vehicle_type == VehicleType.BIKE:
            return TwoWheelerParkingManager(available_spots)
        elif vehicle_type in [VehicleType.CAR, VehicleType.TRUCK]:
            return FourWheelerParkingManager(available_spots)
        raise ValueError("Invalid Vehicle Type!")

# Entrance Gate
class EntranceGate:
    def __init__(self, gate_id: int, parking_spot_factory: ParkingSpotFactory, available_spots):
        self.gate_id = gate_id
        self.parking_spot_factory = parking_spot_factory
        self.available_spots = available_spots

    def generate_ticket(self, vehicle: Vehicle):
        # Obtain the proper parking manager with the current list of available spots
        parking_manager = self.parking_spot_factory.get_parking_manager(vehicle.vehicle_type, self.available_spots)
        spot = parking_manager.park_vehicle(vehicle)
        if not spot:
            return None
        return Ticket(vehicle, spot)

# Cost Computation Strategy
class PriceStrategy(ABC):
    @abstractmethod
    def compute_price(self, duration_seconds: float, rate: float):
        pass

class HourlyPricingStrategy(PriceStrategy):
    def compute_price(self, duration_seconds: float, rate: float):
        # Minimum charge is 10; otherwise compute based on duration in hours
        return max(10, (duration_seconds / 3600) * rate)

# Cost Computation Interface
class CostComputationInterface(ABC):
    def __init__(self, price_strategy: PriceStrategy):
        self.price_strategy = price_strategy

    @abstractmethod
    def calculate_cost(self, entry_time: datetime, exit_time: datetime, rate: float):
        pass

class TwoWheelerCostComputation(CostComputationInterface):
    def calculate_cost(self, entry_time: datetime, exit_time: datetime, rate: float):
        duration = (exit_time - entry_time).total_seconds()
        return self.price_strategy.compute_price(duration, rate)

class FourWheelerCostComputation(CostComputationInterface):
    def calculate_cost(self, entry_time: datetime, exit_time: datetime, rate: float):
        duration = (exit_time - entry_time).total_seconds()
        return self.price_strategy.compute_price(duration, rate)

class CostComputationFactory:
    @staticmethod
    def get_cost_computation(vehicle_type, price_strategy):
        if vehicle_type == VehicleType.BIKE:
            return TwoWheelerCostComputation(price_strategy)
        elif vehicle_type in [VehicleType.CAR, VehicleType.TRUCK]:
            return FourWheelerCostComputation(price_strategy)
        raise ValueError("Invalid Vehicle Type!")

# Payment Strategy
class PaymentStrategy(ABC):
    @abstractmethod
    def process_payment(self, amount: float) -> bool:
        pass

class CreditCardPaymentStrategy(PaymentStrategy):
    def process_payment(self, amount: float) -> bool:
        # Implement credit card payment processing logic here
        return True

class CashPaymentStrategy(PaymentStrategy):
    def process_payment(self, amount: float) -> bool:
        # Implement cash payment processing logic here
        return True

# Exit Gate
class ExitGate:
    def __init__(self, gate_id: int, issued_tickets: dict, cost_computation_factory: CostComputationFactory,
                 parking_spot_factory: ParkingSpotFactory, available_spots, payment_strategy: PaymentStrategy):
        self.gate_id = gate_id
        self.issued_tickets = issued_tickets
        self.cost_computation_factory = cost_computation_factory
        self.parking_spot_factory = parking_spot_factory
        self.available_spots = available_spots
        self.payment_strategy = payment_strategy

    def calculate_price(self, ticket: Ticket) -> float:
        exit_time = datetime.now()
        cost_computation = self.cost_computation_factory.get_cost_computation(
            ticket.vehicle.vehicle_type, HourlyPricingStrategy()
        )
        return cost_computation.calculate_cost(ticket.entry_time, exit_time, ticket.parking_spot.price_per_hour)

    def process_payment(self, ticket: Ticket) -> bool:
        amount_due = self.calculate_price(ticket)
        return self.payment_strategy.process_payment(amount_due)

    def remove_vehicle(self, ticket_id: str) -> bool:
        ticket = self.issued_tickets.pop(ticket_id, None)
        if not ticket or not self.process_payment(ticket):
            return False
        # Release the spot by updating the available spots list
        parking_manager = self.parking_spot_factory.get_parking_manager(ticket.vehicle.vehicle_type, self.available_spots)
        parking_manager.release_spot(ticket.parking_spot)
        return True

# Central Parking Lot Class to manage available spots and issued tickets
class ParkingLot:
    def __init__(self, two_wheeler_spots, four_wheeler_spots):
        self.available_two_wheeler_spots = two_wheeler_spots
        self.available_four_wheeler_spots = four_wheeler_spots
        self.issued_tickets = {}

    def get_available_spots(self, vehicle_type):
        if vehicle_type == VehicleType.BIKE:
            return self.available_two_wheeler_spots
        elif vehicle_type in [VehicleType.CAR, VehicleType.TRUCK]:
            return self.available_four_wheeler_spots
        else:
            return []

    def park_vehicle(self, vehicle: Vehicle, entrance_gate: EntranceGate):
        ticket = entrance_gate.generate_ticket(vehicle)
        if ticket:
            self.issued_tickets[ticket.ticket_id] = ticket
        return ticket

    def exit_vehicle(self, ticket_id: str, exit_gate: ExitGate):
        return exit_gate.remove_vehicle(ticket_id)

# ------------------ Testing the System ------------------
if __name__ == "__main__":
    # Create parking spots for two- and four-wheelers
    two_wheeler_spots = [TwoWheelerSpot(i) for i in range(1, 6)]
    four_wheeler_spots = [FourWheelerSpot(i) for i in range(101, 106)]

    # Initialize the ParkingLot with available spots
    parking_lot = ParkingLot(two_wheeler_spots, four_wheeler_spots)

    # Instantiate a ParkingSpotFactory
    parking_spot_factory = ParkingSpotFactory()

    # Create Entrance Gates for bikes and cars using the actual available spots lists
    entrance_gate_bike = EntranceGate(1, parking_spot_factory, parking_lot.available_two_wheeler_spots)
    entrance_gate_car = EntranceGate(2, parking_spot_factory, parking_lot.available_four_wheeler_spots)

    # Prepare cost computation and payment strategies
    cost_factory = CostComputationFactory()
    payment_strategy = CashPaymentStrategy()

    # Create Exit Gates for bikes and cars using the corresponding available spots lists
    exit_gate_bike = ExitGate(1, parking_lot.issued_tickets, cost_factory, parking_spot_factory,
                              parking_lot.available_two_wheeler_spots, payment_strategy)
    exit_gate_car = ExitGate(2, parking_lot.issued_tickets, cost_factory, parking_spot_factory,
                             parking_lot.available_four_wheeler_spots, payment_strategy)

    # Park a Bike
    bike = Bike("BIKE123")
    ticket_bike = parking_lot.park_vehicle(bike, entrance_gate_bike)
    if ticket_bike:
        print("Bike parked with ticket:", ticket_bike.ticket_id)
    else:
        print("No available spot for the bike.")

    # Park a Car
    car = Car("CAR456")
    ticket_car = parking_lot.park_vehicle(car, entrance_gate_car)
    if ticket_car:
        print("Car parked with ticket:", ticket_car.ticket_id)
    else:
        print("No available spot for the car.")

    # Simulate exit for Bike
    if ticket_bike:
        success = parking_lot.exit_vehicle(ticket_bike.ticket_id, exit_gate_bike)
        print("Bike exit successful:", success)

    # Simulate exit for Car
    if ticket_car:
        success = parking_lot.exit_vehicle(ticket_car.ticket_id, exit_gate_car)
        print("Car exit successful:", success)
