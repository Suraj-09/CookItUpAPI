from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from recipe_generator import recipe_generation_function
import mongo_helper

app = FastAPI()

class Ingredients(BaseModel):
    ingredients: str

@app.get('/')
def welcome():
    return 'Welcome to the Cook It Up API!'

@app.get('/get_recipe')
def get_recipe(recipe_id: str):
    recipe = mongo_helper.get_recipe(recipe_id)

    if not recipe:
        raise HTTPException(status_code=400, detail="Recipe not found")

    return {"recipe": recipe}

@app.post('/generate_recipe')
def generate_recipe(ingredients: Ingredients):
    if not ingredients.ingredients:
        raise HTTPException(status_code=400, detail="Missing 'ingredients' parameter in the POST request.")

    recipe = recipe_generation_function(ingredients.ingredients)

    if not recipe:
        raise HTTPException(status_code=422, detail="Failed to generate recipe")

    return {"recipe": recipe}

@app.get('/performance/get_recipe')
def get_recipe(recipe_id: str):
    recipe = mongo_helper.get_recipe(recipe_id)

    if not recipe:
        raise HTTPException(status_code=400, detail="Recipe not found")

    return {"recipe": recipe}

@app.post('/performance/generate_recipe')
def generate_recipe(ingredients: Ingredients, use_db: bool):
    if not ingredients.ingredients:
        raise HTTPException(status_code=400, detail="Missing 'ingredients' parameter in the POST request.")
    
    if not use_db:
        raise HTTPException(status_code=400, detail="Missing 'use_db' parameter in the POST request.")

    recipe = recipe_generation_function(ingredients.ingredients, use_db)

    if not recipe:
        raise HTTPException(status_code=422, detail="Failed to generate recipe")

    return {"recipe": recipe}