from cupboard import Cupboard, UnitMismatchError
from database.cupboard import (
    remove_cupboard,
    rename_cupboard,
)


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
    cupboard[item_name].unit = new_unit

def remove_item(cupboard) -> None:
    item_name = input("Input Item name: > ").lower()
    del cupboard[item_name]

def rename_item(cupboard) -> None:
    item_name = input("Input Item name: > ").lower()
    new_name = input(f"Input the new name for {item_name}: > ").lower()
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