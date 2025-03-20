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
            return spot
        return None

    def release_spot(self, spot):
        spot.remove_vehicle()
        self.available_spots.append(spot)

# Concrete Parking Spot Managers
class TwoWheelerParkingManager(ParkingSpotManager):
    def __init__(self, available_spots):
        super().__init__(available_spots, FirstAvailableStrategy())

class FourWheelerParkingManager(ParkingSpotManager):
    def __init__(self, available_spots):
        super().__init__(available_spots, FirstAvailableStrategy())

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
    def __init__(self, gate_id: int, parking_spot_factory: ParkingSpotFactory):
        self.gate_id = gate_id
        self.parking_spot_factory = parking_spot_factory

    def generate_ticket(self, vehicle: Vehicle):
        parking_manager = self.parking_spot_factory.get_parking_manager(vehicle.vehicle_type, [])
        spot = parking_manager.find_parking_space()
        if not spot:
            return None
        spot.assign_vehicle(vehicle)
        return Ticket(vehicle, spot)

# Cost Computation Strategy
class PriceStrategy(ABC):
    @abstractmethod
    def compute_price(self, duration_seconds: float, rate: float):
        pass

class HourlyPricingStrategy(PriceStrategy):
    def compute_price(self, duration_seconds: float, rate: float):
        return max(10, (duration_seconds / 3600) * rate)

# Cost Computation Interface
class CostComputationInterface(ABC):
    def __init__(self, price_strategy: PriceStrategy):
        self.price_strategy = price_strategy

    @abstractmethod
    def calculate_cost(self, entry_time: datetime, exit_time: datetime, rate: float):
        pass

class TwoWheelerCostComputation(CostComputationInterface):
    def __init__(self, price_strategy: PriceStrategy):
        super().__init__(price_strategy)

    def calculate_cost(self, entry_time: datetime, exit_time: datetime, rate: float):
        duration = (exit_time - entry_time).total_seconds()
        return self.price_strategy.compute_price(duration, rate)

class FourWheelerCostComputation(CostComputationInterface):
    def __init__(self, price_strategy: PriceStrategy):
        super().__init__(price_strategy)

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
                 parking_spot_factory: ParkingSpotFactory, payment_strategy: PaymentStrategy):
        self.gate_id = gate_id
        self.issued_tickets = issued_tickets
        self.cost_computation_factory = cost_computation_factory
        self.parking_spot_factory = parking_spot_factory
        self.payment_strategy = payment_strategy

    def price_cal(self, ticket: Ticket) -> float:
        exit_time = datetime.now()
        cost_computation = self.cost_computation_factory.get_cost_computation(ticket.vehicle.vehicle_type, HourlyPricingStrategy())
        return cost_computation.calculate_cost(ticket.entry_time, exit_time, ticket.parking_spot.price_per_hour)

    def process_payment(self, ticket: Ticket):
        amount_due = self.price_cal(ticket)
        return self.payment_strategy.process_payment(amount_due)

    def remove_vehicle(self, ticket_id: str):
        ticket = self.issued_tickets.pop(ticket_id, None)
        if not ticket or not self.process_payment(ticket):
            return False
        parking_manager = self.parking_spot_factory.get_parking_manager(ticket.vehicle.vehicle_type, [])
        parking_manager.release_spot(ticket.parking_spot)
        return True
