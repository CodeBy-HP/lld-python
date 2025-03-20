from VendingMachine import VendingMachine

if __name__ == "__main__":
    vm = VendingMachine()

    vm.insert_money()
    vm.dispense()
    vm.refund()