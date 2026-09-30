class Item:
    def __init__(self, name: str, quantity: float, unit: str = "") -> None:
        self._name = name.lower()
        self._quantity = quantity
        self._unit = unit

    def __str__(self) -> str:
        return f"{self._name.capitalize()}: {self._quantity}{self._unit}"

    def add_quantity(self, quantity: float) -> None:
        if quantity < 0:
            raise ValueError(f"Can not add a negative amount of {self._name}")

        self._quantity += quantity

    def used(self, quantity: float) -> None:
        if quantity < 0:
            raise ValueError(f"Can not use a negative amount of {self._name}")
        
        self._quantity = max(self._quantity - quantity, 0)

    def update(self, new_quantity, float) -> None:

        if new_quantity < 0:
            raise ValueError(f"Must have a positive quantity of {self._name}")

        self._quantity = new_quantity

    @property
    def name(self) -> str:
        return self._name

    @name.setter
    def name(self, name: str) -> None:
        self._name = name.lower()
        