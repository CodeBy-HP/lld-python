import uuid
from datetime import datetime
from enums import ReservationStatus, ReservationType
from user import User
from vehicle import Vehicle
from location import Location

class Reservation:
    def __init__(
        self,
        user: User,
        vehicle: Vehicle,
        pickup_time: datetime,
        pickup_location: Location,
        drop_time: datetime,
        drop_location: Location,
        reservation_type: ReservationType
    ) -> None:
        self.r_id: str = str(uuid.uuid4())
        self.user: User = user
        self.vehicle: Vehicle = vehicle
        self.pickup_time: datetime = pickup_time
        self.drop_time: datetime = drop_time
        self.pickup_location: Location = pickup_location
        self.drop_location: Location = drop_location
        self.status: ReservationStatus = ReservationStatus.SCHEDULED
        self.reservation_type: ReservationType = reservation_type

    def set_reservation_status(self, status: ReservationStatus) -> None:
        self.status = status
