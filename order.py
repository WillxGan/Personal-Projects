class OrderItem:
    def __init__(self, menuitem, quantity=1):
        self.menuitem = menuitem
        self.quantity = quantity


class Order:
    def __init__(self):
        self.items = []

    def add(self, menuitem, quantity=1):
        for order in self.items:
            if order.menuitem.name == menuitem.name:
                order.quantity += quantity
                return
        new_order = OrderItem(menuitem, quantity)
        self.items.append(new_order)

    def total_price(self):
        return sum(item.menuitem.price * item.quantity for item in self.items)

    def total_quantity(self):
        return sum(item.quantity for item in self.items)

    def print(self):
        print("YOUR ORDER:                 Qty     Price     Total")

        for item in self.items:
            name = item.menuitem.name[:24]  # Limit the name to 24 characters
            qty = item.quantity
            price = f"${item.menuitem.price:.2f}"
            total = f"${item.menuitem.price * item.quantity:.2f}"

            # Print each item with correct formatting
            print(f"  {name:<24}  {qty:>3} {price:>9}  {total:>8}")

        # Calculate total price string
        total_price_str = f"${self.total_price():.2f}"

        # Adjust alignment with extra space before the dollar sign
        if len(total_price_str) ==5:
            print(f"{'TOTAL':<43}   {total_price_str}")
        elif len(total_price_str) == 6:
            print(f"{'TOTAL':<43}  {total_price_str}")
        elif len(total_price_str) == 7:
            print(f"{'TOTAL':<42}  {total_price_str}")


class MenuItem:
    def __init__(self, name, price):
        self.name = name
        self.price = price


if __name__ == "__main__":
    cheeseburger = MenuItem("Cheeseburger", 8.00)
    fountain_drink = MenuItem("Fountain Drink", 3.10)

    order = Order()
    order.add(cheeseburger, 17)  # Add 17 cheeseburgers
    order.add(fountain_drink, 1)  # Add 1 fountain drink

    order.print()
