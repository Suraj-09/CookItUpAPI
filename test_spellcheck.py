from spellchecker import SpellChecker

spell = SpellChecker(distance=2)

# find those words that may be misspelled
misspelled = spell.unknown(['something', 'is', 'hapenning', 'here', 'macarooni'])

for word in misspelled:
    # Get the one `most likely` answer
    print(spell.correction(word))

    # Get a list of `likely` options
    print(spell.candidates(word))