from cli.main_menu import main_menu
from database.utils import initialise_database


def main():
    initialise_database()
    main_menu()

if __name__ == "__main__":
    main()