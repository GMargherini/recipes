from data.ingredient import Ingredient
from typing import List, Dict, Any

class Recipe:

    courses = ['antipasto', 'primo', 'secondo', 'contorno', 'dolce', 'piatto unico']

    def __init__(self, id: int =0, name: str ='', ingredients: List[Ingredient] = [], serves: int =0, steps: List[str] = [], course: str =''):
        self.id = id
        self.name = name
        self.ingredients = [Ingredient.decode(i) for i in ingredients]
        self.serves = serves
        self.steps = steps
        self.course = course

    #TODO implement setters
    def set_name(self, name):
        self.name = name
    



    def decode(d):
        return Recipe(d['id'], d['name'], d['ingredients'], d['serves'], d['steps'], d['course'])

    def encode(r):
        ingredients = [Ingredient.encode(i) for i in r.ingredients]
        return {'id':r.id, 'name':r.name, 'ingredients':ingredients, 'serves':r.serves, 'steps':r.steps, 'course':r.course}

    