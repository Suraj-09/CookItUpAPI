from spellchecker import SpellChecker
from fractions import Fraction

measurements_set = {
    "tsp", "tsp.", "tbsp", "tbsp.", "c", "c.", "lb", "lb.",
    "oz", "oz.", "g", "g.", "kg", "kg.", "ml", "ml.", "l", "l.",
    "pt", "pt.", "qt", "qt.", "gal", "gal.", "pinch", "pinches",
    "dash", "dashes", "smidgen", "smidgens", "drop", "drops",
    "piece", "pieces", "slice", "slices", "strip", "strips",
    "can", "cans", "bunch", "bunches", "sprig", "sprigs",
    "clove", "cloves"
}

def validate(ingredient_list):
    spell = SpellChecker()
    print(ingredient_list)

    for i in range(len(ingredient_list)):
        # print(f"check: {ingredient_list[i]}")
        # Check if the word is misspelled

        ingredient_split = ingredient_list[i].split()

        # print(ingredient_split)

        for j in range(len(ingredient_split)):
            ing = ingredient_split[j]
            if not is_numeric(ing) and ing not in measurements_set:
                if spell.known([ing]):
                    # print(f"{ing} is known")
                    continue
                else:
                    # print(f"{ing} is NOT known")
                    # misspelled = spell.unknown([ing])
                    # print(len(misspelled))
                    

                    correct_spelling = spell.correction(ing)

                    print(f"{ing} was corrected to {correct_spelling}")

                    ingredient_split[j] = correct_spelling
                    ingredient_list[i] = " ".join(ingredient_split)

                    # ingredient_list[i] = correct_spelling

    print(ingredient_list)
    return ingredient_list

def is_numeric(str):
    return is_float(str) or is_fraction(str) or str.isdigit()

def is_float(str):
    try:
        float(str)
        return True
    except ValueError:
        return False
    
def is_fraction(str):
    try:
        Fraction(str)
        return True
    except ValueError:
        return False
    