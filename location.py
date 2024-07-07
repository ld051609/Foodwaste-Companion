import os
from dotenv import load_dotenv
import requests
# Load environment variables from .env file
load_dotenv()

def get_local_food_market(street_address, city):        
    try:
        GOOGLE_MAPS_API_KEY = os.getenv('GOOGLE_MAPS_API_KEY')
        if city is None: 
            geocode_url = f'https://maps.googleapis.com/maps/api/geocode/json?address={street_address}&key={GOOGLE_MAPS_API_KEY}'
        else: 
            geocode_url = f'https://maps.googleapis.com/maps/api/geocode/json?address={street_address},{city}&key={GOOGLE_MAPS_API_KEY}'
        
        geocode_response = requests.get(geocode_url)
        geocode_data = geocode_response.json()

        if geocode_data['status'] == 'OK':
            location = geocode_data['results'][0]['geometry']['location']
            lat, lng = location['lat'], location['lng']

            places_url = f'https://maps.googleapis.com/maps/api/place/nearbysearch/json?location={lat},{lng}&radius=5000&type=local_market&key={GOOGLE_MAPS_API_KEY}'
            places_response = requests.get(places_url)
            places_data = places_response.json()

            if places_data['status'] == 'OK':
                results = places_data['results'][:3]
                locations = []
                for result in results:
                    name = result['name']
                    place_id = result['place_id']
                    # Get the Google Maps URL for the location_id
                    maps_url = f'https://www.google.com/maps/place/?q=place_id:{place_id}'
                    locations.append({'name': name, 'maps_url': maps_url})
                print(locations)
                locations = ', '.join([f"{location['name']} ({location['maps_url']})" for location in locations])
                return locations
            else:
                print(f"Places API Error: {places_data.get('error_message', 'Unknown error')}")
        else:
            print(f"Geocode API Error: {geocode_data.get('error_message', 'Unknown error')}")
        
        return None
    except Exception as e:
        print(f"Error occurred: {e}")
        return None

def get_food_banks_nearby(street_address, city):
    try:
        GOOGLE_MAPS_API_KEY = os.getenv('GOOGLE_MAPS_API_KEY')
        if city is None: 
            geocode_url = f'https://maps.googleapis.com/maps/api/geocode/json?address={street_address}&key={GOOGLE_MAPS_API_KEY}'
        else:
            geocode_url = f'https://maps.googleapis.com/maps/api/geocode/json?address={street_address},{city}&key={GOOGLE_MAPS_API_KEY}'
        
        geocode_response = requests.get(geocode_url)
        geocode_data = geocode_response.json()

        if geocode_data['status'] == 'OK':
            location = geocode_data['results'][0]['geometry']['location']
            lat, lng = location['lat'], location['lng']

            places_url = f'https://maps.googleapis.com/maps/api/place/nearbysearch/json?location={lat},{lng}&radius=5000&type=food_bank&key={GOOGLE_MAPS_API_KEY}'
            places_response = requests.get(places_url)
            places_data = places_response.json()

            if places_data['status'] == 'OK':
                results = places_data['results'][:3]
                locations = []
                for result in results:
                    name = result['name']
                    place_id = result['place_id']
                    # Get the Google Maps URL for the location_id
                    maps_url = f'https://www.google.com/maps/place/?q=place_id:{place_id}'
                    locations.append({'name': name, 'maps_url': maps_url})
                print(locations)
                locations = ', '.join([f"{location['name']} ({location['maps_url']})" for location in locations])
                return locations
            else:
                print(f"Places API Error: {places_data.get('error_message', 'Unknown error')}")
        else:
            print(f"Geocode API Error: {geocode_data.get('error_message', 'Unknown error')}")
        
        return None
    except Exception as e:
        print(f"Error occurred: {e}")
        return None