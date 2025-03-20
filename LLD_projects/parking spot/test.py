# Import required modules from the parking lot system
from parking_lot_system import (
    ParkingLot, VehicleFactory, 
    CreditCardPaymentStrategy, CashPaymentStrategy, UPIPaymentStrategy,
    HourlyPricingStrategy, DailyPricingStrategy
)
import time
from datetime import datetime, timedelta

def test_parking_lot_system():
    print("=" * 50)
    print("PARKING LOT SYSTEM TEST")
    print("=" * 50)
    
    # 1. Initialize parking lot
    print("\n1. Initializing parking lot...")
    parking_lot = ParkingLot("Downtown Parking")
    parking_lot.initialize_parking_lot(two_wheeler_spots=5, four_wheeler_spots=10)
    
    # 2. Create vehicles
    print("\n2. Creating vehicles...")
    bike1 = VehicleFactory.create_vehicle("bike", "B-1001")
    bike2 = VehicleFactory.create_vehicle("bike", "B-1002")
    car1 = VehicleFactory.create_vehicle("car", "C-5001")
    car2 = VehicleFactory.create_vehicle("car", "C-5002")
    truck1 = VehicleFactory.create_vehicle("truck", "T-7001")
    
    # 3. Park vehicles and get tickets
    print("\n3. Parking vehicles...")
    entrance_gate = parking_lot.entrance_gates[0]
    
    ticket_bike1 = entrance_gate.generate_ticket(bike1)
    ticket_bike2 = entrance_gate.generate_ticket(bike2)
    ticket_car1 = entrance_gate.generate_ticket(car1)
    ticket_car2 = entrance_gate.generate_ticket(car2)
    ticket_truck1 = entrance_gate.generate_ticket(truck1)
    
    # 4. Try to park more vehicles than capacity
    print("\n4. Testing parking capacity limits...")
    # Create more bikes than spots available
    for i in range(3, 10):
        bike = VehicleFactory.create_vehicle("bike", f"B-100{i}")
        ticket = entrance_gate.generate_ticket(bike)
        if ticket is None:
            print(f"No space available for bike B-100{i} as expected")
    
    # 5. Process exit for different vehicles with different payment methods
    print("\n5. Processing exits with different payment methods...")
    exit_gate = parking_lot.exit_gates[0]
    
    # Wait for some time to simulate parking duration
    print("\nSimulating parking duration (5 seconds)...")
    time.sleep(5)
    
    # Process exit for bike1 with credit card
    print("\nProcessing exit for bike1 with credit card...")
    credit_card_payment = CreditCardPaymentStrategy("1234-5678-9012-3456", "12/25", "123")
    exit_gate.process_exit(ticket_bike1.ticket_id, credit_card_payment)
    
    # Process exit for car1 with cash
    print("\nProcessing exit for car1 with cash...")
    cash_payment = CashPaymentStrategy()
    exit_gate.process_exit(ticket_car1.ticket_id, cash_payment)
    
    # Process exit for truck1 with UPI
    print("\nProcessing exit for truck1 with UPI...")
    upi_payment = UPIPaymentStrategy("user@upi")
    exit_gate.process_exit(ticket_truck1.ticket_id, upi_payment)
    
    # 6. Test different pricing strategies
    print("\n6. Testing different pricing strategies...")
    # Set daily pricing strategy
    exit_gate.set_pricing_strategy(DailyPricingStrategy())
    print("\nUsing daily pricing strategy for car2...")
    exit_gate.process_exit(ticket_car2.ticket_id, cash_payment)
    
    # Reset to hourly pricing
    exit_gate.set_pricing_strategy(HourlyPricingStrategy())
    print("\nReset to hourly pricing strategy for bike2...")
    exit_gate.process_exit(ticket_bike2.ticket_id, credit_card_payment)
    
    # 7. Test invalid ticket ID
    print("\n7. Testing invalid ticket ID...")
    exit_gate.calculate_parking_fee("invalid-ticket-id")
    
    # 8. Test parking again after spots are freed
    print("\n8. Testing parking after spots are freed...")
    new_bike = VehicleFactory.create_vehicle("bike", "B-2001")
    new_car = VehicleFactory.create_vehicle("car", "C-6001")
    
    ticket_new_bike = entrance_gate.generate_ticket(new_bike)
    ticket_new_car = entrance_gate.generate_ticket(new_car)
    
    print("\n9. Verifying ticket status...")
    active_tickets = len(parking_lot.issued_tickets)
    closed_tickets = len(parking_lot.closed_tickets)
    print(f"Active tickets: {active_tickets}")
    print(f"Closed tickets: {closed_tickets}")
    
    print("\n" + "=" * 50)
    print("PARKING LOT SYSTEM TEST COMPLETED")
    print("=" * 50)

if __name__ == "__main__":
    test_parking_lot_system()