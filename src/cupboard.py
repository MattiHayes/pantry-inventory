from database.cupboard import insert_cupboard, get_items_in_cupboard, get_cupboards
from database.item import get_item_with_name_in_cupboard, insert_item
from item import Item

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
            ) -> None:

        name = item_name.lower()

        if name not in self._items:
            raise ValueError(f"Item {name.capitalize} not in the {self._name.capitalize()}")

        self._items[name].add_quantity(item_quantity)

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

