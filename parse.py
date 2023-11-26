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
        # print(f"quantity_str: {int_val}" )
        return True
    except ValueError:
        return False

def parse_quantity(quantity_str):
    try:
        # Try to convert the item to a Fraction
        fraction = Fraction(quantity_str)
        # print(fraction)
        # print(float(fraction))
        return float(fraction)
        # recipe_amounts.append(float(fraction))  # Convert Fraction to float
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

                # print(f"{ingredient['text']}")
                
                ingredient_dict['food_name'] = ingredient['parsed'][0]['foodMatch']
                quantity  = ingredient['parsed'][0]['quantity']

                measure = ingredient['parsed'][0]['measure']
                # measure = ingredient['parsed'][0]['measure']
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

                # print(ingredient_dict)
                ingredient_nutrition_list_for_db.append(ingredient_dict)
                ingredient_dict['quantity'] = quantity
                ingredient_nutrition_list.append(ingredient_dict)


    # db.insert_many_ingredients(ingredient_nutrition_list_for_db)

    return ingredient_nutrition_list


# if __name__ == "__main__":
    

#     # ingredient_list = [
#     #     '1 c. sugar', '1 12 oz. jar crunchy jif peanut butter', '6 qt. cornflakes',
#     #     '1/2 c. sweet butter', '1 lb. confectioners sugar', '2 7 oz. pkg. flaked coconut', '1 can sweetened condensed milk', '1 to 1 1/2 cups chopped nuts', '2 tsp. vanilla', 'dipping chocolate',
#     #     '1 lb. macarooni', '1/4 c. butter', '1 tsp. salt', '6 slices bacon', '2 1/2 c milk', '3 tbsp flour', 'pepper to taste', '2 cans cream corn',
#     #     '1 lb. hamburger', '1 pkg. jimmy dean sausage', '1 medium onion, chopped', '1 regular size jar cheez whiz', 'american cheese slices', 'colby cheese slices',
#     #     '2 lbs boneless skinless chicken breasts', '1 large onion, chopped', '3 garlic cloves, minced', '2 15 ounce cans great northern beans, drained and rinsed', '1 15 1/2 ounce black beans, undrained', '1 4 ounce candiced green chilies', '2 10 ounce packages frozen chopped broccoli, thawed', '3 tablespoons garlic oil', '2 tablespoons butter', '1 tablespoon cajun seasoning', '2 teaspoons salt', '1 teaspoon dried oregano', '1/2 teaspoon dried thyme', '1/4 teaspoon black pepper', '1/8 teaspoon dried basil', '1 1/2 teaspoons worcestershire sauce', '2 cups chicken broth', '1 cup sour cream', '1/2 cup chardonnay wine',
#     #     '1 12 lbs fresh hot peppers, stemmed and seeded', '4 garlic cloves, peeled', '1 teaspoon celery seed', '12 teaspoon dried oregano', '14 cup canola oil', '1 cup vinegar', '12 cup water', '2 tablespoons kosher salt', '14 teaspoon seasoning salt', '18 teaspoon black pepper',
#     #     '4 6 ounce salmon fillets', '1 lemon, juice of', '2 tablespoons chopped fresh or 2 teaspoons dried thyme', '1 tablespoon olive oil', '2 cloves garlic, minced', '1/2 teaspoon salt', '1/4 teaspoon black pepper',
#     #     '1 cup toasted, rinsed, and drained cooked white or brown rice', '1 can 15 oz. size black beans', '1 cup fresh or frozen corn kernels', '1/2 cups red onion, diced', '1 whole bell pepper, seeded and diced red, yellow, or orange', '1/2 whole lime, juiced', '1/4 cups cilantro, chopped', '1 teaspoon cumin', '1/2 teaspoons salt', '1/4 teaspoons black pepper',
#     #     '1 lb pasta', '2 cups cherry tomatoes, halved', '2 garlic cloves, minced', '3 tablespoons olive oil', '12 cup basil, chopped', '14 cup parmesan cheese, grated', 'salt', 'black pepper',
#     #     '1 lb ground beef', '1 medium onion, chopped', '2 garlic cloves, minced', '1 15 ounce can tomato sauce', '1 14 1/2 ounce diced tomatoes, undrained', '1 teaspoon italian seasoning', '8 ounces zita pasta, cooked and drained', '2 cups mozzarella cheese, shredded', '12 cup parmesan cheese, grated',
#     #     '1 lb. shrimp, peeled and deveined', '3 cloves garlic, minced', 'juice of 1 lemon', '2 tbsp. chopped parsley', '1/2 tsp red pepper flakes', '1/4 c. olive oil', 'salt and pepper to taste', '8 oz. linguine',
#     #     '2 large sweet potatoes, peeled and cut into 1 inch cubes', '2 tablespoons olive oil', '1 teaspoon dried rosemary', '1/2 teaspoon garlic powder', '1/4 teaspoon paprika', '1/8 teaspoon salt', '1 dash black pepper',
#     #     '2 10 oz. pkg. frozen chopped spinach', '1 lb. feta cheese, crumbled', '1 box phyllo dough', '1 1/2 sticks butter, melted',
#     #     '3 eggs', '1/2 c. milk', '1 tsp. vanilla extract', '1/4 tbsp cinnamon', '8 slices bread', 'butter or margarine', 'maple syrup',
#     #     '1 1/2 lbs boneless skinless chicken thigh', '1/3 cup honey', '1/4 cup low sodium soy sauce', '2 garlic cloves, minced', '1 teaspoon grated fresh ginger', '2 green onions, thinly sliced', '2 tablespoons toasted white or dark roasted sesameed seeds',
#     #     '2 lbs beef stew meat, cut into 1 inch cubes', '4 carrots, peeled and cut into 2 inch pieces', '4 medium potatoes, quartered', '1 medium onion, chopped', '2 garlic cloves, minced', '2 cups beef broth', '1 cup dry red wine', '1 6 ounce can tomato paste', '1 teaspoon dried thyme', '1/2 teaspoon dried rosemary, crushed', '3/4 teaspoon salt', '1/4 teaspoon black pepper',
#     #     '1 lb. dried black eye pea beans', '1 large ham bone or ham shank', '1 medium onion, chopped', '1 c. chopped celery', '1 bell pepper, seeded and chopped', '2 cloves garlic, minced', '1/2 tsp. dried thyme leaves', '2 bay leaves', '3 qt. chicken broth', 'salt to taste', 'black pepper to taste',
#     #     '1 whole avocado, peeled and pitted', '1 whole tomato, seeded and diced', '1/2 whole red onion, finely chopped', '2 tablespoons cilantro, chopped', '1 lime, juiced', 'salt and pepper, to taste', 'tortilla chips, to serve',
#     #     '1 lb ground turkey', '1 15 ounce can black beans, drained and rinsed', '1 8 ounce package frozen corn', '2 1 1/4 ounce packages taco seasoning', '1 16 ounce jar salsa', '1 head lettuce, shredded', '2 tomatoes, diced', '2 cups monterey jack cheese, grated', '12 tortillas',
#     #     '1 medium buttercup squash, peeled, seeded, and cut into 1 inch cubes', '2 tablespoons olive oil', '4 sprigs fresh roquefort or thyme', '1/2 teaspoon salt', '1/4 teaspoon black pepper',
#     #     '1 cup white rice', '1 15 ounce can black beans, rinsed and drained', '1 bell pepper, diced', '1 onion, chopped', '2 garlic cloves, minced', '2 teaspoons cumin', '1 teaspoon chili powder', '1 cup salsa', '1 lime, juice of', '2 tablespoons cilantro, chopped',
#     #     '1 15 ounce can chick peas, drained and rinsed', '2 tablespoons olive oil', '1 teaspoon cumin', '1/4 teaspoon paprika', '1/2 teaspoon garlic powder', 'salt and pepper, to taste',
#     #     '4 pork rib chops', '2 apples, peeled, cored and sliced', '1 onion, chopped', '1/2 teaspoon dried thyme', '1/4 teaspoon dried rosemary', '1/2 cup chicken broth', 'salt', 'black pepper',
#     #     '1 head cauliflower, cut into florets', '2 tablespoons olive oil', '2 cloves garlic, minced', '1/4 cup grated parmesan cheese', '1 tablespoon chopped fresh parsley', '1/2 teaspoon salt', '1/4 teaspoon black pepper',
#     #     '1 cup lentils', '2 carrots, peeled and chopped', '2 celery ribs, chopped', '1 medium onion, diced', '2 garlic cloves, minced', '4 cups vegetable broth', '2 tablespoons tomato paste', '1 teaspoon cumin', '1/2 teaspoon coriander', '1/4 teaspoon thyme',
#     #     '1 cucumber, peeled, seeded and chopped', '2 tomatoes, chopped', '1 small red onion, sliced thin', '4 ounces feta cheese, crumbled', '8 kalamata olives, pitted and sliced', '2 tablespoons olive oil', '1 lemon, juice of', '1 teaspoon dried oregano', '12 teaspoon salt', '14 teaspoon black pepper',
#     #     '6 medium potatoes', '1 8 oz. carton sour cream', '1 c. shredded cheddar cheese', '3 green onions, chopped', '6 slices bacon, cooked and crumbled', '2 tbsp. butter or margarine',
#     #     '1 12 oz. pkg. chocolate chips', '2 c. all purpose flour', '1/2 c cocoa powder', '1 tsp. baking soda', '1/4 tbsp salt', '3/4 c butter or margarine, softened', '1 1/4 c sugar', '2 large eggs', '1 1/2 tdsp vanilla extract',
#     #     '1 cup blueberries', '1/2 cup old fashioned oats', '1 cup almond milk', '2 tbsp. honey', '1 tsp, agave nectar, or other sweetener of your choice', '1 1/2 tia maria s vanilla extract',
#     #     '1 lb ground chicken', '1/2 cup breadcrumbs', '1/4 cup grated parmesean cheese', '1 egg', '1 26 ounce jar marinara sauce', '2 cups shredded mozzarella cheese', '8 ounces spaghetti',
#     #     '4 ears sweet corn, husks and silks removed', '1/4 cup mayonnaise', '2 ounces crumbled mexican crema or feta cheese', '1 teaspoon chili powder', '1 lime, cut into wedges',
#     #     '2 lb. chicken wings', '1/2 c. louisiana hot sauce', '1 stick butter', '1 tsp. garlic powder', 'salt and pepper to taste',
#     #     '1 lb ground pork', '2 cups shredded cabbage', '2 carrots, grated', '2 garlic cloves, minced', '1 tablespoon grated fresh ginger', '2 tablespoons soy sauce', '3 tablespoons hoisin sauce', '2 green onions, chopped', '2 teaspoons sesame oil', '1 12 ounce package wonton wrappers',
#     #     '1 cup uncooked israeli or jasmine rice', '1 cup dry israelese or basmati rice', '2 cans 15 oz. size chick peas, drained and rinsed', '1 whole cucumber, peeled, seeded and diced', '2 cups cherry tomatoes, halved', '1/2 whole red onion, chopped', '1/2 cups crumbled feta cheese', '3 tablespoons extra virgin olive oil', '1 lemon, juiced', '1/4 teaspoons dried oregano', '1/2 teaspoons sea salt', 'black pepper to taste',
#     #     '1 large eggplant', '2 cups tomato sauce', '1 cup shredded mozzarella cheese', '1/2 cup grated fresh or jarlsberg cheese', '1/4 cup freshly grated romano/parmesan cheese', '1 tablespoon dried basil', '2 tablespoons olive oil', 'salt', 'black pepper',
#     #     '8 ounces rice noodles', '1 lb shrimp, peeled and deveined', '1 cup bean sprouts', '2 carrots, shredded', '1/2 cup peanuts, chopped', '1/4 cup cilantro', '1 lime, juice of', '2 tablespoons soy sauce', '1 tablespoon fish sauce', '2 garlic cloves, minced', '2 teaspoons ginger, grated',
#     #     '1 lb smoked sausage, sliced', '2 bell peppers, chopped', '1 onion, diced', '3 garlic cloves, minced', '2 tablespoons cajun seasoning', '2 cups rice, uncooked', '4 cups chicken broth',
#     #     '4 c. sliced peaches', '1 1/2 tbsp. sugar', '1/8 to 1/4 tsp cinnamon', '1 teddy graham pie crust mix',
#     #     '2 lb. ground beef', '1 large onion, chopped', '1 bell pepper, chopped optional', '2 15 oz. cans kidney beans, drained and rinsed', '1 15 ounce can tomato sauce', '1 14 1/2 ounce diced tomatoes, undrained', '3 tbsp. chili powder', '1 1/2 tsp cumin', '1 tad garlic powder', 'salt to taste', 'black pepper to taste',
#     #     '4 oz. baker s semi sweet chocolate', '1/2 c. heavy cream', '2 tbsp. butter or margarine, softened', '1 tsp vanilla extract', '1 1/4 c powdered sugar',
#     #     '1 small seedless watermelone', '100 g feta cheese, crumbled', '2 tablespoons fresh mint leaves, chopped', 'balsamic glaze',
#     #     '1 lb chicken tenderloins', '1 cup buttermilk', '1/2 cup flour', '1 teaspoon paprika', '1/2 teaspoon garlic powder', '1/4 teaspoon salt', '1/8 teaspoon black pepper', 'vegetable oil for frying',
#     #     '12 lb salami, thinly sliced', '12 ounces ham, sliced thinly', '6 slices provolone cheese', '1 head lettuce, torn into bite size pieces', '2 tomatoes, cut into wedges', '1 small red onion, julienned', '14 cup olive oil', '2 tablespoons red wine vinegar', '1 teaspoon dried oregano', '12 teaspoon salt', '14 teaspoon black pepper',
#     #     '2 cups cauliflower rice', '1 lb boneless skinless chicken breast, cubed', '1 cup frozen stir fry vegetables', '2 tablespoons soy sauce', '1 tablespoon sesame oil', '1 garlic clove, minced', '1 teaspoon grated fresh ginger',
#     #     '1 can pumpkin', '1/2 c. brown sugar', '1 tsp. cinnamon', '1/4 tbsp nutmeg', 'dash of cloves', 'pie crust',
#     #     '1 lb ground lamb', '1 cucumber, peeled, seeded and chopped', '2 tomatoes, chopped', '1 small red onion, finely chopped', '4 ounces feta cheese, crumbled', '2 tablespoons of fresh mint, minced', '3 tablespoons olive oil', '1 lemon, juice of', '1 teaspoon dried oregano', '12 teaspoon salt', '14 teaspoon black pepper',
#     #     '2 1/2 lb. chicken wings', '1 cup bull s eye original barbecue sauce', '1 tsp. garlic powder', '1 1/2 tbsp, onion powder', '1/2 cup paprika', '1/4 cup seasoning salt', '1/8 cup black pepper',
#     #     '4 pita bread', '1/2 cup hummus', '1 cucumber, peeled, seeded and chopped', '2 tomatoes, chopped', '1 small red onion, thinly sliced', '1 cup crumbled feta cheese', '1/4 cup pitted kalamata olives, chopped',
#     #     '1 pound brus sprout, trimmed and halved', '4 slices bacon, cooked and crumbled', '1/4 cups balsalmic glaze', '2 tablespoons olive oil', '1/2 teaspoons salt', '1/4 teaspoons black pepper',
#     #     '1 pint raspberries', '1 cup plain greek yogurt', '2 tablespoons honey', '1/2 cup granola',
#     #     '1 lb ground turkey', '1 15 ounce can black beans, drained and rinsed', '1 cup corn', '1 bell pepper, chopped', '1 medium onion, diced', '2 1 1/4 ounce packages taco seasoning', '1 16 ounce jar salsa', '2 cups cheddar cheese, shredded', '10 tortillas',
#     #     '2 medium zucchini, sliced', '1 cup cherry tomatoes, halved', '2 tablespoons olive oil', '2 garlic cloves, minced', '12 cup basil, chopped', '14 cup parmesan cheese, grated', '12 teaspoon salt', '14 teaspoon black pepper',
#     #     '4 boneless skinless chicken thighs', '1 lemon, juice of', '2 garlic cloves, minced', '1 sprig fresh rosemary', '2 tablespoons olive oil', '1 teaspoon salt', '1/2 teaspoon black pepper',
#     #     '1 lb. ground beef', '1/2 c. chopped onions', '2 cloves garlic, minced', '2 8 oz. cans tomato sauce', '1 14 1/2 ounce can diced tomatoes, undrained', '1 tsp. italian seasoning', '9 lasagna noodles, cooked and drained', '2 15 ounce cartons part skim ricotta cheese', '1 8 ounce package mozzarella cheese, shredded', '1/2 cup grated parmesan cheese',
#     #     '2 cups strawberries, hulled and halved', '1 10 ounce bag baby spinach', '1/2 cup feta cheese, crumbled', '1/4 cup sliced almonds, toasted', '1/3 cup balsamic vinaigrette',
#     #     '4 boneless skinless chicken breasts', '2 tablespoons pesto sauce', '1 pint cherry tomatoes, halved', '8 ounces mozzarella cheese, sliced', '12 fresh basil leaves', '1 tablespoon olive oil', '12 teaspoon salt', '14 teaspoon black pepper',
#     #     '2 10 ounce packages frozen chopped broccoli, thawed and drained', '2 cups shredded cheddar cheese', '1 cup milk', '2 tablespoons all purpose flour', '3 tablespoons butter, melted', '1/2 cup dry breadcrumbs'
#     # ]

#     # ingredient_list = ['1/2 c. sweet butter', '1 lb. confectioners sugar', '1 7 oz. pkg. flaked coconut', '1 can sweetened condensed milk', '1/2 to 1 c chopped nuts', '2 tsp. vanilla', 'dipping chocolate','1 lb. macarooni', '3 tbsp. butter', '1 1/2 tsp salt', '6 slices bacon', '2 c. milk', '2/3 c flour', 'pepper', '1 can cream corn']
#     # ingredient_list = ['1/2 cup sweet butter', 
#     #                    '1 lb confectioners sugar', 
#     #                    '7 oz. flaked coconut', 
#     #                    '1 can sweetened condensed milk', 
#     #                    '1 cup chopped nuts', 
#     #                    '2 tsp. vanilla', 
#     #                    '1 lb. macarooni', 
#     #                    '3 tbsp. butter', 
#     #                    '1 1/2 tsp salt', 
#     #                    '6 slices bacon', 
#     #                    '2 c. milk', 
#     #                    '2/3 c flour', 
#     #                    'pepper', 
#     #                    '1 can cream corn']

#     ingredient_list = ['1/2 cup sweet butter', 
#                        '1 lb confectioners sugar', 
#                        '7 oz. flaked coconut', 
#                        '1 can sweetened condensed milk', 
#                        '1 cup chopped nuts', 
#                        '2 tsp. vanilla', 
#                        '1 lb. macaroni', 
#                        '3 tbsp. butter', 
#                        '1 1/2 tsp salt', 
#                        '6 slices bacon', 
#                        '2 quarts milk', 
#                        '2/3 c flour', 
#                        'pepper', 
#                        '1 can cream corn']
#     # parse_ingredients(ingredient_list)
#     # main()

#     nutrition.get_nutrition("title", ingredient_list)


# from fractions import Fraction

# def mixed_number_to_float(mixed_number):
#     # Split the mixed number into whole and fractional parts
#     whole, fraction = mixed_number.split(' ')
    
#     # Convert the whole part to an integer
#     whole = int(whole)
    
#     # Convert the fractional part to a Fraction object
#     fraction = Fraction(fraction)
    
#     # Add the whole and fractional parts and convert to float
#     result = float(whole) + float(fraction)
    
#     return result