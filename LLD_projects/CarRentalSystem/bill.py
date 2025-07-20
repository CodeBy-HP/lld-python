import uuid
from reservation import Reservation
from enums import BillStatus

class Bill:
    def __init__(self, reservation: Reservation) -> None:
        self.bill_id: str = str(uuid.uuid4())
        self.reservation: Reservation = reservation
        # For demonstration, set a fixed amount.
        # Real logic would calculate based on times & vehicle costs.
        self.amount: int = 100
        self.status: BillStatus = BillStatus.PENDING
