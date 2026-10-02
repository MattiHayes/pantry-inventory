import sqlite3
from database.item import update_item_quantity, rename_item

class Item:

    @classmethod
    def from_db(cls, row: sqlite3.Row):
        return cls(
            row["id"],
            row["name"],
            row["quantity"],
            row["unit"]
        )

    def __init__(
            self,
            id: int,
            name: str, 
            quantity: float,
            unit: str = "",
        ) -> None:
        self._name = name.lower()
        self._quantity = quantity
        self._unit = unit
        self._id = id

    def __str__(self) -> str:
        return f"{self._name.capitalize()}: {self._quantity}{self._unit}"

    def update_db(self):
        update_item_quantity(self._id, self._quantity)

    def add_quantity(self, quantity: float) -> None:
        if quantity < 0:
            raise ValueError(f"Can not add a negative amount of {self._name}")

        self._quantity += quantity
        self.update_db()
        

    def used(self, quantity: float) -> None:
        if quantity < 0:
            raise ValueError(f"Can not use a negative amount of {self._name}")
        
        self._quantity = max(self._quantity - quantity, 0)
        self.update_db()

    def update(self, new_quantity, float) -> None:

        if new_quantity < 0:
            raise ValueError(f"Must have a positive quantity of {self._name}")

        self._quantity = new_quantity
        self.update_db()

    @property
    def name(self) -> str:
        return self._name

    @name.setter
    def name(self, name: str) -> None:
        self._name = name.lower()
        rename_item(self._id, self._name)

        