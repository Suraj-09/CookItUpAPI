from spellchecker import SpellChecker
import json
import hashlib

def sort_ingredients(ingredients_string):

    ingredients_list = []
    split_ingredients = ingredients_string.split(',')

    for ingredient in split_ingredients:
        ingredients_list.append(ingredient.strip())

    # Sort the ingredients alphabetically
    ingredients_list.sort()
    
    # Join the sorted ingredients into a string
    sorted_ingredients_string = ', '.join(ingredients_list)
    
    return sorted_ingredients_string

def spell_check_ingredient(ingredient):
    spell = SpellChecker()
    correct_spelling = ingredient

    if not spell.known([ingredient]):
        correct_spelling = spell.correction(ingredient)
        if correct_spelling is None:
            correct_spelling = ingredient

        # print(f"{ingredient} was corrected to {correct_spelling}")
        return correct_spelling

    return correct_spelling

def hash_string(input_string):
    # Create a new SHA-256 hash object
    sha256_hash = hashlib.sha256()

    # Update the hash object with the bytes-like object (encoded string)
    sha256_hash.update(input_string.encode('utf-8'))

    # Get the hexadecimal representation of the hash
    hashed_string = sha256_hash.hexdigest()

    return hashed_string


def hash_json(json_object):
    # Convert the JSON object to a string
    json_string = json.dumps(json_object, sort_keys=True)

    # Create a new SHA-256 hash object
    sha256_hash = hashlib.sha256()

    # Update the hash object with the bytes-like object (encoded JSON string)
    sha256_hash.update(json_string.encode('utf-8'))

    # Get the hexadecimal representation of the hash
    hashed_json = sha256_hash.hexdigest()

    return hashed_json
