from datetime import datetime
from enums import VehicleType, VehicleStatus, ReservationType, PaymentMode
from vehicle import Car, Bike
from location import Location
from user import User
from store import Store
from vehicle_rental_system import VehicleRentalSystem
from bill import Bill
from payment import Payment

def main():
    # Create users
    user1 = User(1, "ABCD 20212365435")
    user2 = User(2, "EDFE 54324567896")

    # Create vehicles
    vehicle1 = Car(1)
    vehicle2 = Car(2)
    vehicle3 = Bike(3)
    vehicle4 = Bike(4)

    # Prepare vehicle lists for different stores
    vehicle_list1 = [vehicle1, vehicle2]
    vehicle_list2 = [vehicle3, vehicle4]

    # Create a location
    location1 = Location("Sector 135", "Noida", "UP", "India", 201304)

    # Create stores
    store1 = Store(1, location1, vehicle_list1)
    store2 = Store(2, location1, vehicle_list2)

    # Initialize the Vehicle Rental System
    rental_system = VehicleRentalSystem()
    rental_system.add_user(user1)
    rental_system.add_user(user2)
    rental_system.add_store(store1)
    rental_system.add_store(store2)

    # user1 wants to rent a Car in Noida
    matching_stores = rental_system.find_stores(location1)

    if not matching_stores:
        print("No stores found in this location.")
        return

    # Assume user chooses the first store
    chosen_store = matching_stores[0]

    # List all available Cars
    available_cars = chosen_store.get_all_vehicles(VehicleType.CAR)
    if not available_cars:
        print("No cars available at this store.")
        return

    # User reserves the first available car
    reserved_car = available_cars[0]
    pickup_time = datetime(2023, 6, 29, 5, 30)
    drop_time = datetime(2023, 6, 30, 22, 30)

    reservation = chosen_store.reserve_vehicle(
        user=user1,
        vehicle=reserved_car,
        pickup_time=pickup_time,
        drop_time=drop_time,
        drop_location=location1,
        reservation_type=ReservationType.DAILY
    )

    # Generate a bill for the reservation
    bill = Bill(reservation)

    # User makes payment
    payment = Payment()
    payment.make_payment(bill, PaymentMode.UPI)

    # Booking is confirmed
    # user comes to pick up vehicle
    reserved_car.set_vehicle_status(VehicleStatus.RENTED)

    # user drops the vehicle later
    chosen_store.complete_reservation(reservation)

if __name__ == "__main__":
    main()
