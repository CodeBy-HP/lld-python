from abc import ABC, abstractmethod
from enum import Enum
from datetime import datetime
import uuid

class VehicleType(Enum):
    BIKE = 1
    CAR = 2
    TRUCK = 3

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

class TwoWheelerSpot(ParkingSpot):
    def __init__(self, spot_id: int):
        super().__init__(spot_id, price_per_hour=2.0)

class FourWheelerSpot(ParkingSpot):
    def __init__(self, spot_id: int):
        super().__init__(spot_id, price_per_hour=5.0)

class ParkingStrategy(ABC):
    @abstractmethod
    def find_parking_spot(self, available_spots):
        pass

class FirstAvailableStrategy(ParkingStrategy):
    def find_parking_spot(self, available_spots):
        return next((spot for spot in available_spots if spot.is_empty), None)

class ParkingSpotManager(ABC):
    def __init__(self, available_spots, parking_strategy):
        self.available_spots = available_spots
        self.parking_strategy = parking_strategy

    def find_parking_space(self):
        return self.parking_strategy.find_parking_spot(self.available_spots)

    def park_vehicle(self, vehicle):
        spot = self.find_parking_space()
        if spot and spot.assign_vehicle(vehicle):
            self.available_spots.remove(spot)
            return spot
        return None

    def release_spot(self, spot):
        spot.remove_vehicle()
        self.available_spots.append(spot)

class TwoWheelerParkingManager(ParkingSpotManager):
    def __init__(self, available_spots):
        super().__init__(available_spots, FirstAvailableStrategy())

class FourWheelerParkingManager(ParkingSpotManager):
    def __init__(self, available_spots):
        super().__init__(available_spots, FirstAvailableStrategy())

class IParkingSpotFactory(ABC):
    @abstractmethod
    def get_parking_manager(self, vehicle_type):
        pass

class ParkingSpotFactory(IParkingSpotFactory):
    def __init__(self):
        self.managers = {
            VehicleType.BIKE: TwoWheelerParkingManager([]),
            VehicleType.CAR: FourWheelerParkingManager([]),
            VehicleType.TRUCK: FourWheelerParkingManager([])
        }

    def get_parking_manager(self, vehicle_type):
        return self.managers.get(vehicle_type)

    def initialize_spots(self, bike_spots=10, car_spots=20, truck_spots=5):
        self.managers[VehicleType.BIKE] = TwoWheelerParkingManager(
            [TwoWheelerSpot(i) for i in range(bike_spots)]
        )
        self.managers[VehicleType.CAR] = FourWheelerParkingManager(
            [FourWheelerSpot(i) for i in range(car_spots)]
        )
        self.managers[VehicleType.TRUCK] = FourWheelerParkingManager(
            [FourWheelerSpot(i + 100) for i in range(truck_spots)]
        )

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

class Ticket:
    def __init__(self, vehicle, parking_spot):
        self.ticket_id = str(uuid.uuid4())
        self.vehicle = vehicle
        self.entry_time = datetime.now()
        self.parking_spot = parking_spot

class PriceStrategy(ABC):
    @abstractmethod
    def compute_price(self, duration_seconds: float, rate: float):
        pass

class HourlyPricingStrategy(PriceStrategy):
    def compute_price(self, duration_seconds: float, rate: float):
        hours = max(1, duration_seconds / 3600)
        return round(hours * rate, 2)

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

class PaymentStrategy(ABC):
    @abstractmethod
    def process_payment(self, amount: float) -> bool:
        pass

class CreditCardPaymentStrategy(PaymentStrategy):
    def process_payment(self, amount: float) -> bool:
        print(f"Processing credit card payment of ${amount}")
        return True

class CashPaymentStrategy(PaymentStrategy):
    def process_payment(self, amount: float) -> bool:
        print(f"Processing cash payment of ${amount}")
        return True

class BillingService:
    def __init__(self, cost_computation_factory, payment_strategy):
        self.cost_computation_factory = cost_computation_factory
        self.payment_strategy = payment_strategy

    def process_exit(self, ticket):
        cost = self.calculate_cost(ticket)
        payment_success = self.payment_strategy.process_payment(cost)
        return payment_success

    def calculate_cost(self, ticket):
        exit_time = datetime.now()
        cost_computation = self.cost_computation_factory.get_cost_computation(
            ticket.vehicle.vehicle_type,
            HourlyPricingStrategy()
        )
        return cost_computation.calculate_cost(
            ticket.entry_time,
            exit_time,
            ticket.parking_spot.price_per_hour
        )

class EntranceGate:
    def __init__(self, gate_id: int, parking_spot_factory: IParkingSpotFactory):
        self.gate_id = gate_id
        self.parking_spot_factory = parking_spot_factory

    def generate_ticket(self, vehicle: Vehicle):
        parking_manager = self.parking_spot_factory.get_parking_manager(vehicle.vehicle_type)
        spot = parking_manager.park_vehicle(vehicle)
        return Ticket(vehicle, spot) if spot else None

class ExitGate:
    def __init__(self, gate_id: int, billing_service: BillingService, parking_spot_factory: IParkingSpotFactory):
        self.gate_id = gate_id
        self.billing_service = billing_service
        self.parking_spot_factory = parking_spot_factory

    def process_exit(self, ticket: Ticket):
        payment_success = self.billing_service.process_exit(ticket)
        if payment_success:
            manager = self.parking_spot_factory.get_parking_manager(ticket.vehicle.vehicle_type)
            manager.release_spot(ticket.parking_spot)
            return True
        return False

# Example usage
if __name__ == "__main__":
    # Initialize parking spots
    parking_factory = ParkingSpotFactory()
    parking_factory.initialize_spots(bike_spots=2, car_spots=3, truck_spots=1)

    # Create services
    cost_factory = CostComputationFactory()
    payment_strategy = CreditCardPaymentStrategy()
    billing_service = BillingService(cost_factory, payment_strategy)

    # Create gates
    entrance = EntranceGate(1, parking_factory)
    exit_gate = ExitGate(2, billing_service, parking_factory)

    # Park a bike
    bike = Bike("BIKE123")
    ticket = entrance.generate_ticket(bike)
    print(f"Bike parked with ticket: {ticket.ticket_id}")

    # Process exit
    success = exit_gate.process_exit(ticket)
    print(f"Exit processed successfully: {success}")