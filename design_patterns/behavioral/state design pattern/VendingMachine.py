from threading import Lock
from NoMoneyState import NoMoneyState
from HasMoneyState import HasMoneyState

class VendingMachine:
    _instance = None
    _lock = Lock()

    def __new__(cls):
        with cls._lock:
            if cls._instance == None:
                cls._instance = super().__new__(cls)
                cls._instance.no_money_state = NoMoneyState(cls._instance)
                cls._instance.has_money_state = HasMoneyState(cls._instance)
                cls._instance.current_state = cls._instance.no_money_state
            return cls._instance
    
    @classmethod
    def get_instance(cls):
        return cls()
    
    def insert_money(self):
        return self.current_state.insert_money()
    
    def refund(self):
        return self.current_state.refund()
    
    def dispense(self):
        return self.current_state.dispense()
    
    def set_state(self, state):
        self.current_state = state
        