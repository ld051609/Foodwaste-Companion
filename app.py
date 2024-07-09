import os
from flask import Flask, request, jsonify
from flask_cors import CORS
import requests
from location import get_local_food_market, get_food_banks_nearby
from food_api import generate_recipe
from model import get_country_production_prediction_model
from datetime import datetime

app = Flask(__name__)
CORS(app)

@app.route('/')
def index():
    return 'Hello World'

@app.route('/webhook', methods=['POST', 'GET'])
def webhook():
    if request.method == 'POST':
        ingredients_for_recipe = []
        dietary_restrictions = []
        req = request.get_json(silent=True, force=True)
        if req is None:
            return jsonify({'fulfillmentText': 'Error: request is None'})
        
        query_result = req.get('queryResult')
        if query_result is None:
            return jsonify({'fulfillmentText': 'Error: queryResult is None'})   
        
        action = query_result['intent']['displayName']
        
        if action == 'find-local-food-market':
            address = query_result['parameters']['location'][0]
            city = address.get('city')
            street_address = address.get('street-address')
            print(address)
            market_info = get_local_food_market(street_address, city)
            return jsonify({'fulfillmentText': f"Here are some local food markets nearby: {market_info}"})
        
        elif action == 'food-banks':
            address = query_result['parameters']['location'][0]
            city = address.get('city')
            street_address = address.get('street-address')
            print(address)
            food_banks = get_food_banks_nearby(street_address, city)
            return jsonify({'fulfillmentText': f"Here are some food banks nearby: {food_banks}"})
        elif action == 'recipe.recipe-custom':
            ingredients = query_result['parameters']['food-items']
            ingredients_for_recipe.append(ingredient for ingredient in ingredients)
            dish_name, ingredient_list, dish_image, dish_url = generate_recipe(ingredients_for_recipe, dietary_restrictions)
            return {
                "fulfillmentMessages": [
                    {
                        "card": {
                            "title": dish_name,
                            "subtitle": ingredient_list,
                            "imageUri": dish_image,
                            "buttons": [
                                {
                                    "text": "View Recipe",
                                    "postback": dish_url
                                }
                            ]
                        }
                    }
                ]
            }
        elif action == 'recipe.recipe-custom':
            country = query_result['parameters']['geo-country']
            year = datetime.now().year
            produced_ingredients = get_country_production_prediction_model(country, year)
            ingredients_for_recipe.append([item['Item'] for item in produced_ingredients])
            items = ', '.join([f"{item['Item']}" for item in produced_ingredients]) 
            return {
                "fulfillmentMessages": f"Top 5 food items with the highest predicted production value in {year} of {country}: {items}. To help with creating waste-free recipes, are there any specific dietary needs or restrictions (i.e. gluten-free, vegetarian, sugar-free), if no, please type 'no'?"
            }
        elif action == 'recipe.recipe-custom':
            dietary_restrictions.append(query_result['parameters']['dietary-restrictions'])
            return{
                "fulfillmentMessages": "Please provide more ingredients that you want to combine with, if no, please type 'no'"
            }



        
        return jsonify({'fulfillmentText': 'Error: action is not recognized'})



    
if __name__ == '__main__':
    app.run(debug=True)
