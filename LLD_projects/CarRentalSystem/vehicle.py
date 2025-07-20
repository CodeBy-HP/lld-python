from datetime import datetime
from typing import Optional
from enums import VehicleType, VehicleStatus

class Vehicle:
    def __init__(
        self,
        vehicle_id: int,
        vehicle_type: VehicleType
    ) -> None:
        self.vehicle_id: int = vehicle_id
        self.vehicle_no: int = 0
        self.company: str = ""
        self.model_name: str = ""
        self.kms_driven: int = 0
        self.manufacturing_date: Optional[datetime] = None
        self.average: int = 0
        self.cc: int = 0
        self.daily_rental_cost: int = 0
        self.hourly_rental_cost: int = 0
        self.no_of_seats: int = 0
        self.status: VehicleStatus = VehicleStatus.AVAILABLE
        self.type: VehicleType = vehicle_type

    def update_rental_cost(self, daily_rental_cost: int, hourly_rental_cost: int) -> None:
        self.daily_rental_cost = daily_rental_cost
        self.hourly_rental_cost = hourly_rental_cost

    def set_vehicle_status(self, status: VehicleStatus) -> None:
        self.status = status

    def update_distance_travelled(self, distance: int) -> None:
        self.kms_driven += distance


class Bike(Vehicle):
    def __init__(self, vehicle_id: int) -> None:
        super().__init__(vehicle_id, VehicleType.BIKE)


class Car(Vehicle):
    def __init__(self, vehicle_id: int) -> None:
        super().__init__(vehicle_id, VehicleType.CAR)
