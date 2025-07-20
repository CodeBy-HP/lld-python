from abc import ABC, abstractmethod
from datetime import datetime
from enum import Enum
import threading
import uuid
import time
from dataclasses import dataclass
from typing import Dict, List, Optional

# ======================
# ENUMS AND DATA CLASSES
# ======================
class VehicleType(Enum):
    MOTORCYCLE = 1
    CAR = 2
    BUS = 3

@dataclass(frozen=True)
class ParkingConfig:
    motorcycle_spots: int = 50
    car_spots: int = 100
    bus_spots: int = 10
    base_hourly_rate: float = 2.5

# =================
# CORE DOMAIN MODEL
# =================
class Vehicle(ABC):
    def __init__(self, license_plate: str, vehicle_type: VehicleType):
        self.license_plate = license_plate
        self.vehicle_type = vehicle_type
        self._validate_license()

    def _validate_license(self):
        if not self.license_plate:
            raise ValueError("License plate cannot be empty")

class Motorcycle(Vehicle):
    def __init__(self, license_plate: str):
        super().__init__(license_plate, VehicleType.MOTORCYCLE)

class Car(Vehicle):
    def __init__(self, license_plate: str):
        super().__init__(license_plate, VehicleType.CAR)

class Bus(Vehicle):
    def __init__(self, license_plate: str):
        super().__init__(license_plate, VehicleType.BUS)

class ParkingSpot(ABC):
    def __init__(self, spot_id: str, hourly_rate: float):
        self.spot_id = spot_id
        self.hourly_rate = hourly_rate
        self.is_occupied = False
        self.lock = threading.Lock()

    @abstractmethod
    def can_accommodate(self, vehicle: Vehicle) -> bool:
        pass

    def occupy(self, vehicle: Vehicle) -> bool:
        with self.lock:
            if not self.is_occupied and self.can_accommodate(vehicle):
                self.is_occupied = True
                return True
            return False

    def vacate(self) -> None:
        with self.lock:
            self.is_occupied = False

class MotorcycleSpot(ParkingSpot):
    def __init__(self, spot_id: str):
        super().__init__(spot_id, hourly_rate=1.5)

    def can_accommodate(self, vehicle: Vehicle) -> bool:
        return vehicle.vehicle_type == VehicleType.MOTORCYCLE

class CompactSpot(ParkingSpot):
    def __init__(self, spot_id: str):
        super().__init__(spot_id, hourly_rate=2.5)

    def can_accommodate(self, vehicle: Vehicle) -> bool:
        return vehicle.vehicle_type in {VehicleType.MOTORCYCLE, VehicleType.CAR}

class LargeSpot(ParkingSpot):
    def __init__(self, spot_id: str):
        super().__init__(spot_id, hourly_rate=4.0)

    def can_accommodate(self, vehicle: Vehicle) -> bool:
        return True  # Can accommodate any vehicle type

# ==============
# CORE SERVICES
# ==============
class ParkingStrategy(ABC):
    @abstractmethod
    def select_spot(self, spots: List[ParkingSpot], vehicle: Vehicle) -> Optional[ParkingSpot]:
        pass

class FirstAvailableStrategy(ParkingStrategy):
    def select_spot(self, spots: List[ParkingSpot], vehicle: Vehicle) -> Optional[ParkingSpot]:
        for spot in spots:
            if spot.can_accommodate(vehicle) and not spot.is_occupied:
                return spot
        return None

class EnergyEfficientStrategy(ParkingStrategy):
    def select_spot(self, spots: List[ParkingSpot], vehicle: Vehicle) -> Optional[ParkingSpot]:
        return next((spot for spot in sorted(spots, key=lambda s: s.hourly_rate) 
                   if spot.can_accommodate(vehicle) and not spot.is_occupied), None)

class PricingStrategy(ABC):
    @abstractmethod
    def calculate_fee(self, entry_time: datetime, exit_time: datetime, spot: ParkingSpot) -> float:
        pass

class StandardPricing(PricingStrategy):
    def calculate_fee(self, entry_time: datetime, exit_time: datetime, spot: ParkingSpot) -> float:
        duration = (exit_time - entry_time).total_seconds() / 3600
        return max(1.0, duration * spot.hourly_rate)

class SurgePricing(PricingStrategy):
    def __init__(self, base_multiplier: float = 1.2):
        self.base_multiplier = base_multiplier

    def calculate_fee(self, entry_time: datetime, exit_time: datetime, spot: ParkingSpot) -> float:
        base_fee = StandardPricing().calculate_fee(entry_time, exit_time, spot)
        hour = exit_time.hour
        if 7 <= hour < 10 or 16 <= hour < 19:
            return base_fee * self.base_multiplier
        return base_fee

# ==============
# PAYMENT SYSTEM
# ==============
class PaymentProcessor(ABC):
    @abstractmethod
    def process_payment(self, amount: float) -> bool:
        pass

class CreditCardProcessor(PaymentProcessor):
    def process_payment(self, amount: float) -> bool:
        print(f"Processing credit card payment: ${amount:.2f}")
        return True  # Simplified for example

class MobileWalletProcessor(PaymentProcessor):
    def process_payment(self, amount: float) -> bool:
        print(f"Processing mobile payment: ${amount:.2f}")
        return True

# ===================
# OBSERVER PATTERN
# ===================
class ParkingEvent:
    def __init__(self, event_type: str, vehicle: Vehicle, spot: ParkingSpot):
        self.timestamp = datetime.now()
        self.event_type = event_type
        self.vehicle = vehicle
        self.spot = spot

class ParkingObserver(ABC):
    @abstractmethod
    def update(self, event: ParkingEvent):
        pass

class LoggingObserver(ParkingObserver):
    def update(self, event: ParkingEvent):
        print(f"[{event.timestamp}] {event.event_type} - {event.vehicle.license_plate} "
              f"at spot {event.spot.spot_id}")

class CapacityObserver(ParkingObserver):
    def __init__(self, parking_lot: 'ParkingLot'):
        self.parking_lot = parking_lot
        
    def update(self, event: ParkingEvent):
        available = self.parking_lot.available_spaces()
        print(f"Capacity Update: Motorcycle: {available[VehicleType.MOTORCYCLE]}, "
              f"Car: {available[VehicleType.CAR]}, Bus: {available[VehicleType.BUS]}")

# ==============
# CORE SYSTEM
# ==============
class ParkingLot:
    _instance = None
    _lock = threading.Lock()

    def __new__(cls, config: ParkingConfig = ParkingConfig()):
        with cls._lock:
            if not cls._instance:
                cls._instance = super().__new__(cls)
                cls._instance._initialize(config)
            return cls._instance

    def _initialize(self, config: ParkingConfig):
        self.config = config
        self.spots = {
            VehicleType.MOTORCYCLE: [MotorcycleSpot(f"M-{i}") for i in range(config.motorcycle_spots)],
            VehicleType.CAR: [CompactSpot(f"C-{i}") for i in range(config.car_spots)],
            VehicleType.BUS: [LargeSpot(f"B-{i}") for i in range(config.bus_spots)]
        }
        self.tickets: Dict[str, 'Ticket'] = {}
        self.observers: List[ParkingObserver] = []
        self.parking_strategy: ParkingStrategy = EnergyEfficientStrategy()
        self.pricing_strategy: PricingStrategy = SurgePricing()
        self.payment_processor: PaymentProcessor = CreditCardProcessor()

    def register_observer(self, observer: ParkingObserver):
        self.observers.append(observer)

    def _notify_observers(self, event: ParkingEvent):
        for observer in self.observers:
            observer.update(event)

    def available_spaces(self) -> Dict[VehicleType, int]:
        return {
            vt: sum(1 for spot in spots if not spot.is_occupied)
            for vt, spots in self.spots.items()
        }

    def park_vehicle(self, vehicle: Vehicle) -> Optional['Ticket']:
        for spot in self._find_appropriate_spots(vehicle.vehicle_type):
            selected_spot = self.parking_strategy.select_spot(spot, vehicle)
            if selected_spot and selected_spot.occupy(vehicle):
                ticket = Ticket(vehicle, selected_spot)
                self.tickets[ticket.ticket_id] = ticket
                self._notify_observers(ParkingEvent("ENTER", vehicle, selected_spot))
                return ticket
        return None

    def _find_appropriate_spots(self, vehicle_type: VehicleType) -> List[List[ParkingSpot]]:
        if vehicle_type == VehicleType.MOTORCYCLE:
            return [self.spots[VehicleType.MOTORCYCLE], self.spots[VehicleType.CAR]]
        elif vehicle_type == VehicleType.CAR:
            return [self.spots[VehicleType.CAR], self.spots[VehicleType.BUS]]
        return [self.spots[VehicleType.BUS]]

    def exit_vehicle(self, ticket_id: str) -> Optional[float]:
        ticket = self.tickets.get(ticket_id)
        if not ticket:
            raise InvalidTicketException("Invalid ticket ID")

        exit_time = datetime.now()
        fee = self.pricing_strategy.calculate_fee(ticket.entry_time, exit_time, ticket.spot)
        
        if self.payment_processor.process_payment(fee):
            ticket.spot.vacate()
            del self.tickets[ticket_id]
            self._notify_observers(ParkingEvent("EXIT", ticket.vehicle, ticket.spot))
            return fee
        raise PaymentFailedException("Payment processing failed")

class Ticket:
    def __init__(self, vehicle: Vehicle, spot: ParkingSpot):
        self.ticket_id = str(uuid.uuid4())
        self.entry_time = datetime.now()
        self.vehicle = vehicle
        self.spot = spot

# ==============
# EXCEPTIONS
# ==============
class ParkingException(Exception):
    """Base class for parking exceptions"""

class InvalidTicketException(ParkingException):
    """Invalid ticket provided"""

class PaymentFailedException(ParkingException):
    """Payment processing failed"""

# ==============
# CLIENT CODE
# ==============
def simulate_parking_operations():
    # Initialize parking lot with configuration
    config = ParkingConfig(motorcycle_spots=2, car_spots=2, bus_spots=1)
    parking_lot = ParkingLot(config)
    
    # Set up observers
    parking_lot.register_observer(LoggingObserver())
    parking_lot.register_observer(CapacityObserver(parking_lot))
    
    # Create test vehicles
    vehicles = [
        Motorcycle("M-001"),
        Motorcycle("M-002"),
        Car("C-001"),
        Car("C-002"),
        Bus("B-001")
    ]
    
    # Park all vehicles
    tickets = []
    print("=== Parking Vehicles ===")
    for idx, vehicle in enumerate(vehicles):
        if ticket := parking_lot.park_vehicle(vehicle):
            tickets.append(ticket)
            print(f"Parked {vehicle.license_plate} with ticket {ticket.ticket_id}")
        else:
            print(f"Failed to park {vehicle.license_plate}")
    
    # Try to park another vehicle (should fail)
    print("\n=== Testing Full Capacity ===")
    extra_car = Car("C-003")
    if parking_lot.park_vehicle(extra_car):
        print("Unexpectedly parked extra vehicle")
    else:
        print("Correctly rejected extra vehicle")
    
    # Wait to accumulate some parking time
    print("\n=== Simulating Time Passage ===")
    time.sleep(2)
    
    # Exit vehicles
    print("\n=== Exiting Vehicles ===")
    for ticket in tickets[:3]:  # Exit first 3 vehicles
        try:
            fee = parking_lot.exit_vehicle(ticket.ticket_id)
            print(f"Vehicle {ticket.vehicle.license_plate} exited. Fee: ${fee:.2f}")
        except ParkingException as e:
            print(f"Exit failed: {str(e)}")
    
    # Test invalid ticket
    print("\n=== Testing Invalid Ticket ===")
    try:
        parking_lot.exit_vehicle("invalid-ticket")
    except InvalidTicketException as e:
        print(f"Caught invalid ticket: {str(e)}")

if __name__ == "__main__":
    simulate_parking_operations()
