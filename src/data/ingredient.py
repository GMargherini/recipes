from typing import Optional

class Ingredient:
    def __init__(self, name:str='', quantity:int='', unit:str=''):
        self.name = name
        self.quantity = quantity
        self.unit = unit

    def set_name(self, name):
        self.name = name
    
    def set_quantity(self, quantity):
        self.quantity = quantity

    def set_unit(self, unit):
        self.unit = unit
    
    def decode(d):
        return Ingredient(d['name'], d['quantity'], d['unit'])
    
    def encode(i):
        return {'name':i.name, 'quantity':i.quantity, 'unit':i.unit}