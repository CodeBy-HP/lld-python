from abc import ABC, abstractmethod
from dataclasses import dataclass
from datetime import datetime
import enum
import threading
from typing import List, Optional


# ======================
# ENUMS AND DATA CLASSES
# ======================


class VehicleType(enum):
    MOTORCYLCE: 1
    CAR: 2
    BUS: 3


@dataclass(frozen=True)
class ParkingConfig:
    motorcycle_spots: int = 50
    car_spots: int = 34
    bus_spots: int = 23


# =================
# CORE DOMAIN MODEL
# =================


class Vehicle(ABC):
    def __init__(self, licence_plate: str, vehicle_type: VehicleType):
        self.licence_plate = licence_plate
        self.vehicle_type = vehicle_type
        self._validate_licence_plate()

    def _validate_licence_plate(self):
        if not self.licence_plate:
            raise ValueError("Licence plate cannot be empty")


class Car(Vehicle):
    def __init__(self, licence_plate: str):
        super().__init__(licence_plate, VehicleType.CAR)


class Bike(Vehicle):
    def __init__(self, licence_plate):
        super().__init__(licence_plate, VehicleType.MOTORCYLCE)


class Bus(Vehicle):
    def __init__(self, licence_plate):
        super().__init__(licence_plate, VehicleType.BUS)


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


class ParkingStrategy(ABC):
    @abstractmethod
    def find_spot(
        self, spots: List[ParkingSpot], vehicle: Vehicle
    ) -> Optional[ParkingSpot]:
        pass


class FirstAvailableStrategy(ParkingStrategy):
    def find_spot(
        self, spots: List[ParkingSpot], vehicle: Vehicle
    ) -> Optional[ParkingSpot]:
        for spot in self.spots:
            if spot.can_accomodate(self.vehilce) and not spot.is_occupied:
                return spot
        return None


class EnergyEfficientStrategy(ParkingStrategy):
    def select_spot(
        self, spots: List[ParkingSpot], vehicle: Vehicle
    ) -> Optional[ParkingSpot]:
        return next(
            (
                spot
                for spot in sorted(spots, key=lambda s: s.hourly_rate)
                if spot.can_accommodate(vehicle) and not spot.is_occupied
            ),
            None,
        )


class PricingStrategy(ABC):
    @abstractmethod
    def calculate_fee(
        self, entry_time: datetime, exit_time: datetime, spot: ParkingSpot
    ) -> float:
        pass


class PricingStrategy(ABC):
    @abstractmethod
    def calculate_fee(
        self, entry_time: datetime, exit_time: datetime, spot: ParkingSpot
    ) -> float:
        pass


class StandardPricing(PricingStrategy):
    def calculate_fee(
        self, entry_time: datetime, exit_time: datetime, spot: ParkingSpot
    ) -> float:
        duration = (exit_time - entry_time).total_seconds() / 3600
        return max(1.0, duration * spot.hourly_rate)

    def calculate_fee(
        self, entry_time: datetime, exit_time: datetime, spot: ParkingSpot
    ) -> float:
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


