import json

# Specify the path to your JSON file
json_file_path = 'nutrition_test.json'

# Open the file and load the JSON data
with open(json_file_path, 'r') as file:
    recipe_data = json.load(file)


# Access specific information
recipe_name = recipe_data.get('uri', '')
recipe_yield = recipe_data.get('yield', 0)
recipe_calories = recipe_data.get('calories', 0)
ingredients = recipe_data.get('ingredients', [])
total_nutrients = recipe_data.get('totalNutrients', {})

# Print the parsed information
print(f"Recipe Name: {recipe_name}")
print(f"Yield: {recipe_yield}")
print(f"Calories: {recipe_calories}")
print("\nIngredients:")

for ingredient in ingredients:
    print(f"- {ingredient['text']}")

print("\nTotal Nutrients:")
for nutrient, details in total_nutrients.items():
    
    nutrient_label = details.get('label', '')
    if nutrient_label in ["Energy", "Total lipid (fat)", "Carbohydrate, by difference", "Protein"]:
        nutrient_quantity = details.get('quantity', 0)
        nutrient_unit = details.get('unit', '')
        print(f"- {nutrient_label}: {nutrient_quantity} {nutrient_unit}")