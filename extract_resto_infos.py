import json
import os
import requests
from urllib.parse import quote
import sys

# Geoapify API key (replace with your actual key)
GEOAPIFY_API_KEY = 'YOUR_GEOAPIFY_API_KEY'

# Define input and output file paths in the current working directory
input_file = os.path.join(os.getcwd(), 'parsed_restaurants_paris.json')
output_file = os.path.join(os.getcwd(), 'processed_restaurants.json')

# Validate input file existence and content
try:
    with open(input_file, 'r', encoding='utf-8') as f:
        restaurants = json.load(f)
    if not restaurants:
        print(f"Error: Input file '{input_file}' is empty.")
        sys.exit(1)
    print(f"Found {len(restaurants)} restaurants to process.")
except FileNotFoundError:
    print(f"Error: Input file '{input_file}' not found.")
    sys.exit(1)
except json.JSONDecodeError as e:
    print(f"Error: Invalid JSON in '{input_file}': {e}")
    sys.exit(1)

# Process the data to extract name, address, and postalCode
result = []
for i, restaurant in enumerate(restaurants, 1):
    # Extract restaurant_name as name
    name = restaurant.get('restaurant_name')
    print(f"Processing restaurant {i}/{len(restaurants)}: {name or 'Unnamed'}")
    
    # Extract address and determine postalCode
    address = restaurant.get('address')
    postal_code = None  # Default to None if address is missing or no postal code found
    
    if address:
        print(f"  Fetching postal code for address: {address}")
        try:
            # Encode the address for the URL
            encoded_address = quote(address)
            url = f"https://api.geoapify.com/v1/geocode/search?text={encoded_address}&apiKey={GEOAPIFY_API_KEY}"
            
            # Make the API request
            response = requests.get(url, timeout=10)
            response.raise_for_status()  # Raise an error for bad status codes
            data = response.json()
            
            # Extract postal code from the first result
            if data.get('features'):
                properties = data['features'][0].get('properties', {})
                postal_code = properties.get('postcode')
                print(f"  Postal code found: {postal_code or 'None'}")
            else:
                print(f"  No results found for address: {address}")
        except requests.RequestException as e:
            print(f"  Error fetching postal code for address '{address}': {e}")
            postal_code = None
    else:
        print(f"  No address provided for {name or 'Unnamed'}")
    
    # Create the output dictionary with only the requested fields
    restaurant_info = {
        'name': name,
        'address': address,
        'postalCode': postal_code
    }
    
    result.append(restaurant_info)

# Write the result to a new JSON file
try:
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(result, f, indent=2)
    print(f"\nSuccess: Output written to '{output_file}'")
except Exception as e:
    print(f"\nError writing to output file '{output_file}': {e}")
    sys.exit(1)