
from cupboard import Cupboard, UnitMismatchError
from database.cupboard import (
    get_cupboards,
    insert_cupboard,
    remove_cupboard,
    rename_cupboard,
)


def list_cupboards() -> list[Cupboard]:
    rows = get_cupboards()
    return [Cupboard.from_db(row) for row in rows]


def show_cupboards() -> None:
    cupboards = list_cupboards()

    if not cupboards:
        print("No cupboards found.")
        return

    for cupboard in cupboards:
        print(cupboard)


def add_cupboard() -> None:
    name = input("Cupboard name: ").strip()

    if not name:
        print("Cupboard name cannot be empty.")
        return

    insert_cupboard(name)
    print(f"Added cupboard: {name}")

def list_items(cupboard) -> None:
    print(cupboard)

def add_item(cupboard) -> None:
    item_name = input("Input Item name: > ").lower()
    quantity = input(f"Input the quantity of the {item_name}: > ")
    unit = input(f"Input the unit for {item_name}: > ")

    try:
        cupboard.add_item(item_name, quantity, unit)
    except UnitMismatchError as e:
        print(e)
        print("Please try again")

def change_item_quantity(cupboard) -> None:
    item_name = input("Input Item name: > ").lower()
    new_quantity = input(f"Input new quantity of {item_name}: > ")
    cupboard[item_name].quantity = new_quantity

def change_item_unit(cupboard) -> None:
    item_name = input("Input Item name: > ").lower()
    new_unit = input(f"Input new unit for {item_name}: > ")
    cupboard[item_name].quantity = new_unit

def remove_item(cupboard) -> None:
    item_name = input("Input Item name: > ").lower()
    del cupboard[item_name]

def rename_item(cupboard) -> None:
    item_name = input("Input Item name: > ").lower()
    new_name = input(f"Input the new name for {item_name}: > ")
    cupboard.rename_item(item_name,  new_name)

def change_cupboard_name(cupboard):
    new_name = input(f"Input the new name for {cupboard.name}: > ").lower()
    cupboard.name = new_name
    rename_cupboard(cupboard.id, new_name)

def delete_cupboard(cupboard) -> bool:
    remove_cupboard(cupboard.id)
    return True

def cupboard_menu(cupboard: Cupboard) -> None:
    while True:
        print(cupboard)
        print()
        print("1. List items")
        print("2. Add item")
        print("3. Change item quantity")
        print("4. Change item unit")
        print("5. Remove item")
        print("6. Rename item")
        print("7. Rename cupboard")
        print("8. Delete cupboard")
        print("9. Back")

        choice = input("\n> ").strip()

        if choice == "1":
            list_items(cupboard)

        elif choice == "2":
            add_item(cupboard)

        elif choice == "3":
            change_item_quantity(cupboard)

        elif choice == "4":
            change_item_unit(cupboard)

        elif choice == "5":
            remove_item(cupboard)

        elif choice == "6":
            rename_item(cupboard)

        elif choice == "7":
            change_cupboard_name(cupboard)

        elif choice == "8":
            if delete_cupboard(cupboard):
                break

        elif choice == "9":
            break

        else:
            print("Invalid choice.")


def select_cupboard() -> None:
    rows = get_cupboards()

    if not rows:
        print("No cupboards found.")
        return

    print("\nSelect a cupboard:")

    for number, row in enumerate(rows, start=1):
        print(f"{number}. {row['name']}")

    choice = input("\n> ").strip()

    if not choice.isdigit():
        print("Invalid choice.")
        return

    index = int(choice) - 1

    if index < 0 or index >= len(rows):
        print("Invalid choice.")
        return

    cupboard = Cupboard.from_db(rows[index])

    cupboard_menu(cupboard)


def main() -> None:
    while True:
        print()
        print("Pantry Inventory")
        print("----------------")
        print("1. List cupboards")
        print("2. Add cupboard")
        print("3. Select cupboard")
        print("4. Exit")

        choice = input("\n> ").strip()

        if choice == "1":
            show_cupboards()

        elif choice == "2":
            add_cupboard()

        elif choice == "3":
            select_cupboard()

        elif choice == "4":
            print("Goodbye!")
            break

        else:
            print("Invalid choice.")


if __name__ == "__main__":
    main()
