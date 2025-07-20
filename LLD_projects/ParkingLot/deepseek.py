from abc import ABC, abstractmethod
from enum import Enum
from datetime import datetime
import uuid
from typing import List, Dict

# -------------------- Enums --------------------
class VehicleType(Enum):
    BIKE = 1
    CAR = 2
    TRUCK = 3

# -------------------- Parking Spots --------------------
class ParkingSpot(ABC):
    def __init__(self, spot_id: int, price_per_hour: float):
        self.spot_id = spot_id
        self.price_per_hour = price_per_hour
        self.is_occupied = False
        self.vehicle = None

    def assign_vehicle(self, vehicle: 'Vehicle') -> bool:
        if not self.is_occupied:
            self.vehicle = vehicle
            self.is_occupied = True
            return True
        return False

    def release_vehicle(self) -> None:
        self.vehicle = None
        self.is_occupied = False

class TwoWheelerSpot(ParkingSpot):
    def __init__(self, spot_id: int):
        super().__init__(spot_id, 2.0)

class FourWheelerSpot(ParkingSpot):
    def __init__(self, spot_id: int):
        super().__init__(spot_id, 5.0)

# -------------------- Vehicle --------------------
class Vehicle:
    def __init__(self, license_plate: str, vehicle_type: VehicleType):
        self.license_plate = license_plate
        self.type = vehicle_type

# -------------------- Parking Strategy --------------------
class ParkingStrategy(ABC):
    @abstractmethod
    def select_spot(self, spots: List[ParkingSpot]) -> ParkingSpot | None:
        pass

class FirstAvailableStrategy(ParkingStrategy):
    def select_spot(self, spots: List[ParkingSpot]) -> ParkingSpot | None:
        return next((spot for spot in spots if not spot.is_occupied), None)

# -------------------- Parking Managers --------------------
class ParkingManager(ABC):
    def __init__(self, spots: List[ParkingSpot], strategy: ParkingStrategy):
        self.spots = spots
        self.strategy = strategy

    def park_vehicle(self, vehicle: Vehicle) -> ParkingSpot | None:
        spot = self.strategy.select_spot(self.spots)
        if spot and spot.assign_vehicle(vehicle):
            return spot
        return None

    def release_spot(self, spot: ParkingSpot) -> None:
        spot.release_vehicle()

class TwoWheelerManager(ParkingManager):
    def __init__(self, spots: List[TwoWheelerSpot]):
        super().__init__(spots, FirstAvailableStrategy())

class FourWheelerManager(ParkingManager):
    def __init__(self, spots: List[FourWheelerSpot]):
        super().__init__(spots, FirstAvailableStrategy())

# -------------------- Factory --------------------
class ManagerFactory:
    registry = {
        VehicleType.BIKE: TwoWheelerManager,
        VehicleType.CAR: FourWheelerManager,
        VehicleType.TRUCK: FourWheelerManager
    }

    @classmethod
    def register_manager(cls, vehicle_type: VehicleType, manager_class: type[ParkingManager]):
        cls.registry[vehicle_type] = manager_class

    @classmethod
    def get_manager(cls, vehicle_type: VehicleType, spots: List[ParkingSpot]) -> ParkingManager:
        return cls.registry[vehicle_type](spots)

# -------------------- Parking Lot --------------------
class ParkingLot:
    def __init__(self):
        self.two_wheeler_spots = [TwoWheelerSpot(i) for i in range(10)]
        self.four_wheeler_spots = [FourWheelerSpot(i) for i in range(20)]
        
    def get_spots(self, vehicle_type: VehicleType) -> List[ParkingSpot]:
        if vehicle_type == VehicleType.BIKE:
            return self.two_wheeler_spots
        return self.four_wheeler_spots

# -------------------- Ticket System --------------------
class Ticket:
    def __init__(self, vehicle: Vehicle, spot: ParkingSpot):
        self.id = uuid.uuid4()
        self.entry_time = datetime.now()
        self.vehicle = vehicle
        self.spot = spot

class TicketRegistry:
    def __init__(self):
        self.tickets: Dict[uuid.UUID, Ticket] = {}

    def add_ticket(self, ticket: Ticket) -> None:
        self.tickets[ticket.id] = ticket

    def get_ticket(self, ticket_id: uuid.UUID) -> Ticket | None:
        return self.tickets.get(ticket_id)

# -------------------- Pricing --------------------
class PricingStrategy(ABC):
    @abstractmethod
    def calculate_cost(self, entry: datetime, exit: datetime, rate: float) -> float:
        pass

class HourlyPricing(PricingStrategy):
    def calculate_cost(self, entry: datetime, exit: datetime, rate: float) -> float:
        duration = (exit - entry).total_seconds() / 3600
        return max(1.0, duration) * rate

# -------------------- Payment --------------------
class PaymentProcessor(ABC):
    @abstractmethod
    def process_payment(self, amount: float) -> bool:
        pass

class CreditCardProcessor(PaymentProcessor):
    def process_payment(self, amount: float) -> bool:
        print(f"Processing credit card payment: ${amount:.2f}")
        return True

# -------------------- Gates --------------------
class EntranceGate:
    def __init__(self, parking_lot: ParkingLot, registry: TicketRegistry):
        self.parking_lot = parking_lot
        self.registry = registry

    def issue_ticket(self, vehicle: Vehicle) -> Ticket | None:
        spots = self.parking_lot.get_spots(vehicle.type)
        manager = ManagerFactory.get_manager(vehicle.type, spots)
        spot = manager.park_vehicle(vehicle)
        
        if spot:
            ticket = Ticket(vehicle, spot)
            self.registry.add_ticket(ticket)
            return ticket
        return None

class ExitGate:
    def __init__(self, registry: TicketRegistry, pricing: PricingStrategy, 
                 payment_processor: PaymentProcessor, parking_lot: ParkingLot):
        self.registry = registry
        self.pricing = pricing
        self.processor = payment_processor
        self.parking_lot = parking_lot

    def process_exit(self, ticket_id: uuid.UUID) -> bool:
        ticket = self.registry.get_ticket(ticket_id)
        if not ticket:
            return False

        exit_time = datetime.now()
        cost = self.pricing.calculate_cost(ticket.entry_time, exit_time, 
                                         ticket.spot.price_per_hour)
        
        if self.processor.process_payment(cost):
            spots = self.parking_lot.get_spots(ticket.vehicle.type)
            manager = ManagerFactory.get_manager(ticket.vehicle.type, spots)
            manager.release_spot(ticket.spot)
            return True
        return False

# -------------------- Usage Example --------------------
if __name__ == "__main__":
    # Initialize system components
    parking_lot = ParkingLot()
    registry = TicketRegistry()
    pricing = HourlyPricing()
    payment_processor = CreditCardProcessor()

    # Create gates
    entrance = EntranceGate(parking_lot, registry)
    exit_gate = ExitGate(registry, pricing, payment_processor, parking_lot)

    # Vehicle enters
    car = Vehicle("ABC123", VehicleType.CAR)
    ticket = entrance.issue_ticket(car)
    
    if ticket:
        print(f"Ticket issued: {ticket.id}")
        
        # Vehicle exits
        success = exit_gate.process_exit(ticket.id)
        print(f"Exit processed successfully: {success}")
    else:
        print("No available spots")