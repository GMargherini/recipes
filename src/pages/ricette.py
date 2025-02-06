from nicegui import ui
import json
from data.recipe import Recipe
from data.ingredient import Ingredient
from typing import List, Dict, Any


def get_recipe(recipe_id:int) -> Recipe:
    for r in recipes:
        if int(r['id']) == int(recipe_id):
            return Recipe.decode(r)

def get_new_id():
    return len(recipes)

def as_dict(obj) -> Dict[str, Any]:
    if 'ingredients' in obj:
        return {
            'id': obj['id'], 'name': obj['name'], 'ingredients': obj['ingredients'],
            'serves': obj['serves'], 'steps': obj['steps'], 
            'course': str(obj['course']).capitalize() if obj['course'] in Recipe.courses else None
        }
    else:
        return obj

def import_recipes(path='recipes.json') -> List[Recipe]:
    with open(path) as file:
        recipes = json.load(file, object_hook=as_dict)
        return recipes

recipes = import_recipes()

# TODO implement json encoder
def save_recipes(new_recipe, path='recipes.json'):
    recipes = list(import_recipes())
    print(recipes)
    recipes[new_recipe.id-1] = Recipe.encode(new_recipe)
    with open(path) as file:
        recipes = json.dump(new_recipe, file)




def ricette_page():
    with ui.row().classes('w-full'):
        ui.space()
        ui.button(icon='add', on_click= lambda: ui.navigate.to('/ricette/nuova'))
    columns = [
        {'HeaderName': 'Nome', 'field': 'name', 'filter': 'agTextColumnFilter'},
        {'HeaderName': 'Portata', 'field': 'course', 'filter': "agSetColumnFilter"}
    ]
    table = ui.aggrid({'columnDefs': columns, 'rowData': recipes, 'rowSelection': 'single'}, theme='quartz') \
        .on('cellClicked', lambda event: ui.navigate.to(f'/ricetta/{event.args['data']['id']}'))