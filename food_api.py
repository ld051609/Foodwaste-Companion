import os
import requests
from dotenv import load_dotenv
load_dotenv()


def generate_recipe(food_items_str, allergic):
    APP_ID = os.getenv('APP_ID')
    APP_KEY = os.getenv('APP_KEY')

    # Assuming food_items_str is a list of strings
    food_items_str = [item.lower() for item in food_items_str]
    food_items_str = ','.join(food_items_str)


    if len(allergic) > 0:
        request_url = f'https://api.edamam.com/search?q={food_items_str}&app_id={APP_ID}&app_key={APP_KEY}&from=1&to=2&health={allergic}'
    else:
        request_url = f'https://api.edamam.com/search?q={food_items_str}&app_id={APP_ID}&app_key={APP_KEY}&from=1&to=2'

    print(request_url)
    response = requests.get(request_url)
    response_json = response.json()
    if response_json['hits']:
        recipe = response_json['hits'][0]['recipe']
        
        dish_name = recipe.get('label', 'No name available')
        dish_image = recipe.get('image', '')
        dish_url = recipe.get('url', '')
        ingredient_list = ', '.join([ingredient for ingredient in recipe.get('ingredientLines', [])])
        
        return dish_name, ingredient_list, dish_image, dish_url
        


# Sample usage
# dish_name, ingredient_list, dish_image, dish_url = generate_recipe(['chicken', 'rice'], 'gluten-free')
# print(dish_name, ingredient_list, dish_image, dish_url)