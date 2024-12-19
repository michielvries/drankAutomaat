import os
import time
from decimal import Decimal

from app.vending_machine.models import Inventory, Drink, Maintenance


class VendingMachine:
    """A vending machine that dispenses drinks"""

    def __init__(self):
        self.inventory = Inventory()
        self.maintenance = Maintenance(self.inventory)

    def setup_stock(self):
        """Initializes the vending machine with some stock"""
        initial_stock = [
            ("Melk", 2.5, 10),
            ("Bier", 1.0, 5),
            ("Bier", 9.50, 3, "Alcoholvrij"),
            ("Karnemelk", 1.5, 7),
            ("Karnemelk", 1.8, 1, "met prik"),
        ]
        for drink in initial_stock:
            self.inventory.add_drink(Drink(*drink))

    def display_drinks(self) -> None:
        """Displays the available drinks"""
        for index, drink in enumerate(self.inventory.drinks.values(), start=1):
            status = f"{drink.quantity} beschikbaar" if drink.is_in_stock() else "UITVERKOCHT"
            naming = f"{drink.brand} {drink.subtype}" if drink.subtype else drink.brand
            print(f"{index}. {naming}: €{drink.price:.2f} - {status}")

    def select_drink(self) -> Drink | None:
        """Prompts the user to select a drink or enter maintenance mode"""
        drinks_list = list(self.inventory.drinks.values())
        clear_screen()

        while True:
            print("Beschikbare producten:")
            self.display_drinks()
            try:
                choice = input("\nVul het nummer van het product in: \n> ")

                # Open secret maintenance menu
                if choice == "adminadmin":
                    clear_screen()
                    self.maintenance.maintenance_menu()
                    break

                choice = int(choice) - 1
                if 0 <= choice < len(drinks_list):
                    selection: Drink = drinks_list[choice]
                    if not selection.is_in_stock():
                        print("Dit product is uitverkocht.")
                        time.sleep(2)
                        return None
                    clear_screen()
                    return selection
                else:
                    clear_screen()
                    print("Ongeldige keuze, probeer opnieuw.\n")
            except ValueError:
                clear_screen()
                print("Ongeldige keuze, probeer opnieuw.\n")

    def dispense_drink(self, drink):
        """Dispenses the selected drink"""
        self.inventory.reduce_amount(drink.brand, drink.subtype)

        # Simulate the drink dispensing
        print(f"{drink.brand} {drink.subtype} wordt uitgegeven...")
        time.sleep(1)
        print("bzzzzzzt")
        time.sleep(2)
        print("plok\n")
        time.sleep(2)
        print("Bedankt voor uw aankoop!\nTot ziens!\n")
        time.sleep(3)
        clear_screen()

    @staticmethod
    def insert_money(drink: Drink) -> float:
        """Inserts money into the vending machine"""
        total_inserted = 0
        coins = [0.1, 0.2, 0.5, 1.0, 2.0]

        while total_inserted < drink.price:
            print(f"Voer €{drink.price:.2f} in om {drink.brand} {drink.subtype} te kopen.\n")
            print("Opties:")
            for i, coin in enumerate(coins, start=1):
                print(f"{i}. €{coin:.2f}")
            print("0. Betaling annuleren")
            print(f"\nTotaal ingevoerd: €{total_inserted:.2f}\n")

            try:
                choice = int(input("Kies een munt: \n> "))
                clear_screen()
                if choice == 0:
                    print("Betaling geannuleerd.")
                    print(f"Uw geld wordt geretourneerd: €{total_inserted:.2f}")
                    time.sleep(4)
                    clear_screen()
                    return False
                if 0 < choice <= len(coins):
                    total_inserted += coins[choice - 1]
                else:
                    print("Ongeldige keuze, probeer opnieuw.\n")
            except ValueError:
                clear_screen()
                print("Ongeldige keuze, probeer opnieuw.\n")
        return total_inserted

    @staticmethod
    def return_change(drink: Drink, total_inserted: float):
        """Returns the change to the user"""
        change = Decimal(total_inserted) - Decimal(drink.price)

        # Check if the user inserted the exact amount
        if str(f"{change:.2f}") == "0.00":
            return

        # Simulate the change return
        print(f"Uw wisselgeld komt het bakje in rollen: €{change:.2f}")
        time.sleep(1)
        print("pling plong pling plong")
        time.sleep(2)
        print("pling\n")
        time.sleep(1)

    def start(self):
        """Starts the vending machine"""
        while True:
            drink = self.select_drink()

            # Make sure a drink was selected
            if drink is None:
                continue

            # Check if the user canceled the payment
            inserted = self.insert_money(drink)
            if not inserted:
                continue

            self.return_change(drink, inserted)
            self.dispense_drink(drink)


def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')
