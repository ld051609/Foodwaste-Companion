import os
import requests
from dotenv import load_dotenv
load_dotenv()

def generate_recipe(food_items, allergic ):
    APP_ID = os.getenv('APP_ID')
    APP_KEY = os.getenv('APP_KEY')
    request_url = f'https://api.edamam.com/search?q={food_items}&app_id={APP_ID}&app_key={APP_KEY}&from=1&to=1&health={allergic}'
    response = requests.get(request_url).json()

    dish_name = response['label']
    dish_image = response['image']
    dish_url = response['url']
    ingredient_list = ', '.join([ingredient['text'] for ingredient in response['ingredients']])
    return dish_name, ingredient_list, dish_image, dish_url
        


