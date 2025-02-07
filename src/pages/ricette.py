from nicegui import ui
from data.database import Database

def ricette_page(db):
    recipes = db.get_recipes_refs()
    with ui.row().classes('w-full'):
        ui.space()
        ui.button(icon='add', on_click= lambda: ui.navigate.to('/ricette/nuova'))
    columns = [
        {'headerName': 'Nome', 'field': 'name', 'filter': 'agTextColumnFilter'},
        {'headerName': 'Portata', 'field': 'course', 'filter': "agSetColumnFilter"}
    ]
    table = ui.aggrid({'columnDefs': columns, 'rowData': recipes, 'rowSelection': 'single'}, theme='quartz') \
        .classes('w-full h-[80vh]') \
        .on('cellClicked', lambda event: ui.navigate.to(f'/ricetta/{event.args['data']['id']}'))