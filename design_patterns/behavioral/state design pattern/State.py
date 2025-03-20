from abc import ABC, abstractmethod


class State(ABC):
    def __init__(self, vending_machine):
        self.vending_machine = vending_machine

    @abstractmethod
    def insert_money(self):
        pass

    @abstractmethod
    def refund(self):
        pass

    @abstractmethod
    def dispense(self):
        pass
