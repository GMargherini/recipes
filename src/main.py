from nicegui import app, ui
from data.database import Database
from pages.ricetta import ricetta_page, nuova_ricetta_page, modifica_ricetta_page
from pages.ricette import ricette_page


@ui.page('/ricette')
def ricette():
    navigation_bar('Ricette')
    ricette_page()

@ui.page('/ricetta/{recipe_id}')
def ricetta(recipe_id):
    recipe = Database().get_recipe(recipe_id)
    navigation_bar(recipe.name.title())
    ricetta_page(recipe)

@ui.page('/ricetta/{recipe_id}/modifica')
def modifica_ricetta(recipe_id):
    recipe = Database().get_recipe(recipe_id)
    navigation_bar(recipe.name.title())
    modifica_ricetta_page(recipe)

@ui.page('/ricette/nuova')
def nuova_ricetta():
    navigation_bar('Nuova Ricetta')
    nuova_ricetta_page(Database().get_new_id())



def navigation_bar(title: str = ''):
    ui.colors(primary='#FAB12F')
    ui.query('body').classes('bg-orange-50')
    links = 'align-middle w-full text-black text-lg p-2 m-0 hover:bg-orange-200 hover:cursor-pointer'
    icons = 'text-3xl p-1 w-[16dp] rounded hover:bg-orange-700 hover:cursor-pointer'
    with ui.header(elevated=True).classes('text-white bg-[#FA812F] items-center h-[60px] justify-between'):
        ui.label(title).classes('text-2xl truncate flex-[2] hover:cursor-default').tooltip(title)
        ui.icon('home').on('click', lambda: ui.navigate.to(f'/ricette')).classes(icons).tooltip('Home')

def main():
    ui.navigate.to('/ricette')
    ui.run(title='Ricette', favicon='🍽️')

if __name__ in {"__main__","__mp_main__"}:
    main()