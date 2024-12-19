import os


class Drink:
    MAX_STOCK = 10

    def __init__(self, brand: str, price: float, quantity: int, subtype: str = ""):
        self.brand: str = brand
        self.subtype: str = subtype
        self.price: float = price
        self.quantity: int = quantity

    def is_in_stock(self) -> bool:
        return self.quantity > 0

    def reduce_stock(self, amount: int):
        if amount < 0:
            raise ValueError("Amount must be a positive number")
        if amount > self.quantity:
            raise ValueError(f"Not enough items of product {self.brand} {self.subtype} in stock")
        self.quantity -= amount

    def increase_stock(self, amount: int):
        """Increases the stock of a drink"""
        if self.quantity + amount > self.MAX_STOCK:
            raise ValueError(f"Can't have more than {self.MAX_STOCK} products of {self.brand} {self.subtype}")
        self.quantity += amount

    def change_stock(self, amount: int) -> bool:
        """Changes the stock of a drink"""
        if amount > self.MAX_STOCK:
            raise ValueError(f"Can't have more than {self.MAX_STOCK} products of {self.brand} {self.subtype}")
        self.quantity = amount
        return True


class Inventory:
    def __init__(self):
        self.drinks = {}

    def add_drink(self, drink: Drink):
        """Adds a new drink to the inventory"""
        key = (drink.brand, drink.subtype)
        if key in self.drinks:
            raise ValueError(f"Drink {drink.brand} {drink.subtype} already exists in the inventory")
        self.drinks[key] = drink

    def get_drink(self, brand: str, subtype: str = "") -> Drink:
        """Returns a drink from the inventory"""
        key = (brand, subtype)
        if key not in self.drinks:
            raise ValueError(f"Drink {brand} {subtype} does not exist in the inventory")
        return self.drinks[key]

    def reduce_amount(self, brand: str, subtype: str = "", amount: int = 1):
        """Reduces the amount of a drink in the inventory"""
        drink = self.get_drink(brand, subtype)
        drink.reduce_stock(amount)

    def is_in_stock(self, brand: str, subtype: str = "") -> bool:
        """Checks if a drink is in stock"""
        drink = self.get_drink(brand, subtype)
        return drink.is_in_stock()


class Maintenance:
    def __init__(self, inventory: Inventory):
        self.inventory = inventory

    def _add_drink(self, drink: Drink):
        self.inventory.add_drink(drink)

    def _remove_drink(self, brand: str, subtype: str = ""):
        self.inventory.drinks.pop((brand, subtype), None)  # Remove drink from inventory else None

    def _display_inventory(self):
        for i, drink in enumerate(self.inventory.drinks.values(), start=1):
            print(f"{i}. {drink.brand} {drink.subtype}: {drink.quantity} beschikbaar")

    def _display_prices(self):
        for i, drink in enumerate(self.inventory.drinks.values(), start=1):
            print(f"{i}. {drink.brand} {drink.subtype}: €{drink.price:.2f}")

    def _restock_all(self):
        for drink in self.inventory.drinks.values():
            drink.quantity = 10

    def maintenance_menu(self):
        """Displays the maintenance menu"""
        while True:
            print("Onderhoudsmenu:")
            print("1. Voeg product toe")
            print("2. Verwijder product")
            print("3. Verander hoeveelheid")
            print("4. Toon voorraad")
            print("5. Vul alles bij")
            print("6. Verander prijs")
            print("7. Sluit onderhoudsmenu")
            choice = input("\n> ")
            clear_screen()

            # Add drink
            if choice == "1":
                brand: str = input("Merk: ")
                subtype: str = input("Subtype (optioneel): ")
                try:
                    price: float = float(input("Prijs (veelvoud van 0.10): "))
                    if price * 100 % 10 != 0:
                        raise ValueError("Prijs moet een veelvoud van 0.10 zijn.")
                    quantity: int = int(input("Aantal: "))
                except ValueError:
                    print("Ongeldige invoer, terug naar menu.\n")
                    continue

                drink = Drink(brand, price, quantity, subtype)
                self._add_drink(drink)
                print(f"{drink.brand} {drink.subtype} is succesvol toegevoegd.\n")

            # Remove drink
            elif choice == "2":
                self._display_inventory()
                try:
                    index = int(input("\nWelk product wil je verwijderen? (nummer): ")) - 1
                    drinks = list(self.inventory.drinks.values())
                    if 0 <= index < len(drinks):
                        drink = drinks[index]
                        self._remove_drink(drink.brand, drink.subtype)
                        print(f"{drink.brand} {drink.subtype} is succesvol verwijderd.\n")
                    else:
                        print("Ongeldige keuze, terug naar menu.\n")
                except ValueError as e:
                    print(f"Ongeldige invoer, terug naar menu.\n{e}")

            # Change quantity
            elif choice == "3":
                self._display_inventory()
                try:
                    index = int(input("\nWelk product wil je de hoeveelheid van veranderen? (nummer): ")) - 1
                    drinks = list(self.inventory.drinks.values())
                    if 0 <= index < len(drinks):
                        drink = drinks[index]
                        try:
                            quantity = int(input("Nieuwe hoeveelheid: "))
                            if drink.change_stock(quantity):
                                print(f"{drink.brand} {drink.subtype} heeft nu {quantity} stuks.\n")
                        except ValueError:
                            print("Ongeldige invoer, terug naar menu.\n")
                except ValueError:
                    print("Ongeldige invoer, terug naar menu.\n")

            # Display inventory
            elif choice == "4":
                self._display_inventory()
                input("\nDruk op enter om terug te gaan naar het menu...")
                clear_screen()

            # Restock all drinks
            elif choice == "5":
                self._restock_all()
                print(f"Alle producten zijn bijgevuld tot {Drink.MAX_STOCK} stuks.\n")

            # Change price
            elif choice == "6":
                self._display_prices()
                try:
                    index = int(input("\nWelk product wil je de prijs van veranderen? (nummer): ")) - 1
                    drinks = list(self.inventory.drinks.values())
                    if 0 <= index < len(drinks):
                        drink = drinks[index]
                        try:
                            print(f"Huidige prijs: €{drink.price:.2f}")
                            price = float(input("Nieuwe prijs: (veelvoud van 0.10) \n> "))
                            if price * 100 % 10 == 0:
                                drink.price = price
                                print(f"{drink.brand} {drink.subtype} heeft nu een prijs van €{price:.2f}\n")
                            else:
                                print("Ongeldige prijs, terug naar menu.\n")
                        # Invalid price
                        except ValueError:
                            print("Ongeldige invoer, terug naar menu.\n")
                # Invalid choice
                except ValueError:
                    print("Ongeldige invoer, terug naar menu.\n")

            # Exit maintenance menu
            elif choice == "7":
                break

            # Invalid choice
            else:
                print("Ongeldige keuze, probeer opnieuw.\n")


def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')
