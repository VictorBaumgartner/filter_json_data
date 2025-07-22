# Process Restaurants with Google Maps API

This Python script reads a JSON file containing restaurant data (names and addresses), geocodes each address using the Google Maps API to extract the **postal code**, and outputs a simplified JSON file with only the restaurant name, address, and postal code.

---

## 📂 Input

- The script expects a file named `parsed_restaurants_paris.json` in the current working directory.
- Each entry in the file should be a dictionary with at least:
  - `restaurant_name`
  - `address`

### Example input (`parsed_restaurants_paris.json`)
```json
[
  {
    "restaurant_name": "Le Gourmet",
    "address": "12 Rue de Paris, 75001 Paris, France"
  }
]
```

---

## 📤 Output

- A file named `processed_restaurants.json` is created in the same directory.
- Each restaurant entry includes:
  - `name`: restaurant name
  - `address`: original address
  - `postalCode`: extracted postal code (or `null` if not found)

### Example output (`processed_restaurants.json`)
```json
[
  {
    "name": "Le Gourmet",
    "address": "12 Rue de Paris, 75001 Paris, France",
    "postalCode": "75001"
  }
]
```

---

## 🔧 Requirements

- Python 3.7+
- `googlemaps` Python package

Install dependencies with:

```bash
pip install -r requirements.txt
```

### `requirements.txt`
```
googlemaps
```

---

## 🔑 Google Maps API Key

To run the script, you need a valid Google Maps API key with **Geocoding API** access enabled.

Replace the line below in the script with your own key:
```python
API_KEY = 'YOUR_GOOGLE_MAPS_API_KEY'
```

> ⚠️ Keep your API key private and secure.

---

## 🛠 How It Works

1. Loads the restaurant data from `parsed_restaurants_paris.json`.
2. For each entry, uses the Google Maps Geocoding API to find the postal code from the address.
3. Handles API errors gracefully (e.g., timeout, transport, quota exceeded).
4. Saves the cleaned data to `processed_restaurants.json`.

---

## 🚨 Error Handling

If the address is missing or the API call fails, the `postalCode` field will be set to `null`, and an error message will be printed to the console.

---

## 📁 File Structure

```
.
├── parsed_restaurants_paris.json    # Input file (you provide)
├── processed_restaurants.json       # Output file (script generates)
├── process_restaurants.py           # The main script
└── requirements.txt                 # Python dependencies
```

---

## 📝 License

This project is provided as-is under the MIT License.
