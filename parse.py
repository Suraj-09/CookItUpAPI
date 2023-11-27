from fractions import Fraction
from ingredient import Ingredient
import mongo_helper as db
import nutrition

ingredients_to_ignore = {
    "pepper to taste",
    "dash of pepper",
    "salt and pepper, to taste"
    "salt to taste",
    "black pepper to taste",
    "pepper",
    "salt"
    }

measurements_set = {
    "tsp", "tsp.", "teaspoon", "teaspoons",
    "tbsp", "tbsp.", "tablespoon", "tablespoons",
    "c", "c.", "cup", "cups",
    "lb", "lb.", "lbs", "pound", "pounds",
    "oz", "oz.", "ounce", "ounces",
    "g", "g.", "grams", "gram",
    "kg", "kg.", "kilogram", "kilograms",
    "ml", "ml.", "milliliter", "milliliters",
    "l", "l.", "liter", "liters",
    "pt", "pt.", "pint", "pints",
    "qt", "qt.", "quart", "quarts",
    "gal", "gal.", "gallon", "gallons",
    "pinch", "pinches",
    "dash", "dashes",
    "smidgen", "smidgens",
    "drop", "drops",
    "piece", "pieces",
    "slice", "slices",
    "strip", "strips",
    "can", "cans",
    "bunch", "bunches",
    "sprig", "sprigs",
    "clove", "cloves",
    "clove,", "cloves,",
    "pkg.", "pkg",
    "whole", "small", "medium", "large",
    "tdsp"
}

measurements_dict = {
    "tsp": "teaspoon", "tsp.": "teaspoon",
    "teaspoons": "teaspoon", "teaspoon": "teaspoon",
    "tbsp": "tablespoon", "tbsp.": "tablespoon",
    "tdsp":"tablespoon",
    "tablespoon": "tablespoon", "tablespoons": "tablespoon",
    "c": "cup", "c.": "cup", "cups": "cup", "cup": "cup",
    "lb": "pound", "lb.": "pound", "lbs": "pound",
    "pound": "pound", "pounds": "pound",
    "oz": "ounce", "oz.": "ounce",
    "ounce": "ounce", "ounces": "ounce",
    "g": "gram", "g.": "gram",
    "gram": "gram", "grams": "gram",
    "kg": "kilogram", "kg.": "kilogram",
    "kilogram": "kilogram", "kilograms": "kilogram",
    "ml": "milliliter", "ml.": "milliliter",
    "milliliter": "milliliter", "milliliters": "milliliter",
    "l": "liter", "l.": "liter", "liters": "liter",
    "pt": "pint", "pt.": "pint", "pints": "pint", "pint": "pint",
    "qt": "quart", "qt.": "quart", "quarts": "quart","quart": "quart",
    "gal": "gallon", "gal.": "gallon", "gallons": "gallon",
    "pinch": "pinch", "pinches": "pinch",
    "dash": "dash", "dashes": "dash",
    "smidgen": "smidgen", "smidgens": "smidgen",
    "drop": "drop", "drops": "drop",
    "piece": "piece", "pieces": "piece",
    "slice": "slice", "slices": "slice",
    "strip": "strip", "strips": "strip",
    "can": "can", "cans": "can",
    "bunch": "bunch", "bunches": "bunch",
    "sprig": "sprig", "sprigs": "sprig",
    "clove": "clove", "cloves": "clove",
    "clove,": "clove", "cloves,": "clove",
    "pkg.": "package", "pkg": "package",
    "whole":"whole","small":"whole", "medium":"whole", "large":"whole"
}

descriptor_set = {
    "frozen", "chopped", "thawed", "and", "drained", "shredded", "dry", "melted",
    "all", "purpose", "fresh", "halved", 'baby','hulled','grated','part','skim', 'cooked',
    'undrained', "diced", "minced", 'rinsed','trimmed', 'toasted','sliced','crumbled', 'of','pitted','dried',
    'cubed', 'julienned', 'cut', 'into', 'wedges', 'torn', 'into', 'bite', 'size', 'thinly', 'for', 'frying','or', 'softened',
    'peeled', 'seeded','finely', 'deveined', 'candiced', 'cored','sweet','sweetened', 'condensed'

}


def parse_ingredients(ingredient_list):
    num_parsed = 0
    num_total = len(ingredient_list)
    num_one_name = 0

    ingredient_object_list = []
    for ingredient in ingredient_list:
        ingredient_object = Ingredient()
        ingredient_object.full = ingredient
        ingredient = ingredient.replace(",", "")
        if (ingredient not in ingredients_to_ignore):
            ing_str = ingredient
            ingredient_split = ingredient.split()
            current_split = ingredient_split
            # print(ingredient_split)

            for i, section in enumerate(ingredient_split):
                
                quantity = parse_quantity(section)
                if quantity is not None:

                    # handle quantities like: 1 to 2 cups
                    if (i > 0 and ingredient_split[i-1] == "to"):
                        ingredient_object.quantity = (ingredient_object.quantity + quantity) / 2
                        current_split = [s for s in current_split if s != section]
                        current_split = [s for s in current_split if s != "to"]
                    # handle ex: 2 10 ounce package of food    
                    elif (i > 0 and (is_whole_num(ingredient_split[i-1])) and (is_whole_num(ingredient_split[i]))):
                        ingredient_object.quantity = (ingredient_object.quantity * quantity)
                        current_split = [s for s in current_split if s != section]
                    else:
                        ingredient_object.quantity = ingredient_object.quantity + quantity
                        current_split = [s for s in current_split if s != section]
                    
                if section in measurements_set:
                    if ingredient_object.measure == "":
                        ingredient_object.measure = measurements_dict[section]
                    current_split = [s for s in current_split if s != section]

                
                if section in descriptor_set:
                    current_split = [s for s in current_split if s != section]


            ingredient_object.name = ' '.join(current_split)
            ingredient_object.split_name = current_split

            if (ingredient_object.quantity != 0 and ingredient_object.measure != ""):
                ingredient_object.parsed = True
                num_parsed = num_parsed + 1
        else:
            ingredient_object.quantity = 1
            ingredient_object.ignore = True

        if (len(ingredient_object.split_name) == 1):
            num_one_name = num_one_name + 1

        ingredient_object_list.append(ingredient_object)
        

    return ingredient_object_list

def parse_nutrition_doc(qty, measure, document):
    nutrition_data = document[measure]
    nutrition_data['Calories'] = nutrition_data['Calories'] * qty
    nutrition_data['Protein'] = nutrition_data['Protein'] * qty
    nutrition_data['Carbohydrate'] = nutrition_data['Carbohydrate'] * qty
    nutrition_data['Fat'] = nutrition_data['Fat'] * qty
    
    return nutrition_data

                    
def is_whole_num(quantity_str):
    # print(quantity_str)
    try:
        # Try to convert the item to a Fraction
        int_val = int(quantity_str)
        return True
    
    except ValueError:
        return False

def parse_quantity(quantity_str):
    try:
        # Try to convert the item to a Fraction
        fraction = Fraction(quantity_str)
        return float(fraction)

    except ValueError:
        return None


def parse_recipe_data(recipe_data):
    # Access specific information
    recipe_name = recipe_data.get('uri', '')
    recipe_yield = recipe_data.get('yield', 0)
    recipe_calories = recipe_data.get('calories', 0)
    ingredients = recipe_data.get('ingredients', [])
    total_nutrients = recipe_data.get('totalNutrients', {})

    ingredient_nutrition_list = []
    ingredient_nutrition_list_for_db = []
    for ingredient in ingredients:
        if 'parsed' in ingredient:
            if 'measure' in ingredient['parsed'][0]:
                ingredient_dict = dict()
                
                ingredient_dict['food_name'] = ingredient['parsed'][0]['foodMatch']
                quantity  = ingredient['parsed'][0]['quantity']

                measure = ingredient['parsed'][0]['measure']
               
                ingredient_dict['measures'] = [measure]
                ingredient_dict[measure] = {}

                for nutrient, details in ingredient['parsed'][0]['nutrients'].items():
                    nutrient_label = details.get('label', '')

                    if nutrient_label == "Energy":
                        nutrient_quantity = details.get('quantity', 0)
                        ingredient_dict[measure]['Calories'] = nutrient_quantity / quantity
                    if nutrient_label == "Total lipid (fat)":
                        nutrient_quantity = details.get('quantity', 0)
                        ingredient_dict[measure]['Fat'] = nutrient_quantity / quantity
                    if nutrient_label == "Carbohydrate, by difference":
                        nutrient_quantity = details.get('quantity', 0)
                        ingredient_dict[measure]['Carbohydrate'] = nutrient_quantity / quantity
                    if nutrient_label == "Protein":
                        nutrient_quantity = details.get('quantity', 0)
                        ingredient_dict[measure]['Protein'] = nutrient_quantity / quantity

                ingredient_nutrition_list_for_db.append(ingredient_dict)
                ingredient_dict['quantity'] = quantity
                ingredient_nutrition_list.append(ingredient_dict)

    return ingredient_nutrition_list