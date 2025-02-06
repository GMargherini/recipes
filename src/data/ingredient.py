from typing import Optional

class Ingredient:
    def __init__(self, name:str, quantity:int, unit:str):
        self.name = name
        self.quantity = quantity
        self.unit = unit
    
    def decode(d):
        return Ingredient(d['name'], d['quantity'], d['unit'])
    
    def encode(i):
        return {'name':i.name, 'quantity':i.quantity, 'unit':i.unit}