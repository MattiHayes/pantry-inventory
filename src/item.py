import sqlite3
from database.item import update_item_quantity, rename_item, change_item_unit

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

    @property
    def name(self) -> str:
        return self._name

    @name.setter
    def name(self, name: str) -> None:
        self._name = name.lower()
        rename_item(self._id, self._name)

    @property
    def unit(self) -> str:
        return self._unit

    @unit.setter
    def unit(self, new_unit: str):
        self._unit = new_unit
        change_item_unit(self._id, self._unit)

    @property
    def quantity(self) -> float:
        return self._quantity

    @quantity.setter
    def quantity(self, new_value: float) -> None:
        self._quantity = new_value
        update_item_quantity(self._id, self._quantity)

    @property
    def id(self) -> int:
        return self._id

    @id.setter
    def id(self, new_id) -> None:
        print ("Can not change item id")
        return

    def add_quantity(self, quantity: float) -> None:
        if quantity < 0:
            raise ValueError(f"Can not add a negative amount of {self._name}")

        self.quantity += quantity
        
    def used(self, quantity: float) -> None:
        if quantity < 0:
            raise ValueError(f"Can not use a negative amount of {self._name}")
        
        self.quantity = max(self._quantity - quantity, 0)

    def update(self, new_quantity, float) -> None:

        if new_quantity < 0:
            raise ValueError(f"Must have a positive quantity of {self._name}")

        self.quantity = new_quantity

