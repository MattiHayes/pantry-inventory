from cupboard import Cupboard

fridge = Cupboard("Fridge")

fridge.new_item("butter", 250, "g")
fridge.add_item("Butter", 250)
fridge.new_item("Onions", 3, 'onions')

print(fridge)