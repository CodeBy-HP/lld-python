class Location:
    def __init__(
        self,
        address: str,
        city: str,
        state: str,
        country: str,
        pin_code: int
    ) -> None:
        self.address: str = address
        self.city: str = city
        self.state: str = state
        self.country: str = country
        self.pin_code: int = pin_code
