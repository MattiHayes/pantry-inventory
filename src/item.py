import sqlite3

from database.item import change_item_unit, rename_item, update_item_quantity


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
    def name(self, new_name: str) -> None:
        name = new_name.lower()
        rename_item(self._id, name)
        self._name = name
        

    @property
    def unit(self) -> str:
        return self._unit

    @unit.setter
    def unit(self, new_unit: str):
        change_item_unit(self._id, new_unit)
        self._unit = new_unit
        

    @property
    def quantity(self) -> float:
        return self._quantity

    @quantity.setter
    def quantity(self, new_value: float) -> None:
        if new_value < 0:
            raise ValueError(f"Can not have a negative quantity of {self._name}")
        update_item_quantity(self._id, new_value)
        self._quantity = new_value
        

    @property
    def id(self) -> int:
        return self._id

    @id.setter
    def id(self, new_id) -> None:
        print ("Can not change item id")

    def add_quantity(self, quantity: float) -> None:
        if quantity < 0:
            raise ValueError(f"Can not add a negative amount of {self._name}")

        self.quantity += quantity
        
    def used(self, quantity: float) -> None:
        if quantity < 0:
            raise ValueError(f"Can not use a negative amount of {self._name}")
        
        self.quantity = max(self._quantity - quantity, 0)
