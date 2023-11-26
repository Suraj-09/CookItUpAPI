import requests
import time
import pandas as pd

class ApiOperations:
    BASE_URL = "http://127.0.0.1:8000"

    @staticmethod
    def your_api_method(data):
        url = f"{ApiOperations.BASE_URL}/generate_recipe"
        response = requests.post(url, json=data)
        return response.json()

# List of ingredients
ingredients_list = [
    "provolone cheese, bacon, bread, ginger",
    "sugar, crunchy jif peanut butter, cornflakes",
    "sweet butter, confectioners sugar, flaked coconut, condensed milk, nuts, vanilla, dipping chocolate",
    "macaroni, butter, salt, bacon, milk, flour, pepper, cream corn",
    "hamburger, sausage, onion, regular, american cheese, colby cheese",
    "chicken breasts, onion, garlic, great northern beans, black beans, green chilies, broccoli, garlic oil, butter, cajun seasoning, salt, oregano, thyme, black pepper, basil, Worcestershire sauce, chicken broth, sour cream, chardonnay wine",
    "serrano peppers, garlic, celery, oregano, canola oil, vinegar, water, kosher salt, salt, black pepper"
]

# Function to perform requests and measure time
def perform_requests():
    results = []

    for i, ingredients in enumerate(ingredients_list, start=1):
        input_data = {"ingredients": ingredients}

        start_time = time.time()

        # Replace 'your_api_method' with the actual method you want to test
        response_data = ApiOperations.your_api_method(input_data)

        end_time = time.time()
        elapsed_time = end_time - start_time

        result = {
            "Request Number": i,
            "Input Data": input_data,
            "Response Data": response_data,
            "Elapsed Time (s)": elapsed_time
        }

        print(result)

        results.append(result)

    return results

# Main function
def main():
    # Perform requests and get results
    results = perform_requests()

    # Convert results to a Pandas DataFrame
    df = pd.DataFrame(results)

    # Save the DataFrame to an Excel file
    df.to_excel("api_results_8.xlsx", index=False)
    print("Results saved to api_results.xlsx")

if __name__ == "__main__":
    main()
