COEN 424 - Project 
# CookItUpAPI 

This project generates recipes based on a list of ingredients. It also provides the macronutrient information of the generated recipes.

The recipes and nutritional information are stored in a NoSQL database. 

Recipes are generated using a Hugging Face model and the macronutrients are retrieved from Edamam Nutritional Analysis API.

The technologies used for this service are:
- Language: python
- API handling: FastAPI 
- NoSQL Database: MongoDB
- Hugging Face Model: t5-recipe-generation
- Cloud Service: Microsoft Azure
- External API: Edamam Nutritional Analysis API

Performance Analysis is also done as an extra feature. 
