from State import State

class NoMoneyState(State):
    def insert_money(self):
        print("Inserting the money")
        self.vending_machine.set_state(self.vending_machine.has_money_state)

    def refund(self):
        print("No money to refund")

    def dispense(self):
        print("Insert the money")

    

