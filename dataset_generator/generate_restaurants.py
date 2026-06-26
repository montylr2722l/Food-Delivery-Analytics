import pandas as pd
import random
from pathlib import Path

# ==============================
# Create Project Paths
# ==============================

# Get the project root directory
BASE_DIR = Path(__file__).resolve().parent.parent

# Create the data folder if it doesn't exist
DATA_DIR = BASE_DIR / "data"
DATA_DIR.mkdir(exist_ok=True)

# Output file path
OUTPUT_FILE = DATA_DIR / "Restaurants.csv"

# ==============================
# Restaurant Data
# ==============================

restaurant_names = [
    "Pizza Hut", "Dominos", "KFC", "Burger King", "McDonald's",
    "Subway", "Biryani House", "Royal Kitchen", "Tandoori Nights",
    "Food Palace", "Spice Hub", "The Curry Bowl", "Urban Tadka",
    "Grill Master", "The Food Corner", "Desi Rasoi", "Cafe Aroma",
    "Punjabi Dhaba", "Sizzling Spoon", "The Hungry Chef",
    "Taste of India", "Wrap World", "South Spice", "Chinese Wok",
    "Pizza Point", "Burger Station", "Hot & Crispy", "Masala Magic",
    "BBQ Nation", "Street Bites", "Tasty Treat", "Crispy Chicken",
    "Green Bowl", "Cafe Delight", "Pasta House", "Snack Stop",
    "Royal Biryani", "Momo Point", "Ice Cream Hub", "Fresh Kitchen",
    "Food Express", "Hungry Birds", "Chef's Table", "Meal Box",
    "Kitchen Story", "Food Factory", "The Oven", "Quick Bites",
    "Eat Fresh", "Daily Dine"
]

cities = [
    "Jaipur", "Delhi", "Mumbai", "Pune", "Bengaluru",
    "Hyderabad", "Ahmedabad", "Chandigarh", "Lucknow", "Indore"
]

cuisines = [
    "North Indian",
    "South Indian",
    "Chinese",
    "Pizza",
    "Burger",
    "Fast Food",
    "Biryani",
    "Cafe",
    "Desserts",
    "Multi Cuisine"
]

# ==============================
# Generate Restaurant Records
# ==============================

restaurants = []

for i in range(1, 51):
    restaurants.append({
        "RestaurantID": i,
        "RestaurantName": restaurant_names[i - 1],
        "Cuisine": random.choice(cuisines),
        "City": random.choice(cities),
        "Rating": round(random.uniform(3.5, 5.0), 1)
    })

# ==============================
# Create DataFrame
# ==============================

df = pd.DataFrame(restaurants)

# ==============================
# Save CSV
# ==============================

df.to_csv(OUTPUT_FILE, index=False)

# ==============================
# Success Message
# ==============================

print("\n✅ Restaurants.csv generated successfully!")
print(f"\n📂 File Location:\n{OUTPUT_FILE}")
print(f"\n📊 Total Records: {len(df)}")