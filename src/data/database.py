import json
from data.recipe import Recipe
from data.ingredient import Ingredient
from typing import List, Dict, Any

class Database():
    def __init__(self, path):
        self.path = path
        self._recipes = Database.import_recipes(path)

    def as_dict(obj) -> Dict[str, Any]:
        if 'ingredients' in obj:
            return {
                'id': obj['id'], 'name': obj['name'], 'ingredients': obj['ingredients'],
                'serves': obj['serves'], 'steps': obj['steps'], 
                'course': str(obj['course']) if obj['course'] in Recipe.courses else None
            }
        else:
            return obj

    def import_recipes(path) -> List[Recipe]:
        with open(path) as file:
            recipes = json.load(file, object_hook=Database.as_dict)
            return recipes
    
    def get_recipe(self, recipe_id:int) -> Recipe:
        for r in self._recipes:
            if int(r['id']) == int(recipe_id):
                return Recipe.decode(r)

    def set_recipe(self, recipe):
        exists = False
        for i in range(len(self._recipes)):
            if self._recipes[i]['id'] == recipe.id:
                self._recipes[i] = Recipe.encode(recipe)
                exists = True
        if not exists:
            self._recipes.append(Recipe.encode(recipe))

    def delete_recipe(self, recipe_id):
        for r in self._recipes:
            if r['id'] == recipe_id:
                self._recipes.remove(r)
            self.save_recipes()

    def get_recipes_refs(self):
        self._recipes = Database.import_recipes(self.path)
        return [{'id':r['id'], 'name':r['name'], 'course':r['course']} for r in self._recipes]

    def get_new_id(self):
        return len(self._recipes)+1

    def save_recipes(self):
        with open(self.path, mode='w') as file:
            json.dump(self._recipes, file)