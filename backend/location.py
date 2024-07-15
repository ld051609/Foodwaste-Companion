import os
from dotenv import load_dotenv
import requests

# Load environment variables from .env file
load_dotenv()

def get_local_food_market(street_address, city=None):
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

            places_url = f'https://maps.googleapis.com/maps/api/place/nearbysearch/json?keyword=farmer_market&location={lat},{lng}&radius=30000&key={GOOGLE_MAPS_API_KEY}'
            places_response = requests.get(places_url)
            places_data = places_response.json()

            if places_data['status'] == 'OK':
                results = places_data['results'][:3]
                locations = []
                for result in results:
                    name = result['name']
                    place_id = result['place_id']
                    image_url = result.get('photos', [{}])[0].get('photo_reference', '')
                    maps_url = f'https://www.google.com/maps/place/?q=place_id:{place_id}'
                    locations.append({
                        "name": name,
                        "maps_url": maps_url,
                        "image_url": image_url
                    })

                return locations
            else:
                return [{"error": f"Places API Error: {places_data.get('error_message', 'Unknown error')}"}]
        else:
            return [{"error": f"Geocode API Error: {geocode_data.get('error_message', 'Unknown error')}"}]

    except Exception as e:
        return [{"error": f"Error occurred: {e}"}]


def get_food_banks_nearby(street_address, city=None):
    try:
        GOOGLE_MAPS_API_KEY = os.getenv('GOOGLE_MAPS_API_KEY')
        geocode_url = f'https://maps.googleapis.com/maps/api/geocode/json?address={street_address}&key={GOOGLE_MAPS_API_KEY}'
        
        geocode_response = requests.get(geocode_url)
        geocode_data = geocode_response.json()

        if geocode_data['status'] == 'OK':
            location = geocode_data['results'][0]['geometry']['location']
            lat, lng = location['lat'], location['lng']

            places_url = f'https://maps.googleapis.com/maps/api/place/nearbysearch/json?keyword=food_bank&location={lat},{lng}&radius=10000&key={GOOGLE_MAPS_API_KEY}'
            places_response = requests.get(places_url)
            places_data = places_response.json()

            if places_data['status'] == 'OK':
                results = places_data['results'][:3]
                locations = []
                for result in results:
                    name = result['name']
                    place_id = result['place_id']
                    image_url = result.get('photos', [{}])[0].get('photo_reference', '')
                    # Get the Google Maps URL for the location_id
                    maps_url = f'https://www.google.com/maps/place/?q=place_id:{place_id}'
                    locations.append({
                        "name": name,
                        "maps_url": maps_url,
                        "image_url": image_url
                    })                
                return locations
            else:
                print(f"Places API Error: {places_data.get('error_message', 'Unknown error')}")
        else:
            print(f"Geocode API Error: {geocode_data.get('error_message', 'Unknown error')}")
        
        return None
    except Exception as e:
        print(f"Error occurred: {e}")
        return None
# Sample usage
# print(get_local_food_market('1600 Amphitheatre Parkway, Mountain View'))