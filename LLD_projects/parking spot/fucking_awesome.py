from abc import ABC, abstractmethod
from enum import Enum
from datetime import datetime
import uuid
import threading
import time
from typing import List, Optional, Dict

# -----------------------------------------------------------------------------
# EXCEPTIONS
# -----------------------------------------------------------------------------

class ParkingLotException(Exception):
    """Base class for parking lot system exceptions."""
    pass

class NoSpotAvailableException(ParkingLotException):
    """Raised when no suitable parking spot is available."""
    pass

class InvalidTicketException(ParkingLotException):
    """Raised when an invalid parking ticket is presented."""
    pass

class PaymentFailedException(ParkingLotException):
    """Raised when payment processing encounters an error."""
    pass

# -----------------------------------------------------------------------------
# ENUMS
# -----------------------------------------------------------------------------

class VehicleType(Enum):
    """Enumerates the types of vehicles."""
    BIKE = 1
    CAR = 2
    TRUCK = 3

# -----------------------------------------------------------------------------
# DOMAIN MODELS
# -----------------------------------------------------------------------------

class Vehicle(ABC):
    """
    Abstract base class for vehicles.
    Defines common properties and behavior for all vehicle types.
    """
    def __init__(self, license_plate: str, vehicle_type: VehicleType):
        if not license_plate:
            raise ValueError("License plate cannot be empty.")
        self.license_plate = license_plate
        self.vehicle_type = vehicle_type

class Bike(Vehicle):
    """Represents a motorcycle or bicycle."""
    def __init__(self, license_plate: str):
        super().__init__(license_plate, VehicleType.BIKE)

class Car(Vehicle):
    """Represents a standard passenger car."""
    def __init__(self, license_plate: str):
        super().__init__(license_plate, VehicleType.CAR)

class Truck(Vehicle):
    """Represents a large vehicle such as a truck or bus."""
    def __init__(self, license_plate: str):
        super().__init__(license_plate, VehicleType.TRUCK)

class ParkingSpot(ABC):
    """
    Abstract base class for parking spots.
    Defines properties and methods common to all parking spot types.
    """
    def __init__(self, spot_id: int, price_per_hour: float):
        self.spot_id = spot_id
        self.is_empty = True
        self.price_per_hour = price_per_hour
        self.lock = threading.Lock()  # Ensure thread-safe operations

    @abstractmethod
    def can_accommodate(self, vehicle: Vehicle) -> bool:
        """Abstract method to check if the spot can accommodate a given vehicle."""
        pass

    def occupy(self, vehicle: Vehicle) -> bool:
        """
        Occupy the parking spot with a vehicle.
        Returns True if successful, False otherwise.
        """
        with self.lock:  # Acquire lock for thread safety
            if self.is_empty and self.can_accommodate(vehicle):
                self.is_empty = False
                return True
            return False

    def vacate(self) -> None:
        """Vacate the parking spot, making it available."""
        with self.lock:  # Acquire lock for thread safety
            self.is_empty = True

class TwoWheelerSpot(ParkingSpot):
    """Represents a parking spot suitable for two-wheeled vehicles."""
    def __init__(self, spot_id: int):
        super().__init__(spot_id, price_per_hour=2.0)

    def can_accommodate(self, vehicle: Vehicle) -> bool:
        """Checks if the spot can accommodate a two-wheeled vehicle."""
        return vehicle.vehicle_type == VehicleType.BIKE

class FourWheelerSpot(ParkingSpot):
    """Represents a parking spot suitable for four-wheeled vehicles."""
    def __init__(self, spot_id: int):
        super().__init__(spot_id, price_per_hour=5.0)

    def can_accommodate(self, vehicle: Vehicle) -> bool:
        """Checks if the spot can accommodate a four-wheeled vehicle."""
        return vehicle.vehicle_type in (VehicleType.CAR, VehicleType.BIKE) #Bikes allowed in four wheeler spots

class LargeSpot(ParkingSpot):
    """Represents a large parking spot suitable for trucks and buses."""
    def __init__(self, spot_id: int):
        super().__init__(spot_id, price_per_hour=8.0) #Trucks are more costly

    def can_accommodate(self, vehicle: Vehicle) -> bool:
        """Checks if the spot can accommodate the given vehicle (always True)."""
        return True

class Ticket:
    """Represents a parking ticket."""
    def __init__(self, vehicle: Vehicle, spot: ParkingSpot):
        self.ticket_id = str(uuid.uuid4())
        self.vehicle = vehicle
        self.spot = spot
        self.entry_time = datetime.now()

    def __repr__(self):
        return f"Ticket(id={self.ticket_id}, vehicle={self.vehicle.license_plate}, spot={self.spot.spot_id})"

# -----------------------------------------------------------------------------
# STRATEGIES
# -----------------------------------------------------------------------------

class ParkingStrategy(ABC):
    """Abstract base class for parking allocation strategies."""
    @abstractmethod
    def find_parking_spot(self, spots: List[ParkingSpot], vehicle: Vehicle) -> Optional[ParkingSpot]:
        """Abstract method to find a suitable parking spot for a vehicle."""
        pass

class FirstAvailableStrategy(ParkingStrategy):
    """Strategy to find the first available spot that can accommodate the vehicle."""
    def find_parking_spot(self, spots: List[ParkingSpot], vehicle: Vehicle) -> Optional[ParkingSpot]:
        """Finds the first available spot in the list."""
        for spot in spots:
            if spot.is_empty and spot.can_accommodate(vehicle):
                return spot
        return None

class PricingStrategy(ABC):
    """Abstract base class for pricing strategies."""
    @abstractmethod
    def calculate_fee(self, entry_time: datetime, exit_time: datetime, spot: ParkingSpot) -> float:
        """Abstract method to calculate the parking fee."""
        pass

class HourlyPricingStrategy(PricingStrategy):
    """Calculates parking fee based on hourly rate."""
    def calculate_fee(self, entry_time: datetime, exit_time: datetime, spot: ParkingSpot) -> float:
        """Calculates fee based on hourly rate and duration."""
        duration_hours = max(0.5, (exit_time - entry_time).total_seconds() / 3600)
        return duration_hours * spot.price_per_hour

class PaymentStrategy(ABC):
    """Abstract base class for payment processing strategies."""
    @abstractmethod
    def process_payment(self, amount: float) -> bool:
        """Abstract method to process a payment."""
        pass

class CreditCardPaymentStrategy(PaymentStrategy):
    """Processes payments using a credit card."""
    def process_payment(self, amount: float) -> bool:
        """Simulates credit card payment processing."""
        print(f"Processing credit card payment: ${amount:.2f}")
        return True

class CashPaymentStrategy(PaymentStrategy):
    """Processes payments using cash."""
    def process_payment(self, amount: float) -> bool:
        """Simulates cash payment processing."""
        print(f"Processing cash payment: ${amount:.2f}")
        return True

# -----------------------------------------------------------------------------
# PARKING LOT COMPONENTS
# -----------------------------------------------------------------------------

class EntranceGate:
    """
    Represents an entrance gate to the parking lot.
    Handles the creation and assignment of parking tickets.
    """
    def __init__(self, gate_id: int, parking_lot: 'ParkingLot'):
        """Initializes the EntranceGate with a unique ID and a reference to the ParkingLot."""
        self.gate_id = gate_id
        self.parking_lot = parking_lot

    def generate_ticket(self, vehicle: Vehicle) -> Ticket:
        """Generates a parking ticket for the given vehicle."""
        spot = self.parking_lot.find_parking_space(vehicle)
        if not spot:
            raise NoSpotAvailableException("No parking spot available.")
        if not spot.occupy(vehicle):
             raise NoSpotAvailableException("Race condition happened.")
        ticket = Ticket(vehicle, spot)
        self.parking_lot.add_ticket(ticket)
        return ticket

class ExitGate:
    """
    Represents an exit gate from the parking lot.
    Handles payment processing and spot release.
    """
    def __init__(self, gate_id: int, parking_lot: 'ParkingLot', payment_strategy: PaymentStrategy):
        """
        Initializes the ExitGate with a unique ID, a reference to the ParkingLot,
        and a PaymentStrategy.
        """
        self.gate_id = gate_id
        self.parking_lot = parking_lot
        self.payment_strategy = payment_strategy

    def process_exit(self, ticket_id: str) -> float:
        """Processes the exit of a vehicle, handling payment and spot release."""
        ticket = self.parking_lot.get_ticket(ticket_id)
        if not ticket:
            raise InvalidTicketException("Invalid ticket ID.")

        fee = self.parking_lot.calculate_fee(ticket)
        if not self.payment_strategy.process_payment(fee):
            raise PaymentFailedException("Payment processing failed.")
        ticket.spot.vacate()
        self.parking_lot.remove_ticket(ticket_id)
        return fee

# -----------------------------------------------------------------------------
# PARKING LOT CORE
# -----------------------------------------------------------------------------

class ParkingLot:
    """
    Manages the parking lot operations, including spot allocation,
    ticket management, and fee calculation.
    """
    def __init__(self, name: str, num_two_wheeler_spots: int = 10, num_four_wheeler_spots: int = 20, num_large_spots: int = 5):
        """
        Initializes the ParkingLot with its name and the number of spots
        for each vehicle type.
        """
        self.name = name
        self.two_wheeler_spots = [TwoWheelerSpot(i) for i in range(num_two_wheeler_spots)]
        self.four_wheeler_spots = [FourWheelerSpot(i) for i in range(num_four_wheeler_spots)]
        self.large_spots = [LargeSpot(i) for i in range(num_large_spots)]
        self.tickets: Dict[str, Ticket] = {}  # Use a dictionary for faster ticket retrieval
        self.parking_strategy: ParkingStrategy = FirstAvailableStrategy()
        self.pricing_strategy: PricingStrategy = HourlyPricingStrategy()
        self.entrance_gates: List[EntranceGate] = []
        self.exit_gates: List[ExitGate] = []

    def add_entrance_gate(self) -> EntranceGate:
        """Adds an entrance gate to the parking lot."""
        gate_id = len(self.entrance_gates) + 1
        gate = EntranceGate(gate_id, self)
        self.entrance_gates.append(gate)
        return gate

    def add_exit_gate(self, payment_strategy: PaymentStrategy) -> ExitGate:
        """Adds an exit gate to the parking lot."""
        gate_id = len(self.exit_gates) + 1
        gate = ExitGate(gate_id, self, payment_strategy)
        self.exit_gates.append(gate)
        return gate

    def find_parking_space(self, vehicle: Vehicle) -> Optional[ParkingSpot]:
        """Finds a suitable parking spot for a given vehicle."""
        if vehicle.vehicle_type == VehicleType.BIKE:
            spots = self.two_wheeler_spots
        elif vehicle.vehicle_type == VehicleType.CAR:
            spots = self.four_wheeler_spots
        elif vehicle.vehicle_type == VehicleType.TRUCK:
            spots = self.large_spots
        else:
            raise ValueError("Invalid Vehicle Type!")

        # Apply parking strategy
        for spot in spots:
           if spot.is_empty and spot.can_accommodate(vehicle):
                return spot
        return None
    def add_ticket(self, ticket: Ticket) -> None:
        """Adds a parking ticket to the list of issued tickets."""
        self.tickets[ticket.ticket_id] = ticket

    def get_ticket(self, ticket_id: str) -> Optional[Ticket]:
        """Retrieves a ticket by its ID."""
        return self.tickets.get(ticket_id)

    def remove_ticket(self, ticket_id: str) -> None:
        """Removes a ticket from the list of issued tickets."""
        if ticket_id in self.tickets:
            del self.tickets[ticket_id]

    def calculate_fee(self, ticket: Ticket) -> float:
        """Calculates the parking fee for a given ticket."""
        exit_time = datetime.now()  # Capture exit time
        return self.pricing_strategy.calculate_fee(ticket.entry_time, exit_time, ticket.spot)
# -----------------------------------------------------------------------------
# CLIENT CODE / TESTING
# -----------------------------------------------------------------------------

def test_parking_lot():
    """Tests the parking lot system."""
    # ----------------------- Setup -----------------------
    # Create parking lot
    parking_lot = ParkingLot("City Center Parking", num_two_wheeler_spots=5, num_four_wheeler_spots=5, num_large_spots=2)

    # Add entrance and exit gates
    entrance_gate = parking_lot.add_entrance_gate()
    credit_exit = parking_lot.add_exit_gate(CreditCardPaymentStrategy())
    cash_exit = parking_lot.add_exit_gate(CashPaymentStrategy())

    # Create vehicles
    bike1 = Bike("B-100")
    bike2 = Bike("B-200")
    car1 = Car("C-100")
    car2 = Car("C-200")
    truck1 = Truck("T-100")
    truck2 = Truck("T-200")

    # ----------------------- Parking Simulation -----------------------
    print("--- Parking Simulation ---")
    
    # Park vehicles
    try:
        ticket_bike1 = entrance_gate.generate_ticket(bike1)
        print(f"{bike1.license_plate} parked. Ticket: {ticket_bike1.ticket_id}")
        ticket_bike2 = entrance_gate.generate_ticket(bike2)
        print(f"{bike2.license_plate} parked. Ticket: {ticket_bike2.ticket_id}")

        ticket_car1 = entrance_gate.generate_ticket(car1)
        print(f"{car1.license_plate} parked. Ticket: {ticket_car1.ticket_id}")
        ticket_car2 = entrance_gate.generate_ticket(car2)
        print(f"{car2.license_plate} parked. Ticket: {ticket_car2.ticket_id}")

        ticket_truck1 = entrance_gate.generate_ticket(truck1)
        print(f"{truck1.license_plate} parked. Ticket: {ticket_truck1.ticket_id}")
    except NoSpotAvailableException as e:
        print(f"Error parking: {e}")

    # Try to park when full
    try:
        ticket_truck2 = entrance_gate.generate_ticket(truck2)
        print(f"Parked {truck2.license_plate} with ticket {ticket_truck2.ticket_id}")
    except NoSpotAvailableException as e:
        print(f"Expected: {e}")

    # ----------------------- Exiting Simulation -----------------------
    print("\n--- Exiting Simulation ---")

    # Vehicles exiting
    try:
        fee_bike1 = credit_exit.process_exit(ticket_bike1.ticket_id)
        print(f"{bike1.license_plate} exited. Fee: ${fee_bike1:.2f}")

        fee_car1 = cash_exit.process_exit(ticket_car1.ticket_id)
        print(f"{car1.license_plate} exited. Fee: ${fee_car1:.2f}")
    except InvalidTicketException as e:
        print(f"Error exiting: {e}")

    # ----------------------- Error Handling Simulation -----------------------
    print("\n--- Error Handling ---")
    try:
        invalid_fee = credit_exit.process_exit("INVALID_TICKET")
        print(f"Exit processed: {invalid_fee}")  # Should not execute
    except InvalidTicketException as e:
        print(f"Expected: {e}")

if __name__ == "__main__":
    test_parking_lot()
