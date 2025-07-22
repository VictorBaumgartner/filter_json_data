import json
import os
import googlemaps
from googlemaps.exceptions import ApiError, TransportError, Timeout

# Initialize Google Maps client 
API_KEY = 'AIzaSyAXTIIKh8BQkXqtXbWVd4swhyv2W7lasyY' 
gmaps = googlemaps.Client(key=API_KEY)

# Define input and output file paths in the current working directory
input_file = os.path.join(os.getcwd(), 'parsed_restaurants_paris.json')
output_file = os.path.join(os.getcwd(), 'processed_restaurants.json')

# Read the input JSON file
with open(input_file, 'r') as f:
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
            # Use Google Places API to geocode the address
            geocode_result = gmaps.geocode(address)
            if geocode_result:
                # Extract postal code from the first result
                for component in geocode_result[0].get('address_components', []):
                    if 'postal_code' in component.get('types', []):
                        postal_code = component['long_name']
                        break
        except (ApiError, TransportError, Timeout) as e:
            print(f"Error fetching postal code for address '{address}': {e}")
            postal_code = None  # Set to None if API call fails
    
    # Create the output dictionary with only the requested fields
    restaurant_info = {
        'name': name,
        'address': address,
        'postalCode': postal_code
    }
    
    result.append(restaurant_info)

# Write the result to a new JSON file
with open(output_file, 'w') as f:
    json.dump(result, f, indent=2)

print(f"Output written to {output_file}")