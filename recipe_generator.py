from transformers import AutoTokenizer, AutoModelForSeq2SeqLM, pipeline
import re
from nutrition import get_nutrition
import mongo_helper

tokenizer = AutoTokenizer.from_pretrained("flax-community/t5-recipe-generation")
model = AutoModelForSeq2SeqLM.from_pretrained("flax-community/t5-recipe-generation")
generator = pipeline("text2text-generation", model=model, tokenizer=tokenizer)

generate_kwargs = {
    "max_length": 512,
    "min_length": 64,
    "no_repeat_ngram_size": 3,
    "do_sample": True,
    "top_k": 60,
    "top_p": 0.95,
    "num_return_sequences": 3
}

def skip_special_tokens_and_prettify(text, tokenizer, use_db):
    recipe_maps = {"<sep>": "--", "<section>": "\n"}
    recipe_map_pattern = "|".join(map(re.escape, recipe_maps.keys()))

    text = re.sub(
        recipe_map_pattern, 
        lambda m: recipe_maps[m.group()], 
        re.sub("|".join(tokenizer.all_special_tokens), "", text)
    )

    data = {"title": "", "ingredients": [], "directions": [], "nutrition": []}
    for section in text.split("\n"):
        section = section.strip()
        section = section.strip()
        if section.startswith("title:"):
            data["title"] = section.replace("title:", "").strip()
        elif section.startswith("ingredients:"):
            data["ingredients"] = [s.strip() for s in section.replace("ingredients:", "").split('--')]
            data["nutrition"] = get_nutrition(data["ingredients"], use_db)
        elif section.startswith("directions:"):
            data["directions"] = [s.strip() for s in section.replace("directions:", "").split('--')]
        else:
            pass

    return data

def post_generator(output_tensors, tokenizer, use_db):
    output_tensors = [output_tensors[i]["generated_token_ids"] for i in range(len(output_tensors))]
    texts = tokenizer.batch_decode(output_tensors, skip_special_tokens=False)
    texts = [skip_special_tokens_and_prettify(texts[0], tokenizer, use_db)]
    return texts


def recipe_generation_function(input_ingredients, use_db = True):
    generated = generator(input_ingredients, return_tensors=True, return_text=False, **generate_kwargs)
    outputs = post_generator(generated, tokenizer, use_db)

    output = outputs[0]

    recipe_id = mongo_helper.insert_recipe(input_ingredients, output)
    output['recipe_id'] = str(recipe_id)

    return output