from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from recipe_generator import recipe_generation_function, recipe_generation_function_with_time
import mongo_helper

# FastAPI Instance Creation
app = FastAPI()

class Ingredients(BaseModel):
    ingredients: str

# Route for root endpoint
@app.get('/')
def welcome():
    return 'Welcome to the Cook It Up API!'

# Route for recipe retrieval from the NoSQL database
@app.get('/get_recipe')
def get_recipe(recipe_id: str):
    recipe = mongo_helper.get_recipe(recipe_id)

    # check if recipe is within the database, otherwise return a status code
    if not recipe:
        raise HTTPException(status_code=400, detail="Recipe not found")

    return {"recipe": recipe}

# Route for recipe generation based on an input of ingredients
@app.post('/generate_recipe')
def generate_recipe(ingredients: Ingredients):
    
    # Check if the request body for ingredients is present
    if not ingredients.ingredients:
        raise HTTPException(status_code=400, detail="Missing 'ingredients' parameter in the POST request.")

    # generate the recipe
    recipe = recipe_generation_function(ingredients.ingredients)

    # check if recipe is generated, otherwise return a status code
    if not recipe:
        raise HTTPException(status_code=422, detail="Failed to generate recipe")

    return {"recipe": recipe}

# route for performance analysis for a recipe stored within the database
@app.get('/performance/get_recipe')
def get_recipe(recipe_id: str):
    recipe = mongo_helper.get_recipe(recipe_id)

    # check if recipe is generated within the database, otherwise return a status code
    if not recipe:
        raise HTTPException(status_code=400, detail="Recipe not found")

    return {"recipe": recipe}

# route for performance analysis for a recipe generation
@app.post('/performance/generate_recipe')
def generate_recipe(payload: dict):

    ingredients_str = payload.get("ingredients", "")
    use_db = payload.get("use_db", True)

    ingredients = Ingredients(ingredients=ingredients_str)
    
    # check if ingredients is within the POST request
    if not ingredients.ingredients:
        raise HTTPException(status_code=400, detail="Missing 'ingredients' parameter in the POST request.")
    
    # check if use_db is within the POST request
    if use_db is None:
        raise HTTPException(status_code=400, detail="Missing 'use_db' parameter in the POST request.")

    # generate the recipe
    response = recipe_generation_function_with_time(ingredients.ingredients, use_db)

    # exception handling for failed recipe generation
    if not response["recipe"]:
        raise HTTPException(status_code=422, detail="Failed to generate recipe")

    return response