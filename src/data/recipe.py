from data.ingredient import Ingredient
from typing import List, Dict, Any

class Recipe:

    courses = ['entree', 'first course', 'second course', 'side', 'dessert', 'main course']

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

    def set_ingredients(self, ingredients):
        self.ingredients = ingredients    
    
    def set_serves(self, serves):
        self.serves = serves   
    
    def set_steps(self, steps):
        self.steps = steps   
    
    def set_course(self, course):
        self.course = course   



    def decode(d):
        return Recipe(d['id'], d['name'], d['ingredients'], d['serves'], d['steps'], d['course'])

    def encode(r):
        ingredients = [Ingredient.encode(i) for i in r.ingredients]
        return {'id':r.id, 'name':r.name, 'ingredients':ingredients, 'serves':r.serves, 'steps':r.steps, 'course':r.course}

    def __repr__(self):
        return f'({self.id}, {self.name})'

    