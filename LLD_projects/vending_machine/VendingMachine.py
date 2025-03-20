from threading import Lock
from IdleState import IdleState
from ReadyState import ReadyState
from DispenseState import DispenseState
from ReturnState import ReturnState
from Inventory import Inventory
from VendingMachineInterface import VendingMachineInterface

class VendingMachine:
    _instance = None
    _lock = Lock()
    def __new__(cls):
        with cls._lock:
            if cls._instance == None:
                cls._instance = super().__new__(cls)
                cls._instance.idle_state = IdleState(cls._instance)
                cls._instance.ready_state = ReadyState(cls._instance)
                cls._instance.dispense_state = DispenseState(cls._instance)
                cls._instance.return_state = ReturnState(cls._instance)
                cls._instance.current_state = cls._instance.idle_state
                cls._instance.total_amount  = 0.0
                cls._instance.selected_product = None
                cls._instance.inventory = Inventory()
                cls._instance.vending_machine_interface = VendingMachineInterface()
            return cls._instance
        
    @classmethod
    def get_instance(cls):
        return cls()
    
    def set_state(self, state):
        self.current_state = state
    
    def select_product(self,product):
        self.current_state.select_product(product)

    def insert_coin(self,coin):
        self.current_state.insert_coin(coin)
    
    def insert_note(self,note):
        self.current_state.insert_note(note)
    
    def dispense_product(self):
        self.current_state.dispense_product()
    
    def return_change(self):
        self.current_state.return_change()
    
    def add_coin(self,coin):
        self.total_amount += coin.value
    
    def add_note(self,note):
        self.total_amount += note.value
    
    def reset_payment(self):
        self.total_amount = 0.0
    
    def reset_selected_product(self):
        self.selected_product = None
    
    def display_product(self):
        self.vending_machine_interface.display_product(self.inventory)

