import pymongo
import os
from dotenv import load_dotenv
import parse
import helper_functions
from bson import ObjectId
import config

# Load environment variables from .env file
load_dotenv()

# setup mongoDB connection 
# atlas_uri = os.getenv('ATLAS_URI')
atlas_uri = config.ATLAS_URI

client = pymongo.MongoClient(atlas_uri)

# assign the nutritional database as variable
db = client["NutritionDatabase"]

# seperate the database into categories depending on the information attributes
collection_nutrition = db["nutritional-information"]
collection_recipe = db["recipe"]

# fetch nutritional information from the ingredients list
def get_ingredient_nutrition(ingredient_list):
    
    #initialise empty list
    ingredients_to_search = []
    ingredients_with_nutrition = []
    
    # for all ingredients, search in the ingredients list 
    for ing_obj in ingredient_list:

        # checks for the flag if the object is ignored or not
        if (not ing_obj.ignore):

            # request for the data of the nutritional information for an ingredient
            query = {"$and": [{"food_name": ing_obj.name}, {str(ing_obj.measure): {"$exists": True}}]}
           
           # return flag if the entry is found within the collection nutritional information
            existing_document = collection_nutrition.find_one(query)

            # check if the entry is found (ingredient), if so parse the nutritional information parameters and append it to the list of ingredients with nutrition for fast retrieval next call
            if existing_document is not None:
                ing_obj.nutrition = parse.parse_nutrition_doc(ing_obj.quantity, ing_obj.measure, existing_document)
                ingredients_with_nutrition.append(ing_obj)
            
            # otherwise, initally calls helper functions to remove unwanted entry type
            else:
                # performs helper function spell check for the ingredients -> attemps to match to an existing word 
                ing_obj.name = helper_functions.spell_check_ingredient(ing_obj.name)
                
                # after spellcheck, restart the query and searching within the database collection
                query = {"$and": [{"food_name": ing_obj.name}, {str(ing_obj.measure): {"$exists": True}}]}
                existing_document = collection_nutrition.find_one(query)
                
                # check the entry as before and append depending if the ingredient is found and retrieve information
                if existing_document is not None:
                    ing_obj.nutrition = parse.parse_nutrition_doc(ing_obj.quantity, ing_obj.measure, existing_document)
                    ingredients_with_nutrition.append(ing_obj)
                else:
                    ingredients_to_search.append(ing_obj)

    return [ingredients_with_nutrition, ingredients_to_search]

# function to insert many ingredients to the ingredients nutrition database
def insert_many_ingredients(ingredient_nutrtion_list):

    # for all ingredients within the nutritional list
    for ingredient in ingredient_nutrtion_list:
        measure = ingredient['measures'][0]

        # find the ingredient name within the database collection of nutrition information
        existing_document = collection_nutrition.find_one({'food_name': ingredient['food_name']})

        # if not found within the database (empty)
        if existing_document is None:
            # insert the ingredient to the database 
            collection_nutrition.insert_one(ingredient)
            print(f"{ingredient['food_name']} was added to database")
        
        else:
        # check for the measurement of the ingredient and if not found:
            if measure not in existing_document['measures']:
                
                # update the collection nutrition with id (from hash), measure 
                collection_nutrition.update_one(
                    {'_id': existing_document['_id']},
                    {
                        '$push': {'measures': measure },
                        '$set': {measure: ingredient[measure]}
                    }
                )
            print(f"{ingredient['food_name']} was updated")

# insert a recipe or update one to the database
def insert_recipe(input_string, recipe):
    
    # initialise default
    recipe_id = None

    # call helper function for each parameter as a hash string
    input_string = helper_functions.sort_ingredients(input_string)
    hashed_input_string = helper_functions.hash_string(input_string)
    hashed_recipe = helper_functions.hash_json(recipe)

    # each recipe have its own hash string and is formatted to make sure it is unique within the collection
    recipe_document = {
        "hashed_ingredients": hashed_input_string,
        "hashed_recipe": hashed_recipe,
        "recipe": recipe
    }

    # flag to check if an existing hash string exist within the collection of recipe
    existing_document = collection_recipe.find_one({'hashed_recipe': hashed_recipe})
    
    # if a recipe does not exist, insert the recipe to the database
    if existing_document is None:
        result = collection_recipe.insert_one(recipe_document)
        print(f"{recipe_document['recipe']['title']} was added to database")
        recipe_id = result.inserted_id
    
    # otherwise, retrieve the id to return the recipe to the user and for subsequent manipulation
    else:
        recipe_id = existing_document['_id']

    return recipe_id

# retrieve a recipe
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
