import uuid
from bill import Bill
from enums import PaymentMode, BillStatus

class Payment:
    def __init__(self) -> None:
        self.payment_id: str = str(uuid.uuid4())
        self.bill: Bill | None = None
        self.payment_mode: PaymentMode | None = None

    def make_payment(self, bill: Bill, payment_mode: PaymentMode) -> None:
        self.bill = bill
        self.payment_mode = payment_mode
        bill.status = BillStatus.PAID
        print(f"Paid Rs {bill.amount} successfully using {payment_mode.value}.")
        print("Your Reservation is successful")
