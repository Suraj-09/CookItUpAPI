import requests
from dotenv import load_dotenv
import os
import json
import mongo_helper
import parse


def get_nutrition(ingredient_list):
    ing_obj_list = parse.parse_ingredients(ingredient_list)
    result = mongo_helper.get_ingredient_nutrition(ing_obj_list)
    ingredients_with_nutrition = result[0]


    ingredients_to_search = result[1]

    for ing_obj in ingredients_to_search:
        ing_nutrition = request_nutrition_from_api(ing_obj.full)
        if ing_nutrition is not None and ing_nutrition != []:
            print(ing_nutrition)
            ing_nutrition = ing_nutrition[0]
            measure = ing_nutrition['measures'][0]
            ing_obj.quantity = ing_nutrition['quantity']
            ing_obj.measure = measure
            ing_obj.nutrition = parse.parse_nutrition_doc(ing_nutrition['quantity'], measure, ing_nutrition)
            ingredients_with_nutrition.append(ing_obj)

    nutrition = {
        'Calories': 0,
        'Fat': 0,
        'Carbohydrate': 0,
        'Protein': 0
    }

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
    app_id = os.getenv('EDAMAM_APP_ID')
    app_key = os.getenv('EDAMAM_APP_KEY')

    # API endpoint
    # api_url = 'https://api.edamam.com/api/nutrition-details'
    api_url = 'https://api.edamam.com/api/nutrition-data'

    # Example body for the POST request


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
