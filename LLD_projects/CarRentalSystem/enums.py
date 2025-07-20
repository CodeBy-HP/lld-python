from enum import Enum

class VehicleStatus(Enum):
    RENTED = "RENTED"
    AVAILABLE = "AVAILABLE"
    MAINTENANCE = "MAINTENANCE"

class VehicleType(Enum):
    CAR = "CAR"
    BIKE = "BIKE"

class ReservationStatus(Enum):
    SCHEDULED = "SCHEDULED"
    INPROGRESS = "INPROGRESS"
    COMPLETED = "COMPLETED"
    CANCELLED = "CANCELLED"

class ReservationType(Enum):
    DAILY = "DAILY"
    HOURLY = "HOURLY"

class BillStatus(Enum):
    PAID = "PAID"
    PENDING = "PENDING"

class PaymentMode(Enum):
    CARD = "CARD"
    UPI = "UPI"
    CASH = "CASH"
