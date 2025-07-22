import json
import os
from geopy.geocoders import Nominatim
from geopy.exc import GeocoderTimedOut, GeocoderServiceError
from time import sleep

# Initialize Nominatim API with a custom user agent
geolocator = Nominatim(user_agent="restaurant_postal_code_fetcher")

# Define input and output file paths in the current working directory
input_file = os.path.join(os.getcwd(), 'parsed_restaurants_paris.json')
output_file = os.path.join(os.getcwd(), 'processed_restaurants.json')

# Read the input JSON file
with open(input_file, 'r', encoding='utf-8') as f:
    restaurants = json.load(f)

# Process the data to extract name, address, and postalCode
result = []
for restaurant in restaurants:
    # Extract restaurant_name as name
    name = restaurant.get('restaurant_name')
    
    # Extract address and determine postalCode
    address = restaurant.get('address')
    postal_code = None  # Default to None if address is missing or no postal code found
    
    if address:
        try:
            # Use Nominatim to geocode the address
            location = geolocator.geocode(address, timeout=10)
            if location and 'postcode' in location.raw.get('address', {}):
                postal_code = location.raw['address']['postcode']
            # Respect Nominatim's rate limit (1 request per second)
            sleep(1)
        except (GeocoderTimedOut, GeocoderServiceError) as e:
            print(f"Error fetching postal code for address '{address}': {e}")
            postal_code = None  # Set to None if geocoding fails
    
    # Create the output dictionary with only the requested fields
    restaurant_info = {
        'name': name,
        'address': address,
        'postalCode': postal_code
    }
    
    result.append(restaurant_info)

# Write the result to a new JSON file
with open(output_file, 'w', encoding='utf-8') as f:
    json.dump(result, f, indent=2)

print(f"Output written to {output_file}")