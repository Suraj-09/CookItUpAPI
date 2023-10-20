from flask import Flask, request, jsonify
from recipe_generator  import generation_function

app = Flask(__name__)

@app.route('/')
def hello():
    return 'Welcome to the Cook It Up API!'

@app.route('/test', methods=["GET"])
def test():
    ingredients = request.json['ingredients']

    if ingredients is None:
        return (
            jsonify({"error": "Missing 'ingredients' parameter in the GET request."}),
            400,
        )
    
    response = generation_function(ingredients)

    return jsonify({"recipe": response})