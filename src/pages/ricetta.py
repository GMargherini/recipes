from nicegui import ui
from data.recipe import Recipe
from pages.ricette import recipes, save_recipes


def save_recipe(recipe):
    save_recipes(recipe)
    ui.notify('Ricetta Salvata')
    ui.navigate.to('/ricette')

def add_step():
    pass

def delete_step():
    pass

def add_ingredient():
    pass

def delete_ingredient():
    pass


def ricetta_page(recipe):
    with ui.row().classes('w-full'):
        ui.space()
        ui.button(icon='edit', on_click= lambda: ui.navigate.to(f'/ricetta/{recipe.id}/modifica'))
    with ui.card().classes('w-full'):
        with ui.column():
            ui.label(recipe.name.title())
            with ui.row():
                ui.label(f'Porzioni: {recipe.serves} persone')
            ui.separator()

            ui.label('Ingredienti')
            with ui.list().props('dense separator'):
                for ingredient in recipe.ingredients:
                    ui.item(f'{ingredient.quantity} {ingredient.unit}\t{ingredient.name}')
            ui.separator()

            ui.label('Preparazione')
            for s in recipe.steps:
                ui.label(s)

def modifica_ricetta_page(recipe):
    nuova_ricetta_page(recipe.id, recipe)

def nuova_ricetta_page(new_id, recipe=None):
    r = Recipe(new_id)
    with ui.card().classes('w-full'):
        with ui.tabs() as tabs:
            info = ui.tab("Informazioni")
            ingrs = ui.tab("Ingredienti")
            steps = ui.tab("Preparazione")
        with ui.tab_panels(tabs, value=info).classes('w-full'):
            with ui.tab_panel(info):
                with ui.row():
                    ui.label('Nome')
                    ui.input(value=recipe.name if recipe is not None else '').on("update:model-value", lambda e: r.set_name(e.args))
                with ui.row():
                    ui.label('Porzione')
                    ui.input(value=recipe.serves if recipe is not None else '').on("update:model-value", lambda e: ui.notify(e.args))
                with ui.row():
                    ui.label('Portata')
                    ui.select(Recipe.courses, value=recipe.course.lower() if recipe is not None else 'antipasto').on("update:model-value", lambda e: ui.notify(e.args['label']))
            with ui.tab_panel(ingrs):
                with ui.row():
                    with ui.column().classes('w-full'):
                        if recipe is not None:
                            for i in range(len(recipe.ingredients)):
                                ui.label(f'Ingrediente {i+1}')
                                with ui.row():
                                    ui.input(value=recipe.ingredients[i].name, placeholder='Ingrediente').on("update:model-value", lambda e: ui.notify(e.args))
                                    ui.input(value=recipe.ingredients[i].quantity, placeholder='Quantità').on("update:model-value", lambda e: ui.notify(e.args))
                                    ui.input(value=recipe.ingredients[i].unit, placeholder='Unità di misura').on("update:model-value", lambda e: ui.notify(e.args))
                                    ui.space()
                                    ui.button(icon='delete', on_click= lambda: delete_ingredient())
                        else:
                            ui.label(f'Ingrediente 1')
                            ui.input(placeholder='Ingrediente').on("update:model-value", lambda e: ui.notify(e.args))
                            ui.input(placeholder='Quantità').on("update:model-value", lambda e: ui.notify(e.args))
                            ui.input(placeholder='Unità di misura').on("update:model-value", lambda e: ui.notify(e.args))
                        with ui.row().classes('w-full'):
                            ui.space()
                            ui.button(icon='add', on_click= lambda: add_ingredient())
            with ui.tab_panel(steps):
                with ui.column().classes('w-full'):
                    if recipe is not None:
                        for i in range(len(recipe.steps)):
                            ui.label(f'Passo {i+1}')
                            ui.textarea(value=recipe.steps[i]).classes('w-full').on("update:model-value", lambda e: ui.notify(e.args))
                            with ui.row().classes('w-full'):
                                ui.space
                                ui.button(icon='delete', on_click= lambda: delete_step())
                    else:
                        ui.label(f'Passo 1')
                        ui.textarea().classes('w-full').on("update:model-value", lambda e: ui.notify(e.args))
                    with ui.row().classes('w-full'):
                        ui.space()
                        ui.button(icon='add', on_click= lambda: add_step())
    with ui.row().classes('w-full'):
        ui.space()
        ui.button(icon='save', on_click= lambda: save_recipe(r))
