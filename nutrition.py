import requests
from dotenv import load_dotenv
import os
import mongo_helper
import parse
import config

# get nutritional information based on a list of ingredients requested by the user (can decode to use database or not)
def get_nutrition(ingredient_list, use_db):

    # Parse ingredients to a list 
    ing_obj_list = parse.parse_ingredients(ingredient_list)
    
    # check if the ingredients are within the database, if so retrieve the ingredients nutritional information
    if use_db:
        result = mongo_helper.get_ingredient_nutrition(ing_obj_list)
        ingredients_with_nutrition = result[0]
        ingredients_to_search = result[1]
    
    # otherwise, API call with Edamam to retrive the nutritional information for all ingredients
    else:
        ingredients_with_nutrition = []
        ingredients_to_search = ing_obj_list

    # adds ingredients to the database if not present and request nutritional information from Edaman API for all ingredients 
    ingredients_for_db = []
    for ing_obj in ingredients_to_search:
        ing_nutrition = request_nutrition_from_api(ing_obj.full)

        # check if nutritional information is valid and under correct format (without absence of value or empty list)
        if ing_nutrition is not None and ing_nutrition != []:
            ing_nutrition = ing_nutrition[0]

            # retrieve nutrition information based on the measurement and quantity proportions 
            measure = ing_nutrition['measures'][0]
            ing_obj.quantity = ing_nutrition['quantity']
            ing_obj.measure = measure

            # parse the nutrional information 
            ing_obj.nutrition = parse.parse_nutrition_doc(ing_nutrition['quantity'], measure, ing_nutrition)    
            
            # append the ingredients with nutritional information
            ingredients_with_nutrition.append(ing_obj)                                                          

            # retrieve quantity information and check if it is valid (not 0 and not empty) 
            ing_nutrition.pop("quantity")
            if (ing_obj.quantity != 0 and ing_obj.measure != ""):

                # checks if the name of the ingredients differs from the food name of the nutritional information
                if (ing_obj.name != ing_nutrition['food_name']):
                  
                    # if so, updates the nutrional information food name with the name from ingredients list
                    ing_nutrition_other_name = dict(ing_nutrition)
                    ing_nutrition_other_name['food_name'] = ing_obj.name
                    
                    # append new nutritional information name for the datase
                    ingredients_for_db.append(ing_nutrition_other_name)

            # append the nutrional information to the database
            ingredients_for_db.append(ing_nutrition)

    # inserts all the missing ingredients from the database
    mongo_helper.insert_many_ingredients(ingredients_for_db)

    # format the nutrition information and sets them to default value
    nutrition = {
        'Calories': 0,
        'Fat': 0,
        'Carbohydrate': 0,
        'Protein': 0
    }

    # for all ingredients containing nutrional information, show their values for different parameters and return those values 
    for ing_obj in ingredients_with_nutrition:
        nutrition['Calories'] += ing_obj.nutrition['Calories']
        nutrition['Fat'] += ing_obj.nutrition['Fat']
        nutrition['Carbohydrate'] += ing_obj.nutrition['Carbohydrate']
        nutrition['Protein'] += ing_obj.nutrition['Protein']
    
    return nutrition


def request_nutrition_from_api(ingredient):
    # Load environment variables from .env file
    load_dotenv()

    # Your dotenv file should have these entries: APP_ID=your_app_id_here, APP_KEY=your_app_key_here
    # app_id = os.getenv('EDAMAM_APP_ID')
    # app_key = os.getenv('EDAMAM_APP_KEY')
    app_id = config.EDAMAM_APP_ID
    app_key = config.EDAMAM_APP_KEY

    # API endpoint
    # api_url = 'https://api.edamam.com/api/nutrition-details'
    api_url = 'https://api.edamam.com/api/nutrition-data'

    # Set up headers with your app_id and app_key
    headers = {
        'Content-Type': 'application/json',
    }

    # Include app_id and app_key as query parameters
    params = {
        'app_id': app_id,
        'app_key': app_key,
        'ingr':ingredient
    }

  
    # Send POST request
    response = requests.get(api_url, params=params, headers=headers)
    
    
    # Check the response
    if response.status_code == 200:
        print("Request successful")
        ingredient_nutrition = parse.parse_recipe_data(response.json())

        return ingredient_nutrition
    else:
        print(f"Request failed with status code {response.status_code}. Response:")
        print(response.text)
        return None

    return response.json()
