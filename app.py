from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from recipe_generator import recipe_generation_function

app = FastAPI()

class Ingredients(BaseModel):
    ingredients: str

@app.get('/')
def root():
    return 'Welcome to the Cook It Up API!'

@app.post('/generate_recipe')
def generate_recipe(ingredients: Ingredients):
    if not ingredients.ingredients:
        raise HTTPException(status_code=400, detail="Missing 'ingredients' parameter in the POST request.")

    response = recipe_generation_function(ingredients.ingredients)
    
    return {"recipe":response}
