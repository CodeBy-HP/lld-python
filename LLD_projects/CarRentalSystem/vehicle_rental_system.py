from typing import List
from user import User
from store import Store
from location import Location

class VehicleRentalSystem:
    def __init__(self) -> None:
        self.users: List[User] = []
        self.stores: List[Store] = []

    def add_user(self, user: User) -> None:
        self.users.append(user)

    def remove_user(self, user: User) -> None:
        if user in self.users:
            self.users.remove(user)

    def add_store(self, store: Store) -> None:
        self.stores.append(store)

    def remove_store(self, store: Store) -> None:
        if store in self.stores:
            self.stores.remove(store)

    def find_stores(self, location: Location) -> List[Store]:
        """
        In a real system, you would filter by location or distance.
        Here, we filter by city for simplicity.
        """
        return [store for store in self.stores if store.location.city == location.city]
