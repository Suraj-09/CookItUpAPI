from flask import Flask, request, jsonify
from recipe_generator  import generation_function

application = Flask(__name__)

@application.route('/')
def hello():
    return 'Welcome to the Cook It Up API!'

@application.route('/test', methods=["GET"])
def test():
    ingredients = request.json['ingredients']

    if ingredients is None:
        return (
            jsonify({"error": "Missing 'ingredients' parameter in the GET request."}),
            400,
        )
    
    response = generation_function(ingredients)

    return jsonify({"recipe": response})