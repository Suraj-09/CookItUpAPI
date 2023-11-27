import pymongo
import os
from dotenv import load_dotenv
import parse
import helper_functions
from bson import ObjectId

# Load environment variables from .env file
load_dotenv()

atlas_uri = os.getenv('ATLAS_URI')

client = pymongo.MongoClient(atlas_uri)

db = client["NutritionDatabase"]

collection_nutrition = db["nutritional-information"]
collection_recipe = db["recipe"]


def get_ingredient_nutrition(ingredient_list):
    ingredients_to_search = []

    ingredients_with_nutrition = []
    for ing_obj in ingredient_list:

        if (not ing_obj.ignore):
            query = {"$and": [{"food_name": ing_obj.name}, {str(ing_obj.measure): {"$exists": True}}]}
            existing_document = collection_nutrition.find_one(query)
            if existing_document is not None:
                ing_obj.nutrition = parse.parse_nutrition_doc(ing_obj.quantity, ing_obj.measure, existing_document)
                ingredients_with_nutrition.append(ing_obj)
            else:
                ing_obj.name = helper_functions.spell_check_ingredient(ing_obj.name)
                query = {"$and": [{"food_name": ing_obj.name}, {str(ing_obj.measure): {"$exists": True}}]}
                existing_document = collection_nutrition.find_one(query)
                if existing_document is not None:
                    ing_obj.nutrition = parse.parse_nutrition_doc(ing_obj.quantity, ing_obj.measure, existing_document)
                    ingredients_with_nutrition.append(ing_obj)
                else:
                    ingredients_to_search.append(ing_obj)

    return [ingredients_with_nutrition, ingredients_to_search]

def insert_many_ingredients(ingredient_nutrtion_list):

    for ingredient in ingredient_nutrtion_list:
        measure = ingredient['measures'][0]

        existing_document = collection_nutrition.find_one({'food_name': ingredient['food_name']})
    
        if existing_document is None:
            collection_nutrition.insert_one(ingredient)
            print(f"{ingredient['food_name']} was added to database")
        else:
            if measure not in existing_document['measures']:
                collection_nutrition.update_one(
                    {'_id': existing_document['_id']},
                    {
                        '$push': {'measures': measure },
                        '$set': {measure: ingredient[measure]}
                    }
                )
            print(f"{ingredient['food_name']} was updated")

def insert_recipe(input_string, recipe):
    recipe_id = None

    input_string = helper_functions.sort_ingredients(input_string)
    hashed_input_string = helper_functions.hash_string(input_string)
    hashed_recipe = helper_functions.hash_json(recipe)

    recipe_document = {
        "hashed_ingredients": hashed_input_string,
        "hashed_recipe": hashed_recipe,
        "recipe": recipe
    }

    existing_document = collection_recipe.find_one({'hashed_recipe': hashed_recipe})
    if existing_document is None:
        result = collection_recipe.insert_one(recipe_document)
        print(f"{recipe_document['recipe']['title']} was added to database")
        recipe_id = result.inserted_id
    else:
        recipe_id = existing_document['_id']

    return recipe_id

def get_recipe(recipe_id):
    # Convert recipe_id to ObjectId
    try:
        recipe_id = ObjectId(recipe_id)
    except Exception as e:
        # Handle the exception if recipe_id is not a valid ObjectId
        print(f"Invalid recipe_id: {e}")
        return None  # or raise an exception, depending on your needs

    existing_document = collection_recipe.find_one({'_id': recipe_id})

    return existing_document['recipe']
