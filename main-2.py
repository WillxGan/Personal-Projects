import sys
from menu import Menu
from order import Order

def load_menu_from_tsv(file_path):
    Newmenu = Menu()
    try:
        with open(file_path, 'r') as file:

            next(file)
            for line in file:

                name, price = line.strip().split('\t')
                Newmenu.add(name, float(price))
    except FileNotFoundError:
        print(f"Error: File '{file_path}' not found.")
        sys.exit(1)
    return Newmenu

def main():

    if len(sys.argv) != 2:
        print("USAGE: main.py menu.tsv")
        sys.exit(1)


    menu_file = sys.argv[1]
    menu = load_menu_from_tsv(menu_file)


    menu.print()
    print()


    Neworder = Order()
    print("What would you like to order?")
    while True:
        try:
            user_input = input().strip()
            if not user_input:
                continue


            menu_item = menu.find(user_input)
            if menu_item:
                Neworder.add(menu_item)
            else:
                print(f'Sorry, "{user_input}" isn\'t on the menu.')
        except EOFError:
            break


    if Neworder.total_quantity() > 0:
        print()
        Neworder.print()

if __name__ == "__main__":
    main()
