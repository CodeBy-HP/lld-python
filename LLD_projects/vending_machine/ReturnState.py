from VendingMachineState import VendingMachineState

class ReturnState(VendingMachineState):
    def select_product(self):
        print("The product already selected collect the change")

    def insert_coin(self):
        print("Already have money collect the change")

    def insert_note(self):
        print("Already have money collect the change")

    def dispense_product(self):
        print("The product Already dispensed collect the Change")

    def return_change(self):
        change = self.vending_machine.total_amount - self.vending_machine.selected_product.cost
        if change > 0:
            print(f"Collect your Change ${change :.2f}")
        else:
            print("No Change to Collect")
        self.vending_machine.reset_payment()
        self.vending_machine.reset_selected_product()
        self.vending_machine.set_state(self.vending_machine.idle_state)


