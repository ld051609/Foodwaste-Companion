from flask import Flask, request, jsonify, session
from flask_cors import CORS
from flask_session import Session
from location import get_local_food_market, get_food_banks_nearby
from food_api import generate_recipe
from model import get_country_production_prediction_model
from datetime import datetime
import random
app = Flask(__name__)

CORS(app)

# Global variables
produced_ingredients_recipe = []
dietary_restrictions = []

@app.route('/webhook', methods=['POST', 'GET'])
def webhook():
    if request.method == 'POST':
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
            fulfillment_messages = []
            for info in market_info:
                card_response = {
                    "card": {
                        "title": info['name'],
                        "subtitle": "Local Market",
                        "imageUri": info['image_url'],
                        "buttons": [
                            {
                                "text": "More Info",
                                "postback": info['maps_url']
                            }
                        ]
                    }
                }
                fulfillment_messages.append(card_response)
            
            # Return the JSON response
            return jsonify({"fulfillmentMessages": fulfillment_messages})

        
        elif action == 'food-banks':
            address = query_result['parameters']['location'][0]
            city = address.get('city')
            street_address = address.get('street-address')
            print(address)
            market_info = get_local_food_market(street_address, city)
            fulfillment_messages = []
            for info in market_info:
                card_response = {
                    "card": {
                        "title": info['name'],
                        "subtitle": "Local Market",
                        "imageUri": info['image_url'],
                        "buttons": [
                            {
                                "text": "More Info",
                                "postback": info['maps_url']
                            }
                        ]
                    }
                }
                fulfillment_messages.append(card_response)
            
            # Return the JSON response
            return jsonify({"fulfillmentMessages": fulfillment_messages})
        
        elif action == 'recipe - location':
            country = query_result['parameters']['geo-country']
            year = datetime.now().year
            produced_ingredients = get_country_production_prediction_model(country, year)
            if produced_ingredients is None:
                return jsonify({'fulfillmentText': f"Sorry, no data available for {country}. Please try again."})
            
            # Clear previous data and store new data
            if len(produced_ingredients_recipe) > 0:
                produced_ingredients_recipe.clear
            produced_ingredients_recipe.extend(produced_ingredients)

            items = ', '.join([item for item in produced_ingredients]) 
            return jsonify({
                'fulfillmentText': f"Top 3 food items with the highest predicted production value in {year} of {country}: {items}. To help with creating waste-free recipes, please provide ONE dietary restriction (i.e. gluten-free, vegetarian, sugar-free), or type 'no'."})

        elif action == 'recipe - dietaryRestrictions':
            # Clear previous data and store new data
            if len(dietary_restrictions) > 0:
                dietary_restrictions.clear
            
            dietary_restrictions.extend(query_result['parameters']['food-restriction'])
            return jsonify({'fulfillmentText': 'Please provide ONE more ingredient that you want to combine with. If no, please type "no".'})
        
        elif action == 'recipe - generateCustomRecipe':
            
            print(f'produced_ingredients_recipe: {produced_ingredients_recipe}')
            print(f'dietary_restrictions: {dietary_restrictions}')

            # Random to get one of the top 3 produced ingredients
            new_produced_ingredients_recipe = [x.split()[0] for x in produced_ingredients_recipe]
            random_produced_ingredient = random.choice(new_produced_ingredients_recipe)
            print(f'random_produced_ingredient: {random_produced_ingredient}')

            # Get a list of all ingreients
            total_ingredients = []
            total_ingredients.append(random_produced_ingredient)
            query_text = query_result['queryText'].lower()
            if not 'no' in query_text:
                # append the user input ingredient
                total_ingredients.append(query_result['parameters']['food-items'][0])

            if len(dietary_restrictions) > 0:
                allergy = dietary_restrictions[0]
            else:
                allergy = []

            dish_name, ingredient_list, dish_image, dish_url = generate_recipe(total_ingredients, allergy)
            
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
            
        
        # Testing the webhook
        return jsonify({'fulfillmentText': 'Error: action is not recognized'})

if __name__ == '__main__':
    app.run(debug=True)
