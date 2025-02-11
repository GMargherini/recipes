from nicegui import app, ui
from data.database import Database
from pages.recipe import recipe_page, new_recipe_page, edit_recipe_page
from pages.recipes import recipes_page
import sys

global db

@ui.page('/recipes')
def recipes():
    navigation_bar('Ricette')
    recipes_page(db)

@ui.page('/recipe/{recipe_id}')
def recipe(recipe_id):
    global db
    recipe = db.get_recipe(recipe_id)
    if recipe is None:
        ui.navigate.to("/recipes")
        ui.notify("Ricetta non trovata")
        return
    navigation_bar(recipe.name.title())
    recipe_page(db, recipe)

@ui.page('/recipe/{recipe_id}/edit')
def edit_recipe(recipe_id):
    global db
    recipe = db.get_recipe(recipe_id)
    if recipe is None:
        ui.navigate.to("/recipes")
        ui.notify("Ricetta non trovata")
        return
    navigation_bar(recipe.name.title())
    edit_recipe_page(db, recipe)

@ui.page('/recipes/new')
def new_recipe():
    global db
    navigation_bar('Nuova Ricetta')
    new_recipe_page(db, db.get_new_id())



def navigation_bar(title: str = ''):
    ui.colors(primary='#FAB12F')
    ui.query('body').classes('bg-orange-50')
    links = 'align-middle w-full text-black text-lg p-2 m-0 hover:bg-orange-200 hover:cursor-pointer'
    icons = 'text-3xl p-1 w-[16dp] rounded hover:bg-orange-700 hover:cursor-pointer'
    with ui.header(elevated=True).classes('text-white bg-[#FA812F] items-center h-[60px] justify-between'):
        ui.label(title).classes('text-2xl truncate flex-[2] hover:cursor-default').tooltip(title)
        ui.icon('home').on('click', lambda: ui.navigate.to(f'/recipes')).classes(icons).tooltip('Home')

def main(path):
    global db
    db = Database(path)
    ui.navigate.to('/recipes')
    ui.run(title='Ricette', favicon='🍽️', port=8080)

if __name__ in {"__main__","__mp_main__"}:
    path = sys.argv[1] if len(sys.argv) > 1 else 'recipes.json'
    main(path)