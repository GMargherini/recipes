from nicegui import ui
from data.database import get_recipes_refs

def ricette_page():
    recipes = get_recipes_refs()
    with ui.row().classes('w-full'):
        ui.space()
        ui.button(icon='add', on_click= lambda: ui.navigate.to('/ricette/nuova'))
    columns = [
        {'HeaderName': 'Nome', 'field': 'name', 'filter': 'agTextColumnFilter'},
        {'HeaderName': 'Portata', 'field': 'course', 'filter': "agSetColumnFilter"}
    ]
    table = ui.aggrid({'columnDefs': columns, 'rowData': recipes, 'rowSelection': 'single'}, theme='quartz') \
        .on('cellClicked', lambda event: ui.navigate.to(f'/ricetta/{event.args['data']['id']}'))