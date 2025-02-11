import json
from data.recipe import Recipe
from data.ingredient import Ingredient
from typing import List, Dict, Any
import pymongo

class Database():
    def __init__(self):
        myclient = pymongo.MongoClient("mongodb://mongodb:27017/")
        mydb = myclient["database"]
        self.recs = mydb["recipes"]
    
    def get_recipe(self, recipe_id:int) -> Recipe:
        res = self.recs.find_one({"id":int(recipe_id)})
        print(res)
        return Recipe.decode(res) if res is not None else None 

    def set_recipe(self, recipe):
        self.recs.insert_one(Recipe.encode(recipe))

    def delete_recipe(self, recipe_id):
        self.recs.delete_one({"id": recipe_id})

    def get_recipes_refs(self):
        return [x for x in self.recs.find({},{ "_id": 0,"id":1, "name": 1, "course": 1 })]

    def get_new_id(self):
        return self.recs.count_documents({})