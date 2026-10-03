from database.cupboard import get_cupboards, get_items_in_cupboard, rename_cupboard
from database.item import insert_item, remove_item
from item import Item


class UnitMismatchError(Exception):
    pass

class Cupboard:

    @classmethod
    def from_db(cls, row):
        return cls(
            row["id"],
            row["name"],
        ) 

    def __init__(self,id: int, name: str) -> None:
        self._id = id
        self._name = name.lower()
        self._items: dict[str, Item] = {}
        self.load_items()


    def __str__(self) -> str:
        items = list(self._items.values())

        if not items:
            return self._name.capitalize() + ":"

        item_lines = [
            f"   ├── {item}"
            for item in items[:-1]
        ]

        item_lines.append(f"   └── {items[-1]}")

        return self._name.capitalize() + ":\n" + "\n".join(item_lines)

    def __getitem__(self, name: str) -> Item:
        return self._items[name]

    def __delitem__(self, item_name: str) -> None:
        # remove from database and then from python memory
        remove_item(self._items[item_name].id)
        del self._items[item_name]

    @property
    def name(self) -> str:
        return self._name

    @name.setter
    def name(self, new_name: str) -> None:
        name = new_name.lower()
        rename_cupboard(self._id, name)
        self._name = name

    @property
    def id(self) -> int:
        return self._id

    @id.setter
    def id(self, new_val) -> None:
        print("Can not change cupboard id.")

    def load_items(self):
        rows = get_items_in_cupboard(self._id)
        for row in rows:
            item = Item.from_db(row)
            self._items[item.name] = item

    def new_item(
            self, 
            item_name: str,
            item_quantity: float,
            item_unit : str  = ""
            ) -> None:

        name = item_name.lower()

        if name in self._items:
            raise ValueError(f"Item {item_name} already in the {self._name.capitalize()}")
        
        item_id = insert_item(name, item_quantity, item_unit, self._id)
        self._items[name] = Item(item_id, name, item_quantity, item_unit)


    def add_item(
            self, 
            item_name: str,
            item_quantity: float,
            item_unit: str = ""
            ) -> None:

        name = item_name.lower()

        if name not in self._items:
            self.new_item(name, item_quantity, item_unit)
            return

        item = self._items[item_name]

        if item_unit != item.unit:
            raise UnitMismatchError(
                f"{name} is already stored in {item.unit}, not {item_unit}."
            )

        self._items[name].add_quantity(item_quantity)

    def rename_item(self, item_name: str, new_name: str) -> None:
        self._items[item_name].name = new_name
        self._items[new_name] = self._items.pop(item_name) 

    def pop(self, item_name: str) -> Item:
        return self._items.pop(item_name)


if __name__ == "__main__":
    # fridge = Cupboard("Fridge")

    # fridge.new_item("butter", 250, "g")
    # fridge.new_item("Onions", 3)
    # print(fridge)

    cupboard_rows = get_cupboards()
    print(cupboard_rows)
    cupboards = [Cupboard.from_db(row) for row in cupboard_rows]

    for cupboard in cupboards:
        print(cupboard)

