from typing import List
from datetime import datetime
from location import Location
from vehicle import Vehicle
from vehicle_inventory import VehicleInventory
from user import User
from enums import VehicleType, VehicleStatus, ReservationType
from reservation import Reservation

class Store:
    def __init__(self, store_id: int, location: Location, vehicles: List[Vehicle]) -> None:
        self.store_id: int = store_id
        self.location: Location = location
        self.vehicle_inventory: VehicleInventory = VehicleInventory(vehicles)
        self.reservations: List[Reservation] = []

    def get_all_vehicles(self, vehicle_type: VehicleType) -> List[Vehicle]:
        return self.vehicle_inventory.get_available_vehicles(vehicle_type)

    def reserve_vehicle(
        self,
        user: User,
        vehicle: Vehicle,
        pickup_time: datetime,
        drop_time: datetime,
        drop_location: Location,
        reservation_type: ReservationType = ReservationType.DAILY
    ) -> Reservation:
        reservation = Reservation(
            user=user,
            vehicle=vehicle,
            pickup_time=pickup_time,
            pickup_location=self.location,
            drop_time=drop_time,
            drop_location=drop_location,
            reservation_type=reservation_type
        )
        self.reservations.append(reservation)
        return reservation

    def complete_reservation(self, reservation: Reservation) -> None:
        # Remove the completed reservation from the list of reservations
        if reservation in self.reservations:
            self.reservations.remove(reservation)
        reservation.vehicle.set_vehicle_status(VehicleStatus.AVAILABLE)
        print("Vehicle is dropped at store")
