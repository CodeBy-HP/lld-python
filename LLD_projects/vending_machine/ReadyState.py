from VendingMachineState import VendingMachineState


class ReadyState(VendingMachineState):
    def select_product(self):
        print("The product already selected")

    def insert_coin(self, coin):
        self.vending_machine.add_coin(coin)
        if self.check_payment_status():
            print("Payment Sucessfull !!!")
            self.vending_machine.set_state(self.vending_machine.dispense_state)

    def insert_note(self, note):
        self.vending_machine.add_note(note)
        if self.check_payment_status():
            print("Payment Sucessfull !!!")
            self.vending_machine.set_state(self.vending_machine.dispense_state)

    def dispense_product(self):
        print("First insert the money")

    def return_change(self):
        change = (
            self.vending_machine.total_amount
            - self.vending_machine.selected_product.cost
        )
        if change > 0:
            print(f"Collect your Change {change :.2f}")
        else:
            print("No Change to Collect")
        self.vending_machine.total_amount = self.vending_machine.selected_product.cost

    def check_payment_status(self):
        if (
            self.vending_machine.total_amount
            >= self.vending_machine.selected_product.cost
        ):
            return True
        return False
