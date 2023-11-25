import pymongo
import os
from dotenv import load_dotenv
import time
import validation
import parse

# Load environment variables from .env file
load_dotenv()

def get_ingredient_nutrition(ingredient_list):
    start_time = time.time()  # Record the start time
    atlas_uri = os.getenv('ATLAS_URI')

    client = pymongo.MongoClient(atlas_uri)

    db = client["NutritionDatabase"]

    collection = db["nutritional-information"]

    end_time = time.time()  # Record the end time
    print(f"connection took {end_time - start_time} seconds")
    
    ingredients_to_search = []

    ingredients_with_nutrition = []
    for ing_obj in ingredient_list:

        if (not ing_obj.ignore):
            query = {"$and": [{"food_name": ing_obj.name}, {str(ing_obj.measure): {"$exists": True}}]}
            existing_document = collection.find_one(query)
            if existing_document is not None:
                ing_obj.nutrition = parse.parse_nutrition_doc(ing_obj.quantity, ing_obj.measure, existing_document)
                ingredients_with_nutrition.append(ing_obj)
            else:
                ing_obj.name = validation.spell_check_ingredient(ing_obj.name)
                query = {"$and": [{"food_name": ing_obj.name}, {str(ing_obj.measure): {"$exists": True}}]}
                existing_document = collection.find_one(query)
                if existing_document is not None:
                    ing_obj.nutrition = parse.parse_nutrition_doc(ing_obj.quantity, ing_obj.measure, existing_document)
                    ingredients_with_nutrition.append(ing_obj)
                else:
                    ingredients_to_search.append(ing_obj)

    return [ingredients_with_nutrition, ingredients_to_search]

def insert_many_ingredients(ingredient_nutrtion_list):

    atlas_uri = os.getenv('ATLAS_URI')

    client = pymongo.MongoClient(atlas_uri)

    db = client["NutritionDatabase"]

    collection = db["nutritional-information"]

    for ingredient in ingredient_nutrtion_list:
        print(ingredient)
        measure = ingredient['measures'][0]

        existing_document = collection.find_one({'food_name': ingredient['food_name']})
    
        if existing_document is None:
            collection.insert_one(ingredient)
            print(f"{ingredient['food_name']} was added to database")
        else:
            if measure not in existing_document['measures']:
                collection.update_one(
                    {'_id': existing_document['_id']},
                    {
                        '$push': {'measures': measure },
                        '$set': {measure: ingredient[measure]}
                    }
                )
            print(f"{ingredient['food_name']} was updated")
