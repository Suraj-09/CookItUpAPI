import requests
from dotenv import load_dotenv
import os
import json

# Load environment variables from .env file
load_dotenv()

# Your dotenv file should have these entries: APP_ID=your_app_id_here, APP_KEY=your_app_key_here
app_id = os.getenv('EDAMAM_APP_ID')
app_key = os.getenv('EDAMAM_APP_KEY')

# API endpoint
api_url = 'https://api.edamam.com/api/nutrition-details'

# Example body for the POST request


# Set up headers with your app_id and app_key
headers = {
    'Content-Type': 'application/json',
}

# Include app_id and app_key as query parameters
params = {
    'app_id': app_id,
    'app_key': app_key
}

def request_nutrition(title, ingredient_list):

    request_body = {
        "title": title,
        "ingr": ingredient_list
    }


    # # Send POST request
    # response = requests.post(api_url, params=params, json=request_body, headers=headers)
    
    
    # # Check the response
    # if response.status_code == 200:
    #     print("Request successful. Response:")
    #     # print(response.json())

    #     with open("nutrition_test.json", 'w') as json_file:
    #         json.dump(response.json(), json_file, indent=2)
    # else:
    #     print(f"Request failed with status code {response.status_code}. Response:")
    #     print(response.text)

    # return response.json()
