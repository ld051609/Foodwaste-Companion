import os
from flask import Flask, request, jsonify
from flask_cors import CORS
import requests
from location import get_local_food_market, get_food_banks_nearby


app = Flask(__name__)
CORS(app)

@app.route('/')
def index():
    return 'Hello World'

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
            return jsonify({'fulfillmentText': f"Here are some local food markets nearby: {market_info}"})
        
        elif action == 'food-banks':
            address = query_result['parameters']['location'][0]
            city = address.get('city')
            street_address = address.get('street-address')
            print(address)
            food_banks = get_food_banks_nearby(street_address, city)
            return jsonify({'fulfillmentText': f"Here are some food banks nearby: {food_banks}"})

        return jsonify({'fulfillmentText': 'Error: action is not recognized'})


    
if __name__ == '__main__':
    app.run(debug=True)
