import json
from data.recipe import Recipe
from data.ingredient import Ingredient
from typing import List, Dict, Any

def as_dict(obj) -> Dict[str, Any]:
    if 'ingredients' in obj:
        return {
            'id': obj['id'], 'name': obj['name'], 'ingredients': obj['ingredients'],
            'serves': obj['serves'], 'steps': obj['steps'], 
            'course': str(obj['course']) if obj['course'] in Recipe.courses else None
        }
    else:
        return obj

def import_recipes(path='recipes.json') -> List[Recipe]:
    with open(path) as file:
        recipes = json.load(file, object_hook=as_dict)
        return recipes

_recipes = import_recipes()

def get_recipe(recipe_id:int) -> Recipe:
    for r in _recipes:
        if int(r['id']) == int(recipe_id):
            return Recipe.decode(r)

def set_recipe(recipe):
    exists = False
    for i in range(len(_recipes)):
        if _recipes[i]['id'] == recipe.id:
            _recipes[i] = Recipe.encode(recipe)
            exists = True
    if not exists:
        _recipes.append(Recipe.encode(recipe))
        
def delete_recipe(recipe_id):
    for i in range(len(_recipes)):
        if _recipes[i]['id'] == recipe_id:
            _recipes.pop(i)
        save_recipes()

def get_recipes_refs():
    _recipes = import_recipes()
    return [{'id':r['id'], 'name':r['name'], 'course':r['course']} for r in _recipes]

def get_new_id():
    return len(_recipes)+1

def save_recipes(path='recipes.json'):
    with open(path, mode='w') as file:
        json.dump(_recipes, file)