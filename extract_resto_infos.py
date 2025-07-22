import json
import os
import sys

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

# Process the data to extract name and address only
result = []
for i, restaurant in enumerate(restaurants, 1):
    # Extract restaurant_name as name
    name = restaurant.get('restaurant_name')
    print(f"Processing restaurant {i}/{len(restaurants)}: {name or 'Unnamed'}")
    
    # Extract address
    address = restaurant.get('address')
    if not address:
        print(f"  No address provided for {name or 'Unnamed'}")
    
    # Create the output dictionary with only the requested fields
    restaurant_info = {
        'name': name,
        'address': address
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