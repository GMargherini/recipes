from nicegui import app, ui
from data.database import Database
from pages.recipe import recipe_page, new_recipe_page, edit_recipe_page
from pages.recipes import recipes_page
from translations import translation
import sys
import os

global db

@ui.page('/{lang}/recipes')
def recipes(lang):
    navigation_bar(lang, translation[lang]["recipes"].title())
    recipes_page(lang, db)

@ui.page('/{lang}/recipes/{recipe_id}')
def recipe(lang, recipe_id):
    global db
    recipe = db.get_recipe(recipe_id)
    if recipe is None:
        ui.navigate.to(f"/{lang}/recipes")
        ui.notify(translation[lang]["not found"])
        return
    navigation_bar(lang, recipe.name.title())
    recipe_page(lang, db, recipe)

@ui.page('/{lang}/recipes/{recipe_id}/edit')
def edit_recipe(lang, recipe_id):
    global db
    recipe = db.get_recipe(recipe_id)
    if recipe is None:
        ui.navigate.to(f"/{lang}/recipes")
        ui.notify(translation[lang]["not found"])
        return
    navigation_bar(lang, recipe.name.title())
    edit_recipe_page(lang, db, recipe)

@ui.page('/{lang}/recipe/new')
def new_recipe(lang):
    global db
    navigation_bar(lang, translation[lang]["new"])
    new_recipe_page(lang, db, db.get_new_id())



def navigation_bar(lang, title: str = ''):
    ui.colors(primary='#FAB12F')
    ui.query('body').classes('bg-orange-50')
    links = 'align-middle w-full text-black text-lg p-2 m-0 hover:bg-orange-200 hover:cursor-pointer'
    icons = 'text-3xl p-1 w-[16dp] rounded hover:bg-orange-700 hover:cursor-pointer'
    with ui.header(elevated=True).classes('text-white bg-[#FA812F] items-center h-[60px] justify-between'):
        ui.label(title).classes('text-2xl truncate flex-[2] hover:cursor-default').tooltip(title)
        ui.icon('home').on('click', lambda: ui.navigate.to(f'/{lang}/recipes')).classes(icons).tooltip('Home')

def main(lang, base_url):
    global db
    db = Database()
    ui.navigate.to(f'/{lang}/recipes')
    if base_url is not '':
        ui.run(title=translation[lang]['recipes'].title(), favicon='🍽️', port=8080, root_path=base_url)
    else:
        ui.run(title=translation[lang]['recipes'].title(), favicon='🍽️', port=8080)

if __name__ in {"__main__","__mp_main__"}:
    base_url = os.environ['BASE_URL'] if os.environ['BASE_URL'] else ''
    if base_url and not base_url.startswith('/'):
        base_url = '/'+base_url
    lang = os.environ['LANGUAGE'] if os.environ['LANGUAGE'] and os.environ['LANGUAGE'] in translation.keys() else 'en'
    main(lang, base_url)