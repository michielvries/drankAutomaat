from app.vending_machine.machine import VendingMachine


def start_app():
    vending_machine = VendingMachine()
    vending_machine.setup_stock()
    vending_machine.start()


if __name__ == "__main__":
    start_app()
