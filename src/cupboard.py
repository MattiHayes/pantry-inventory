from item import Item

class Cupboard:

    def __init__(self, name: str) -> None:
        self._name = name.lower()
        self._items: dict[str, Item] = {}


    def new_item(
            self, 
            item_name: str,
            item_quantity: float,
            item_unit : str  = ""
            ) -> None:

        name = item_name.lower()

        if name in self._items:
            raise ValueError(f"Item {item_name} already in the {self._name.capitalize()}")
        
        self._items[name] = Item(name, item_quantity, item_unit)


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
        items = []
        for item in self._items:
            items.append(f"   ├── {str(self._items[item])}")

        return self._name.capitalize() + ":\n" + "\n".join(items)



if __name__ == "__main__":
    fridge = Cupboard("Fridge")

    fridge.new_item("butter", 250, "g")
    fridge.add_item("Butter", 250)
    fridge.new_item("Onions", 3)
    print(fridge)