from nicegui import ui
from data.recipe import Recipe
from data.ingredient import Ingredient
from data.database import save_recipes, set_recipe, delete_recipe

def remove_recipe(recipe_id):
    delete_recipe(recipe_id)
    ui.navigate.to(f'/ricette/')

def ricetta_page(recipe):
    with ui.row().classes('w-full'):
        ui.space()
        ui.button(icon='edit', on_click= lambda: ui.navigate.to(f'/ricetta/{recipe.id}/modifica'))
        ui.button(icon='delete', on_click= lambda: remove_recipe(recipe.id))
    with ui.card().classes('w-full'):
        with ui.column():
            ui.label(recipe.name.title())
            with ui.row():
                ui.label(f'Porzioni: {recipe.serves}')
            ui.separator()

            ui.label('Ingredienti')
            with ui.list().props('bordered separator'):
                for ingredient in recipe.ingredients:
                    ui.item(f'{ingredient.name}: {ingredient.quantity} {ingredient.unit}')
            ui.separator()

            ui.label('Preparazione')
            for s in recipe.steps:
                ui.label(s)

def save_recipe(recipe):
    set_recipe(recipe)
    save_recipes()
    ui.notify('Ricetta Salvata')
    ui.navigate.to(f'/ricetta/{recipe.id}')

def add_step(steps, container):
    steps.append(step_item(steps, len(steps) if steps else 0, container))

def delete_step(steps, container, num):
    if list(container) and steps:
        steps.pop(num)
        container.remove(num)
    return steps

def add_ingredient(ingrs, container):
    ingrs.append(ingredient_item(ingrs, len(ingrs) if ingrs else 0, container))

def delete_ingredient(ingrs, container, num):
    if list(container) and ingrs:
        ingrs.pop(num)
        container.remove(num)
    return ingrs

def remove_add_button(container):
    if list(container):
        i = len(list(container)) - 1
        container.remove(i)

def add_button(function, data, container):
        with ui.row().classes('w-full'):
            ui.space()
            ui.button(icon='add', on_click= lambda: function(data, container))

def set_step(steps, num, string):
    if num < len(steps):
        steps[num] = string
    else:
        steps.append(string)

def update_steps(steps, new_steps):
    steps = new_steps

def step_item(steps, num, container):
    with container:
        step = steps[num] if num < len(steps) else ''
        with ui.card().classes('w-full'):
            ui.label(f'Passo {num+1}')
            ui.textarea(value=step).classes('w-full').on("update:model-value", lambda e: set_step(steps, num, e.args))
            if num > 0:
                with ui.row().classes('w-full'):
                    ui.space()
                    ui.button(icon='delete', on_click= lambda: delete_step(steps, container, num))
    return steps

def ingredient_item(ingrs, num, container):
    with container:
        ingr = ingrs[num] if num < len(ingrs) else Ingredient()
        with ui.card().classes('w-full'):
            ui.label(f'Ingrediente {num+1}')
            with ui.row().classes('w-full'):
                ui.input(value=ingr.name, placeholder='Ingrediente').on("update:model-value", lambda e: ingr.set_name(e.args))
                ui.input(value=ingr.quantity, placeholder='Quantità').on("update:model-value", lambda e: ingr.set_quantity(e.args))
                ui.input(value=ingr.unit, placeholder='Unità di misura').on("update:model-value", lambda e: ingr.set_unit(e.args))
                if num > 0:
                    ui.space()
                    ui.button(icon='delete', on_click= lambda: delete_ingredient(ingrs, container, num))
    return ingrs

def ingredients_form(recipe):
    ingredients = []
    with ui.card().classes('w-full'):
        with ui.column().classes('w-full') as container:
            if recipe is not None and recipe.ingredients != []:
                for i in range(len(recipe.ingredients)):
                    ingredients = ingredient_item(recipe.ingredients, i, container)        
            else:
                ingredients = ingredient_item(ingredients, 0, container)
        add_button(add_ingredient, ingredients, container)
    return ingredients


def steps_form(recipe):
    steps = []
    with ui.card().classes('w-full'):
        with ui.column().classes('w-full') as container:
            if recipe is not None and recipe.steps != []:
                for i in range(len(recipe.steps)):
                    steps = step_item(recipe.steps, i, container)
            else:
                steps = step_item(steps, 0, container)
        add_button(add_step, steps, container)
    return steps

def modifica_ricetta_page(recipe):
    nuova_ricetta_page(recipe.id, recipe)

def nuova_ricetta_page(new_id, recipe=None):
    r = Recipe(new_id)
    if recipe is not None:
        r.name = recipe.name
        r.serves = recipe.serves
        r.course = recipe.course
        r.ingredients = recipe.ingredients
        r.steps = recipe.steps
    
    with ui.card().classes('w-full'):
        with ui.row():
            ui.label('Nome')
            ui.input(value=r.name).on("update:model-value", lambda e: r.set_name(e.args))
        with ui.row():
            ui.label('Porzione')
            ui.input(value=r.serves).on("update:model-value", lambda e: r.set_serves(e.args))
        with ui.row():
            ui.label('Portata')
            ui.select(Recipe.courses, value=(r.course.lower() if r.course != '' else 'antipasto')).on("update:model-value", lambda e: r.set_course(e.args['label']))

    r.ingredients = ingredients_form(r)

    r.steps = steps_form(r)

    with ui.row().classes('w-full'):
        ui.space()
        ui.button(icon='save', on_click= lambda: save_recipe(r))
