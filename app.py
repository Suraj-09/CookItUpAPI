from flask import Flask, request, jsonify
from recipe_generator  import generation_function

app = Flask(__name__)

# ingredients = "macaroni, butter, salt, bacon, milk, flour, pepper, cream corn"
ingredients = "spaghetti, olive oil, garlic, tomatoes, basil, oregano, salt, black pepper, Parmesan cheese, chicken breast, soy sauce, ginger, bell pepper, broccoli, jasmine rice, black beans, ground beef, chili powder, cumin, paprika, salsa, tortillas, sour cream, cheddar cheese, mayonnaise, mustard, pickles, ground turkey, whole wheat bread, lettuce, tomato, cucumber, lemon, honey, Dijon mustard, quinoa, spinach, feta cheese, lemon juice, chickpeas, cayenne pepper, coriander, turmeric, cumin, coconut milk, red curry paste, lentils, vegetable broth, sweet potatoes, cinnamon, nutmeg, vanilla extract, baking soda, baking powder, all-purpose flour, sugar, chocolate chips, oats, peanut butter, bananas, vanilla extract, cinnamon, baking soda, walnuts, strawberries, yogurt, honey, blueberries, almond milk, chia seeds, pumpkin puree, pumpkin spice, maple syrup, pecans, cranberries, white beans, kale, balsamic vinegar, garlic, dijon mustard, red onion, cherry tomatoes, parsley"


response = generation_function(ingredients)
print("-----------------------------------")
print(response)
print("-----------------------------------")
print(response["ingredients"])
print("-----------------------------------")
# @app.route('/')
# def hello():
#     return 'Welcome to the Cook It Up API!'

# @app.route('/test', methods=["GET"])
# def test():
#     ingredients = request.json['ingredients']

#     if ingredients is None:
#         return (
#             jsonify({"error": "Missing 'ingredients' parameter in the GET request."}),
#             400,
#         )
    
#     response = generation_function(ingredients)

#     return jsonify({"recipe": response})