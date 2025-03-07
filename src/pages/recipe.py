from nicegui import ui
from data.recipe import Recipe
from data.ingredient import Ingredient
from data.database import Database
from translations import translation

def remove_recipe(lang, db, recipe_id):
    db.delete_recipe(recipe_id)
    ui.navigate.to(f'/{lang}/recipes/')

def recipe_page(lang, db, recipe):
    with ui.row().classes('w-full'):
        ui.space()
        ui.button(icon='edit', on_click= lambda: ui.navigate.to(f'/{lang}/recipes/{recipe.id}/edit'))
        ui.button(icon='delete', on_click= lambda: remove_recipe(lang, db, recipe.id))
    with ui.card().classes('w-full'):
        with ui.column():
            ui.label(recipe.name.title()).classes('text-2xl')
            with ui.row():
                ui.label(f'{translation[lang]["serves"]}: {recipe.serves}')
            ui.separator()

            ui.label(translation[lang]["ingredients"]).classes('text-2xl')
            with ui.list().props('bordered separator'):
                for ingredient in recipe.ingredients:
                    ui.item(f'{ingredient.name}: {ingredient.quantity} {ingredient.unit}')
            ui.separator()

            ui.label(translation[lang]["steps"]).classes('text-2xl')
            for s in recipe.steps:
                ui.label(s)

def save_recipe(lang, db, recipe):
    db.set_recipe(recipe)
    ui.notify(translation[lang]["saved"])
    ui.navigate.to(f'/{lang}/recipes/{recipe.id}')


def add_item(lang, item, data, container):
    item(lang, data, len(data) if data else 0, container)
    

def delete_item(data, container, num):
    if list(container) and data:
        if num < len(data):
            data.pop(num)
        container.remove(num)
    return data

def remove_add_button(container):
    if list(container):
        i = len(list(container)) - 1
        container.remove(i)

def add_button(lang, function, data, container):
    with ui.row().classes('w-full'):
        ui.space()
        ui.button(icon='add', on_click= lambda: add_item(lang, function, data, container))

def set_item(data, num, item):
    if num < len(data):
        data[num] = item
    else:
        data.append(item)


def update(data, new_data):
    data = new_data

def step_item(lang, steps, num, container):
    with container:
        step = steps[num] if num < len(steps) else ''
        with ui.card().classes('w-full'):
            ui.label(f'{translation[lang]["step"]} {num+1}')
            ui.textarea(value=step).classes('w-full').on("update:model-value", lambda e: set_item(steps, num, e.args))
            if num > 0:
                with ui.row().classes('w-full'):
                    ui.space()
                    ui.button(icon='delete', on_click= lambda: update(steps, delete_item(steps, container, num)))
        set_item(steps, num, step)
    return steps

def ingredient_item(lang, ingrs, num, container):
    with container:
        ingr = ingrs[num] if num < len(ingrs) else Ingredient()
        with ui.card().classes('w-full'):
            ui.label(f'{translation[lang]["ingredient"]} {num+1}')
            with ui.row().classes('w-full'):
                ui.input(value=ingr.name, placeholder=translation[lang]["ingredient"]).on("update:model-value", lambda e: ingr.set_name(e.args))
                ui.input(value=ingr.quantity, placeholder=translation[lang]["quantity"]).on("update:model-value", lambda e: ingr.set_quantity(e.args))
                ui.input(value=ingr.unit, placeholder=translation[lang]["unit"]).on("update:model-value", lambda e: ingr.set_unit(e.args))
                if num > 0:
                    ui.space()
                    ui.button(icon='delete', on_click= lambda: update(ingrs, delete_item(ingrs, container, num)))
        set_item(ingrs, num, ingr)
    return ingrs

def ingredients_form(lang, recipe):
    ingredients = []
    with ui.card().classes('w-full'):
        with ui.column().classes('w-full') as container:
            if recipe.ingredients == []:
                recipe.ingredients.append(Ingredient())
            for i in range(len(recipe.ingredients)):
                ingredients = ingredient_item(lang, recipe.ingredients, i, container)
        add_button(lang, ingredient_item, ingredients, container)
    recipe.set_ingredients(ingredients)


def steps_form(lang, recipe):
    steps = []
    with ui.card().classes('w-full'):
        with ui.column().classes('w-full') as container:
            if recipe.steps == []:
                recipe.steps.append('')
            for i in range(len(recipe.steps)):
                steps = step_item(lang, recipe.steps, i, container)
        add_button(lang, step_item, steps, container)
    recipe.set_steps(steps)

def edit_recipe_page(lang, db, recipe):
    new_recipe_page(lang, db, recipe.id, recipe)

def new_recipe_page(lang, db, new_id, recipe=None):
    r = Recipe(new_id)
    if recipe is not None:
        r.name = recipe.name
        r.serves = recipe.serves
        r.course = recipe.course
        r.ingredients = recipe.ingredients
        r.steps = recipe.steps
    
    with ui.card().classes('w-full'):
        with ui.row():
            ui.label(translation[lang]["name"])
            ui.input(value=r.name).on("update:model-value", lambda e: r.set_name(e.args))
        with ui.row():
            ui.label(translation[lang]["serves"])
            ui.input(value=r.serves).on("update:model-value", lambda e: r.set_serves(e.args))
        with ui.row():
            trasnlated_courses = [translation[lang][c] for c in Recipe.courses]
            ui.label(translation[lang]["course"])
            ui.select(trasnlated_courses, value=(translation[lang][r.course.lower()] if r.course != '' else translation[lang]['entree'])).on("update:model-value", lambda e: r.set_course(list(translation[lang].keys())[list(translation[lang].values()).index(e.args['label'])]))

    ingredients_form(lang, r)

    steps_form(lang, r)

    with ui.row().classes('w-full'):
        ui.space()
        ui.button(icon='save', on_click= lambda: save_recipe(lang, db, r))
