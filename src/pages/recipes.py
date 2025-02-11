from nicegui import ui
from data.database import Database
from translations import translation

def recipes_page(lang, db):
    recipes = db.get_recipes_refs()
    for r in recipes:
        r["course"] = translation[lang][r["course"] if r["course"] else "entree"].title()
    with ui.row().classes('w-full'):
        ui.space()
        ui.button(icon='add', on_click= lambda: ui.navigate.to(f'/{lang}/recipes/new'))
    columns = [
        {'headerName': 'Nome', 'field': 'name', 'filter': 'agTextColumnFilter'},
        {'headerName': 'Portata', 'field': 'course', 'filter': "agSetColumnFilter"}
    ]
    table = ui.aggrid({'columnDefs': columns, 'rowData': recipes, 'rowSelection': 'single'}, theme='quartz') \
        .classes('w-full h-[80vh]') \
        .on('cellClicked', lambda event: ui.navigate.to(f'/{lang}/recipe/{event.args['data']['id']}'))