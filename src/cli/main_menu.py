from cupboard import Cupboard
from database.cupboard import get_cupboards, insert_cupboard

from .cupboard_menu import cupboard_menu


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


def main_menu() -> None:
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