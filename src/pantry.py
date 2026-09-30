from cupboard import Cupboard

class Pantry:

    def __init__(self) -> None:
        self._cupboards : dict[str, Cupboard] = {}

    def new_cupboard(self, cupboard_name: str) -> None:
        name = cupboard_name.lower()
        
        
        self._cupboards[name] 