from State import State

class HasMoneyState(State):
    def insert_money(self):
        print("Already have Money")

    def refund(self):
        print("Refunding the money")
        self.vending_machine.set_state(self.vending_machine.no_money_state)

    def dispense(self):
        print("Dispensing the product")
        self.vending_machine.set_state(self.vending_machine.no_money_state)
