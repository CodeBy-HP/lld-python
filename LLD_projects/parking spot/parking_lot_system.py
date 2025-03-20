from abc import ABC, abstractmethod
from enum import Enum
from datetime import datetime
import uuid
from typing import List, Dict, Optional
import time

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
        if not self.is_empty:
            self.vehicle = None
            self.is_empty = True
            return True
        return False

    def get_spot_type(self):
        return self.__class__.__name__

# Concrete Parking Spot Classes
class TwoWheelerSpot(ParkingSpot):
    def __init__(self, spot_id: int):
        super().__init__(spot_id, price_per_hour=2.0)

class FourWheelerSpot(ParkingSpot):
    def __init__(self, spot_id: int):
        super().__init__(spot_id, price_per_hour=5.0)

# Observer Pattern for Spot Availability Notifications
class SpotAvailabilityObserver(ABC):
    @abstractmethod
    def update(self, spot_type: str, spot_id: int):
        pass

# Parking Strategy Interface
class ParkingStrategy(ABC):
    @abstractmethod
    def find_parking_spot(self, available_spots: List[ParkingSpot]):
        pass

# Concrete Strategy Implementations
class FirstAvailableStrategy(ParkingStrategy):
    def find_parking_spot(self, available_spots: List[ParkingSpot]):
        for spot in available_spots:
            if spot.is_empty:
                return spot
        return None

class NearestEntranceStrategy(ParkingStrategy):
    def find_parking_spot(self, available_spots: List[ParkingSpot]):
        if not available_spots:
            return None
        
        # Assuming spots with lower IDs are closer to entrance
        available_empty_spots = [spot for spot in available_spots if spot.is_empty]
        if not available_empty_spots:
            return None
            
        return min(available_empty_spots, key=lambda spot: spot.spot_id)

# Parking Spot Manager
class ParkingSpotManager:
    def __init__(self, parking_strategy: ParkingStrategy):
        self.available_spots: List[ParkingSpot] = []
        self.parking_strategy = parking_strategy
        self.observers: List[SpotAvailabilityObserver] = []
    
    def add_spot(self, spot: ParkingSpot):
        self.available_spots.append(spot)
    
    def add_spots(self, spots: List[ParkingSpot]):
        self.available_spots.extend(spots)
        
    def find_parking_space(self):
        return self.parking_strategy.find_parking_spot(self.available_spots)
    
    def park_vehicle(self, vehicle):
        spot = self.find_parking_space()
        if spot and spot.assign_vehicle(vehicle):
            # Remove from available spots
            self.available_spots = [s for s in self.available_spots if s.spot_id != spot.spot_id]
            return spot
        return None
    
    def release_spot(self, spot: ParkingSpot):
        if spot.remove_vehicle():
            self.available_spots.append(spot)
            # Notify observers
            for observer in self.observers:
                observer.update(spot.get_spot_type(), spot.spot_id)
            return True
        return False
    
    def register_observer(self, observer: SpotAvailabilityObserver):
        self.observers.append(observer)
    
    def unregister_observer(self, observer: SpotAvailabilityObserver):
        if observer in self.observers:
            self.observers.remove(observer)

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
    def __init__(self, vehicle: Vehicle, parking_spot: ParkingSpot):
        self.ticket_id = str(uuid.uuid4())
        self.vehicle = vehicle
        self.entry_time = datetime.now()
        self.parking_spot = parking_spot
        self.exit_time = None
        self.amount_paid = 0.0
        self.status = "ACTIVE"
    
    def close_ticket(self, exit_time: datetime, amount_paid: float):
        self.exit_time = exit_time
        self.amount_paid = amount_paid
        self.status = "CLOSED"

# Price Strategy Interface
class PriceStrategy(ABC):
    @abstractmethod
    def compute_price(self, duration_seconds: float, rate: float) -> float:
        pass

# Concrete Price Strategies
class HourlyPricingStrategy(PriceStrategy):
    def compute_price(self, duration_seconds: float, rate: float) -> float:
        hours = duration_seconds / 3600
        return max(10, hours * rate)  # Minimum charge of $10

class DailyPricingStrategy(PriceStrategy):
    def compute_price(self, duration_seconds: float, rate: float) -> float:
        days = duration_seconds / (24 * 3600)
        daily_rate = rate * 8  # Assume daily rate is 8 hours worth
        return max(daily_rate, days * daily_rate)

# Cost Computation Interface
class CostComputation:
    def __init__(self, price_strategy: PriceStrategy):
        self.price_strategy = price_strategy
    
    def calculate_cost(self, entry_time: datetime, exit_time: datetime, rate: float) -> float:
        duration = (exit_time - entry_time).total_seconds()
        return self.price_strategy.compute_price(duration, rate)

# Payment Strategy Interface
class PaymentStrategy(ABC):
    @abstractmethod
    def process_payment(self, amount: float) -> bool:
        pass

# Concrete Payment Strategies
class CreditCardPaymentStrategy(PaymentStrategy):
    def __init__(self, card_number: str, expiry_date: str, cvv: str):
        self.card_number = card_number
        self.expiry_date = expiry_date
        self.cvv = cvv
    
    def process_payment(self, amount: float) -> bool:
        # Implement credit card payment processing logic here
        # For now, just simulate a successful payment
        print(f"Processing credit card payment of ${amount:.2f}")
        return True

class CashPaymentStrategy(PaymentStrategy):
    def process_payment(self, amount: float) -> bool:
        # Implement cash payment processing logic here
        print(f"Processing cash payment of ${amount:.2f}")
        return True

class UPIPaymentStrategy(PaymentStrategy):
    def __init__(self, upi_id: str):
        self.upi_id = upi_id
    
    def process_payment(self, amount: float) -> bool:
        # Implement UPI payment processing logic
        print(f"Processing UPI payment of ${amount:.2f} to {self.upi_id}")
        return True

# Factories
class ParkingSpotFactory:
    @staticmethod
    def create_parking_spot(spot_type: str, spot_id: int) -> ParkingSpot:
        if spot_type.lower() == "bike" or spot_type.lower() == "twowheeler":
            return TwoWheelerSpot(spot_id)
        elif spot_type.lower() in ["car", "truck", "fourwheeler"]:
            return FourWheelerSpot(spot_id)
        raise ValueError(f"Invalid parking spot type: {spot_type}")

class VehicleFactory:
    @staticmethod
    def create_vehicle(vehicle_type: str, vehicle_no: str) -> Vehicle:
        if vehicle_type.lower() == "bike":
            return Bike(vehicle_no)
        elif vehicle_type.lower() == "car":
            return Car(vehicle_no)
        elif vehicle_type.lower() == "truck":
            return Truck(vehicle_no)
        raise ValueError(f"Invalid vehicle type: {vehicle_type}")

# Display Board - Observer for Spot Availability
class DisplayBoard(SpotAvailabilityObserver):
    def __init__(self, display_id: int):
        self.display_id = display_id
        self.available_spots = {"TwoWheelerSpot": 0, "FourWheelerSpot": 0}
    
    def update(self, spot_type: str, spot_id: int):
        self.available_spots[spot_type] += 1
        self.display()
    
    def update_count(self, spot_type: str, count: int):
        self.available_spots[spot_type] = count
        self.display()
    
    def display(self):
        print(f"Display Board {self.display_id} - Available Spots:")
        for spot_type, count in self.available_spots.items():
            print(f"{spot_type}: {count}")

# Central Parking Lot Control System
class ParkingLot:
    def __init__(self, name: str):
        self.name = name
        self.parking_managers: Dict[VehicleType, ParkingSpotManager] = {}
        self.display_boards: List[DisplayBoard] = []
        self.issued_tickets: Dict[str, Ticket] = {}
        self.closed_tickets: Dict[str, Ticket] = {}
        self.entrance_gates: List['EntranceGate'] = []
        self.exit_gates: List['ExitGate'] = []

    def initialize_parking_lot(self, two_wheeler_spots: int, four_wheeler_spots: int):
        # Create managers with different strategies
        bike_manager = ParkingSpotManager(FirstAvailableStrategy())
        car_truck_manager = ParkingSpotManager(NearestEntranceStrategy())
        
        # Create and add spots
        for i in range(two_wheeler_spots):
            bike_manager.add_spot(TwoWheelerSpot(i + 1))
        
        for i in range(four_wheeler_spots):
            car_truck_manager.add_spot(FourWheelerSpot(i + 1))
        
        # Register managers
        self.parking_managers[VehicleType.BIKE] = bike_manager
        self.parking_managers[VehicleType.CAR] = car_truck_manager
        self.parking_managers[VehicleType.TRUCK] = car_truck_manager
        
        # Create display board
        display_board = DisplayBoard(1)
        display_board.update_count("TwoWheelerSpot", two_wheeler_spots)
        display_board.update_count("FourWheelerSpot", four_wheeler_spots)
        self.display_boards.append(display_board)
        
        # Register display board as observer for all managers
        for manager in self.parking_managers.values():
            manager.register_observer(display_board)
        
        # Create entrance and exit gates
        entrance_gate = EntranceGate(1, self)
        exit_gate = ExitGate(1, self)
        
        self.entrance_gates.append(entrance_gate)
        self.exit_gates.append(exit_gate)
        
        print(f"Parking Lot '{self.name}' initialized with {two_wheeler_spots} two-wheeler spots and {four_wheeler_spots} four-wheeler spots")

    def get_parking_manager(self, vehicle_type: VehicleType) -> Optional[ParkingSpotManager]:
        return self.parking_managers.get(vehicle_type)
    
    def add_ticket(self, ticket: Ticket):
        self.issued_tickets[ticket.ticket_id] = ticket
    
    def get_ticket(self, ticket_id: str) -> Optional[Ticket]:
        return self.issued_tickets.get(ticket_id)
    
    def close_ticket(self, ticket: Ticket, exit_time: datetime, amount_paid: float):
        if ticket.ticket_id in self.issued_tickets:
            ticket.close_ticket(exit_time, amount_paid)
            self.closed_tickets[ticket.ticket_id] = ticket
            del self.issued_tickets[ticket.ticket_id]
            return True
        return False

# Entrance Gate
class EntranceGate:
    def __init__(self, gate_id: int, parking_lot: ParkingLot):
        self.gate_id = gate_id
        self.parking_lot = parking_lot

    def generate_ticket(self, vehicle: Vehicle) -> Optional[Ticket]:
        parking_manager = self.parking_lot.get_parking_manager(vehicle.vehicle_type)
        
        if not parking_manager:
            print(f"No parking manager available for vehicle type: {vehicle.vehicle_type}")
            return None
        
        spot = parking_manager.park_vehicle(vehicle)
        
        if not spot:
            print(f"No parking spot available for vehicle: {vehicle.vehicle_no}")
            return None
        
        ticket = Ticket(vehicle, spot)
        self.parking_lot.add_ticket(ticket)
        
        print(f"Ticket generated: {ticket.ticket_id} for vehicle {vehicle.vehicle_no} at spot {spot.spot_id}")
        return ticket

# Exit Gate
class ExitGate:
    def __init__(self, gate_id: int, parking_lot: ParkingLot):
        self.gate_id = gate_id
        self.parking_lot = parking_lot
        self.cost_computation = CostComputation(HourlyPricingStrategy())
    
    def set_pricing_strategy(self, strategy: PriceStrategy):
        self.cost_computation.price_strategy = strategy
    
    def calculate_parking_fee(self, ticket_id: str) -> Optional[float]:
        ticket = self.parking_lot.get_ticket(ticket_id)
        
        if not ticket:
            print(f"Invalid ticket ID: {ticket_id}")
            return None
        
        exit_time = datetime.now()
        fee = self.cost_computation.calculate_cost(
            ticket.entry_time, 
            exit_time, 
            ticket.parking_spot.price_per_hour
        )
        
        print(f"Parking fee for ticket {ticket_id}: ${fee:.2f}")
        return fee
    
    def process_exit(self, ticket_id: str, payment_strategy: PaymentStrategy) -> bool:
        fee = self.calculate_parking_fee(ticket_id)
        
        if fee is None:
            return False
        
        ticket = self.parking_lot.get_ticket(ticket_id)
        
        if not payment_strategy.process_payment(fee):
            print(f"Payment failed for ticket {ticket_id}")
            return False
        
        # Release the parking spot
        parking_manager = self.parking_lot