from nicegui import app, ui
from data.database import Database
from pages.ricetta import ricetta_page, nuova_ricetta_page, modifica_ricetta_page
from pages.ricette import ricette_page
import sys

global db

@ui.page('/ricette')
def ricette():
    navigation_bar('Ricette')
    ricette_page(db)

@ui.page('/ricetta/{recipe_id}')
def ricetta(recipe_id):
    global db
    recipe = db.get_recipe(recipe_id)
    if recipe is None:
        ui.navigate.to("/ricette")
        ui.notify("Ricetta non trovata")
        return
    navigation_bar(recipe.name.title())
    ricetta_page(db, recipe)

@ui.page('/ricetta/{recipe_id}/modifica')
def modifica_ricetta(recipe_id):
    global db
    recipe = db.get_recipe(recipe_id)
    if recipe is None:
        ui.navigate.to("/ricette")
        ui.notify("Ricetta non trovata")
        return
    navigation_bar(recipe.name.title())
    modifica_ricetta_page(db, recipe)

@ui.page('/ricette/nuova')
def nuova_ricetta():
    global db
    navigation_bar('Nuova Ricetta')
    nuova_ricetta_page(db, db.get_new_id())



def navigation_bar(title: str = ''):
    ui.colors(primary='#FAB12F')
    ui.query('body').classes('bg-orange-50')
    links = 'align-middle w-full text-black text-lg p-2 m-0 hover:bg-orange-200 hover:cursor-pointer'
    icons = 'text-3xl p-1 w-[16dp] rounded hover:bg-orange-700 hover:cursor-pointer'
    with ui.header(elevated=True).classes('text-white bg-[#FA812F] items-center h-[60px] justify-between'):
        ui.label(title).classes('text-2xl truncate flex-[2] hover:cursor-default').tooltip(title)
        ui.icon('home').on('click', lambda: ui.navigate.to(f'/ricette')).classes(icons).tooltip('Home')

def main(path):
    global db
    db = Database(path)
    ui.navigate.to('/ricette')
    ui.run(title='Ricette', favicon='🍽️', port=8080)

if __name__ in {"__main__","__mp_main__"}:
    path = sys.argv[1] if len(sys.argv) > 1 else 'recipes.json'
    main(path)