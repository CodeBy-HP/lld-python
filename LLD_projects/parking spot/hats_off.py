from abc import ABC, abstractmethod
from enum import Enum
from datetime import datetime
import uuid
import threading
import time
from typing import Dict, List, Optional, Tuple

# Custom Exception Hierarchy
class ParkingLotException(Exception):
    """Base exception for parking lot system"""
    pass

class NoSpotAvailableException(ParkingLotException):
    """Raised when no parking spot is available"""
    pass

class InvalidTicketException(ParkingLotException):
    """Raised when an invalid ticket is provided"""
    pass

class PaymentFailedException(ParkingLotException):
    """Raised when payment processing fails"""
    pass

# Enums for Vehicle and Customer Types
class VehicleType(Enum):
    BIKE = 1
    CAR = 2
    TRUCK = 3

class CustomerType(Enum):
    REGULAR = 1
    PREMIUM = 2
    VIP = 3

# Abstract Vehicle Class
class Vehicle(ABC):
    def __init__(self, license_plate: str, vehicle_type: VehicleType, 
                 customer_type: CustomerType = CustomerType.REGULAR):
        if not license_plate:
            raise ValueError("License plate cannot be empty")
        self.license_plate = license_plate
        self.vehicle_type = vehicle_type
        self.customer_type = customer_type

# Concrete Vehicle Classes
class Bike(Vehicle):
    def __init__(self, license_plate: str, customer_type: CustomerType = CustomerType.REGULAR):
        super().__init__(license_plate, VehicleType.BIKE, customer_type)

class Car(Vehicle):
    def __init__(self, license_plate: str, customer_type: CustomerType = CustomerType.REGULAR):
        super().__init__(license_plate, VehicleType.CAR, customer_type)

class Truck(Vehicle):
    def __init__(self, license_plate: str, customer_type: CustomerType = CustomerType.REGULAR):
        super().__init__(license_plate, VehicleType.TRUCK, customer_type)

# Abstract Parking Spot Class
class ParkingSpot(ABC):
    def __init__(self, spot_id: str, hourly_rate: float):
        self.spot_id = spot_id
        self.hourly_rate = hourly_rate
        self.is_occupied = False
        self.vehicle = None
        self.lock = threading.Lock()  # Thread safety

    @abstractmethod
    def can_accommodate(self, vehicle: Vehicle) -> bool:
        pass

    def occupy(self, vehicle: Vehicle) -> bool:
        with self.lock:
            if not self.is_occupied and self.can_accommodate(vehicle):
                self.vehicle = vehicle
                self.is_occupied = True
                return True
            return False

    def vacate(self) -> None:
        with self.lock:
            self.vehicle = None
            self.is_occupied = False

# Concrete Parking Spot Classes
class MotorcycleSpot(ParkingSpot):
    def __init__(self, spot_id: str):
        super().__init__(spot_id, hourly_rate=2.0)

    def can_accommodate(self, vehicle: Vehicle) -> bool:
        return vehicle.vehicle_type == VehicleType.BIKE

class CompactSpot(ParkingSpot):
    def __init__(self, spot_id: str):
        super().__init__(spot_id, hourly_rate=5.0)

    def can_accommodate(self, vehicle: Vehicle) -> bool:
        return vehicle.vehicle_type in {VehicleType.BIKE, VehicleType.CAR}

class LargeSpot(ParkingSpot):
    def __init__(self, spot_id: str):
        super().__init__(spot_id, hourly_rate=10.0)

    def can_accommodate(self, vehicle: Vehicle) -> bool:
        return True  # Can accommodate any vehicle type


# Allocation Strategy Interfaces
class ParkingStrategy(ABC):
    @abstractmethod
    def select_spot(self, spots: List[ParkingSpot], vehicle: Vehicle) -> Optional[ParkingSpot]:
        pass

class FirstAvailableStrategy(ParkingStrategy):
    def select_spot(self, spots: List[ParkingSpot], vehicle: Vehicle) -> Optional[ParkingSpot]:
        for spot in spots:
            if not spot.is_occupied and spot.can_accommodate(vehicle):
                return spot
        return None

class NearestEntranceStrategy(ParkingStrategy):
    def select_spot(self, spots: List[ParkingSpot], vehicle: Vehicle) -> Optional[ParkingSpot]:
        # Assuming spots are sorted by proximity to entrance
        return next((spot for spot in spots 
                   if not spot.is_occupied and spot.can_accommodate(vehicle)), None)

# Pricing Strategy Interfaces
class PricingStrategy(ABC):
    @abstractmethod
    def calculate_fee(self, entry_time: datetime, exit_time: datetime, 
                     spot: ParkingSpot, vehicle: Vehicle) -> float:
        pass

class HourlyPricing(PricingStrategy):
    def calculate_fee(self, entry_time: datetime, exit_time: datetime, 
                     spot: ParkingSpot, vehicle: Vehicle) -> float:
        duration_hours = max(0.5, (exit_time - entry_time).total_seconds() / 3600)
        return duration_hours * spot.hourly_rate

class DynamicPricing(PricingStrategy):
    def __init__(self, base_multiplier: float = 1.0, peak_multiplier: float = 1.5,
                 occupancy_threshold: float = 0.7):
        self.base_multiplier = base_multiplier
        self.peak_multiplier = peak_multiplier
        self.occupancy_threshold = occupancy_threshold
        
    def calculate_fee(self, entry_time: datetime, exit_time: datetime, 
                     spot: ParkingSpot, vehicle: Vehicle) -> float:
        # Base calculation
        duration_hours = max(0.5, (exit_time - entry_time).total_seconds() / 3600)
        base_fee = duration_hours * spot.hourly_rate * self.base_multiplier
        
        # Time-based adjustment (peak hours: 8-10AM, 5-7PM on weekdays)
        current_hour = exit_time.hour
        is_weekday = exit_time.weekday() < 5
        is_peak_time = is_weekday and ((8 <= current_hour < 10) or (17 <= current_hour < 19))
        
        multiplier = self.peak_multiplier if is_peak_time else 1.0
        
        # Customer type adjustment
        if vehicle.customer_type == CustomerType.PREMIUM:
            multiplier *= 0.9  # 10% discount
        elif vehicle.customer_type == CustomerType.VIP:
            multiplier *= 0.8  # 20% discount
            
        return base_fee * multiplier

# Payment Strategy Interfaces
class PaymentProcessor(ABC):
    @abstractmethod
    def process_payment(self, amount: float) -> bool:
        pass

class CreditCardProcessor(PaymentProcessor):
    def process_payment(self, amount: float) -> bool:
        print(f"Processing credit card payment: ${amount:.2f}")
        # In real implementation, this would call payment gateway
        return True  # Simplified for example

class MobileWalletProcessor(PaymentProcessor):
    def process_payment(self, amount: float) -> bool:
        print(f"Processing mobile wallet payment: ${amount:.2f}")
        # In real implementation, this would call payment gateway
        return True  # Simplified for example


# Ticket and Gate Classes
class Ticket:
    def __init__(self, vehicle: Vehicle, spot: ParkingSpot):
        self.ticket_id = str(uuid.uuid4())
        self.entry_time = datetime.now()
        self.exit_time = None
        self.vehicle = vehicle
        self.spot = spot
        self.fee_paid = 0.0
        self.payment_status = False

    def mark_paid(self, amount: float):
        self.exit_time = datetime.now()
        self.fee_paid = amount
        self.payment_status = True

class EntranceGate:
    def __init__(self, gate_id: int, parking_lot: 'ParkingLot'):
        self.gate_id = gate_id
        self.parking_lot = parking_lot
        
    def issue_ticket(self, vehicle: Vehicle) -> Ticket:
        spot = self.parking_lot.find_spot(vehicle)
        if not spot:
            raise NoSpotAvailableException(f"No spot available for {vehicle.vehicle_type.name}")
            
        if not spot.occupy(vehicle):
            raise NoSpotAvailableException("Failed to occupy spot")
            
        ticket = Ticket(vehicle, spot)
        self.parking_lot.add_ticket(ticket)
        self.parking_lot.notify("ENTRY", vehicle, spot)
        return ticket

class ExitGate:
    def __init__(self, gate_id: int, parking_lot: 'ParkingLot', 
                payment_processor: PaymentProcessor):
        self.gate_id = gate_id
        self.parking_lot = parking_lot
        self.payment_processor = payment_processor
        
    def process_exit(self, ticket_id: str) -> float:
        ticket = self.parking_lot.get_ticket(ticket_id)
        if not ticket:
            raise InvalidTicketException("Invalid ticket ID")
            
        fee = self.parking_lot.calculate_fee(ticket)
        
        if not self.payment_processor.process_payment(fee):
            raise PaymentFailedException("Payment processing failed")
            
        ticket.mark_paid(fee)
        ticket.spot.vacate()
        self.parking_lot.remove_ticket(ticket_id)
        self.parking_lot.notify("EXIT", ticket.vehicle, ticket.spot)
        
        return fee

# Observer Pattern Implementation
class ParkingObserver(ABC):
    @abstractmethod
    def update(self, event_type: str, vehicle: Vehicle, spot: ParkingSpot):
        pass

class DisplayObserver(ParkingObserver):
    def update(self, event_type: str, vehicle: Vehicle, spot: ParkingSpot):
        print(f"[{datetime.now()}] {event_type}: {vehicle.license_plate} "
              f"({vehicle.vehicle_type.name}) at spot {spot.spot_id}")

class OccupancyMonitor(ParkingObserver):
    def __init__(self, parking_lot: 'ParkingLot', threshold: float = 0.8):
        self.parking_lot = parking_lot
        self.threshold = threshold
        self.alert_triggered = False
        
    def update(self, event_type: str, vehicle: Vehicle, spot: ParkingSpot):
        occupancy = self.parking_lot.get_occupancy_rate()
        
        if occupancy > self.threshold and not self.alert_triggered:
            print(f"⚠️ ALERT: Parking lot occupancy at {occupancy:.1%} (threshold: {self.threshold:.1%})")
            self.alert_triggered = True
        elif occupancy <= self.threshold and self.alert_triggered:
            print(f"✓ CLEAR: Parking lot occupancy now at {occupancy:.1%}")
            self.alert_triggered = False


# Main Parking Lot Class - Singleton Pattern
class ParkingLot:
    _instance = None
    _lock = threading.Lock()
    
    def __new__(cls, *args, **kwargs):
        with cls._lock:
            if cls._instance is None:
                cls._instance = super(ParkingLot, cls).__new__(cls)
                cls._instance._initialized = False
            return cls._instance
    
    def __init__(self, name: str, motorcycle_spots: int = 10, 
                car_spots: int = 20, large_spots: int = 5):
        if self._initialized:
            return
            
        self.name = name
        self.spots = {
            VehicleType.BIKE: [MotorcycleSpot(f"M-{i}") for i in range(motorcycle_spots)],
            VehicleType.CAR: [CompactSpot(f"C-{i}") for i in range(car_spots)],
            VehicleType.TRUCK: [LargeSpot(f"L-{i}") for i in range(large_spots)]
        }
        
        self.parking_strategy = FirstAvailableStrategy()
        self.pricing_strategy = DynamicPricing()
        
        self.tickets = {}
        self.observers = []
        self.entrance_gates = []
        self.exit_gates = []
        
        self._initialized = True
    
    def add_entrance_gate(self) -> EntranceGate:
        gate = EntranceGate(len(self.entrance_gates) + 1, self)
        self.entrance_gates.append(gate)
        return gate
        
    def add_exit_gate(self, payment_processor: PaymentProcessor) -> ExitGate:
        gate = ExitGate(len(self.exit_gates) + 1, self, payment_processor)
        self.exit_gates.append(gate)
        return gate
    
    def register_observer(self, observer: ParkingObserver):
        self.observers.append(observer)
        
    def notify(self, event_type: str, vehicle: Vehicle, spot: ParkingSpot):
        for observer in self.observers:
            observer.update(event_type, vehicle, spot)
    
    def find_spot(self, vehicle: Vehicle) -> Optional[ParkingSpot]:
        # First try vehicle-specific spots
        if vehicle.vehicle_type == VehicleType.BIKE:
            if spot := self.parking_strategy.select_spot(self.spots[VehicleType.BIKE], vehicle):
                return spot
                
        # For cars, try car spots first
        if vehicle.vehicle_type == VehicleType.CAR:
            if spot := self.parking_strategy.select_spot(self.spots[VehicleType.CAR], vehicle):
                return spot
        
        # For any vehicle, try large spots as last resort
        return self.parking_strategy.select_spot(self.spots[VehicleType.TRUCK], vehicle)
    
    def add_ticket(self, ticket: Ticket):
        self.tickets[ticket.ticket_id] = ticket
        
    def get_ticket(self, ticket_id: str) -> Optional[Ticket]:
        return self.tickets.get(ticket_id)
        
    def remove_ticket(self, ticket_id: str):
        if ticket_id in self.tickets:
            del self.tickets[ticket_id]
    
    def calculate_fee(self, ticket: Ticket) -> float:
        exit_time = datetime.now() if not ticket.exit_time else ticket.exit_time
        return self.pricing_strategy.calculate_fee(
            ticket.entry_time, exit_time, ticket.spot, ticket.vehicle)
    
    def get_occupancy_rate(self) -> float:
        total_spots = sum(len(spots) for spots in self.spots.values())
        occupied_spots = sum(sum(1 for spot in spots if spot.is_occupied) 
                            for spots in self.spots.values())
        return occupied_spots / total_spots if total_spots > 0 else 0
        
    def get_status(self) -> Dict:
        available = {
            vt: sum(1 for spot in spots if not spot.is_occupied)
            for vt, spots in self.spots.items()
        }
        
        return {
            "name": self.name,
            "occupancy": f"{self.get_occupancy_rate():.1%}",
            "available_motorcycle_spots": available[VehicleType.BIKE],
            "available_car_spots": available[VehicleType.CAR],
            "available_large_spots": available[VehicleType.TRUCK],
            "active_tickets": len(self.tickets)
        }


# Loyalty Program - Surprise Feature 1
class LoyaltyProgram:
    def __init__(self):
        self.points = {}  # license_plate -> points
        self.customer_types = {}  # license_plate -> CustomerType
        self.lock = threading.Lock()
        
    def record_payment(self, license_plate: str, amount: float):
        with self.lock:
            if license_plate not in self.points:
                self.points[license_plate] = 0
                self.customer_types[license_plate] = CustomerType.REGULAR
                
            points_earned = int(amount)
            self.points[license_plate] += points_earned
            
            # Update customer type based on total points
            total_points = self.points[license_plate]
            if total_points >= 1000:
                self.customer_types[license_plate] = CustomerType.VIP
            elif total_points >= 500:
                self.customer_types[license_plate] = CustomerType.PREMIUM
                
            print(f"🎁 {license_plate} earned {points_earned} points! Total: {total_points}")
            
    def get_customer_type(self, license_plate: str) -> CustomerType:
        with self.lock:
            return self.customer_types.get(license_plate, CustomerType.REGULAR)

# Real-time Notification System - Surprise Feature 2
class NotificationSystem(ParkingObserver):
    def __init__(self):
        self.subscribers = {}  # license_plate -> notification_callback
        
    def subscribe(self, license_plate: str, callback):
        self.subscribers[license_plate] = callback
        
    def update(self, event_type: str, vehicle: Vehicle, spot: ParkingSpot):
        if vehicle.license_plate in self.subscribers:
            if event_type == "ENTRY":
                message = f"Your vehicle has been parked at spot {spot.spot_id}"
            elif event_type == "EXIT":
                message = f"Your vehicle has exited from spot {spot.spot_id}"
            else:
                message = f"Event {event_type} for your vehicle at spot {spot.spot_id}"
                
            # In real app, this would send an SMS, push notification, etc.
            print(f"📱 NOTIFICATION TO {vehicle.license_plate}: {message}")


def test_parking_system():
    # Initialize the parking lot with specific capacity
    parking_lot = ParkingLot("Downtown Premium Parking", 
                             motorcycle_spots=5, car_spots=3, large_spots=2)
    
    # Set up observers and special features
    display_observer = DisplayObserver()
    occupancy_monitor = OccupancyMonitor(parking_lot, threshold=0.7)
    loyalty_program = LoyaltyProgram()
    notification_system = NotificationSystem()
    
    # Register observers
    parking_lot.register_observer(display_observer)
    parking_lot.register_observer(occupancy_monitor)
    parking_lot.register_observer(notification_system)
    
    # Set up entrance and exit gates
    entrance_gate = parking_lot.add_entrance_gate()
    credit_card_exit = parking_lot.add_exit_gate(CreditCardProcessor())
    mobile_exit = parking_lot.add_exit_gate(MobileWalletProcessor())
    
    try:
        print("\n===== PARKING SYSTEM DEMO =====")
        print(f"Welcome to {parking_lot.name}!")
        print(f"Initial status: {parking_lot.get_status()}")
        
        # Create vehicles
        bike1 = Bike("M-1234")
        bike2 = Bike("M-5678")
        car1 = Car("C-1234")
        car2 = Car("C-5678")
        truck = Truck("T-1234")
        
        # Subscribe car1 owner to notifications
        notification_system.subscribe(car1.license_plate, lambda msg: None)
        
        # Park vehicles
        print("\n----- Parking Vehicles -----")
        tickets = []
        
        # Park bike 1
        ticket1 = entrance_gate.issue_ticket(bike1)
        tickets.append(ticket1)
        print(f"Bike 1 parked with ticket: {ticket1.ticket_id}")
        
        # Park bike 2
        ticket2 = entrance_gate.issue_ticket(bike2)
        tickets.append(ticket2)
        print(f"Bike 2 parked with ticket: {ticket2.ticket_id}")
        
        # Park car 1 (with notifications)
        ticket3 = entrance_gate.issue_ticket(car1)
        tickets.append(ticket3)
        print(f"Car 1 parked with ticket: {ticket3.ticket_id}")
        
        # Park car 2
        ticket4 = entrance_gate.issue_ticket(car2)
        tickets.append(ticket4)
        print(f"Car 2 parked with ticket: {ticket4.ticket_id}")
        
        # Current status
        print(f"\nCurrent status: {parking_lot.get_status()}")
        
        # Try to park truck (should fail as only large spots are full)
        try:
            truck_ticket = entrance_gate.issue_ticket(truck)
            print(f"Truck parked with ticket: {truck_ticket.ticket_id}")
        except NoSpotAvailableException as e:
            print(f"Expected error: {e}")
        
        # Simulate time passing (for pricing calculation)
        print("\n----- Simulating time passing (3 seconds) -----")
        time.sleep(3)
        
        # Exit some vehicles
        print("\n----- Exiting Vehicles -----")
        
        # Exit bike 1 with credit card
        fee1 = credit_card_exit.process_exit(ticket1.ticket_id)
        print(f"Bike 1 exited. Fee paid: ${fee1:.2f}")
        loyalty_program.record_payment(bike1.license_plate, fee1)
        
        # Exit car 1 with mobile wallet
        fee3 = mobile_exit.process_exit(ticket3.ticket_id)
        print(f"Car 1 exited. Fee paid: ${fee3:.2f}")
        loyalty_program.record_payment(car1.license_plate, fee3)
        
        # Updated status
        print(f"\nUpdated status: {parking_lot.get_status()}")
        
        # Now park the truck
        print("\n----- Parking Truck -----")
        truck_ticket = entrance_gate.issue_ticket(truck)
        print(f"Truck parked with ticket: {truck_ticket.ticket_id}")
        
        # Final status
        print(f"\nFinal status: {parking_lot.get_status()}")
        
        # Test error handling
        print("\n----- Testing Error Handling -----")
        
        # Invalid ticket
        try:
            credit_card_exit.process_exit("invalid-ticket-id")
        except InvalidTicketException as e:
            print(f"✓ Correctly caught: {e}")
        
        # Advanced loyalty program demo
        print("\n----- Loyalty Program Demo -----")
        # Simulate many visits for a VIP customer
        vip_plate = "VIP-1000"
        loyalty_program.record_payment(vip_plate, 200)
        loyalty_program.record_payment(vip_plate, 300)
        loyalty_program.record_payment(vip_plate, 500)
        
        # Create a VIP customer vehicle
        vip_car = Car(vip_plate, loyalty_program.get_customer_type(vip_plate))
        print(f"VIP car customer type: {vip_car.customer_type}")
        
        # Park VIP car
        vip_ticket = entrance_gate.issue_ticket(vip_car)
        print(f"VIP car parked with ticket: {vip_ticket.ticket_id}")
        
        # Exit VIP car to show discount
        time.sleep(1)
        vip_fee = credit_card_exit.process_exit(vip_ticket.ticket_id)
        print(f"VIP car exited. Discounted fee: ${vip_fee:.2f}")
        
    except Exception as e:
        print(f"ERROR: {e}")

if __name__ == "__main__":
    test_parking_system()
