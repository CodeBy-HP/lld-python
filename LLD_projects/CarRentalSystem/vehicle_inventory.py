from typing import List
from enums import VehicleType, VehicleStatus
from vehicle import Vehicle

class VehicleInventory:
    def __init__(self, vehicles: List[Vehicle]) -> None:
        self.vehicles: List[Vehicle] = vehicles

    def get_available_vehicles(self, vehicle_type: VehicleType) -> List[Vehicle]:
        """
        Return vehicles whose status is AVAILABLE and whose VehicleType matches.
        """
        available = []
        for v in self.vehicles:
            if v.type == vehicle_type and v.status == VehicleStatus.AVAILABLE:
                available.append(v)
        return available

    def add_vehicle(self, vehicle: Vehicle) -> None:
        self.vehicles.append(vehicle)

    def remove_vehicle(self, vehicle: Vehicle) -> None:
        if vehicle in self.vehicles:
            self.vehicles.remove(vehicle)
