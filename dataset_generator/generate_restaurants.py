"""
generate_restaurants.py
-----------------------
Generates 5000 restaurants with cuisines, names, and ratings.
Output: data/raw/Restaurants.csv
"""

import csv
import random
import os
import sys

# Add project root to path for config import
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from config.config import RAW_DATA_DIR


def generate_restaurants(num_restaurants=5000):

    cuisines = [
        "Fast Food",
        "Pizza",
        "Italian",
        "Indian",
        "Chinese",
        "Healthy",
        "Desserts",
        "Mexican",
        "South Indian",
        "North Indian",
        "Biryani",
        "Burger",
        "Cafe",
        "Bakery",
        "Thai",
        "Mughlai",
        "Street Food",
        "Seafood",
        "Continental",
        "BBQ"
    ]

    names_part1 = [
        "Taste of",
        "Spice",
        "Golden",
        "Urban",
        "The",
        "Happy",
        "Hot",
        "Quick",
        "Fresh",
        "Royal",
        "Classic",
        "Foodie's",
        "Grand",
        "Express",
        "Delight",
        "Blue",
        "Green",
        "Red",
        "Magic",
        "King"
    ]

    names_part2 = [
        "Bites",
        "Bowl",
        "Plate",
        "Grill",
        "Wok",
        "Spoon",
        "Oven",
        "Kitchen",
        "Diner",
        "Cafe",
        "House",
        "Corner",
        "Palace",
        "Point",
        "Treat",
        "Hub",
        "Garden",
        "Express",
        "Junction",
        "Restaurant"
    ]

    restaurants = []

    used_names = set()

    for i in range(1, num_restaurants + 1):

        while True:
            name = f"{random.choice(names_part1)} {random.choice(names_part2)}"

            if name not in used_names:
                used_names.add(name)
                break

            name = f"{name} {i}"
            if name not in used_names:
                used_names.add(name)
                break

        # Better rating distribution
        p = random.random()

        if p <= 0.10:
            rating = round(random.uniform(2.5, 3.2), 1)

        elif p <= 0.35:
            rating = round(random.uniform(3.3, 3.9), 1)

        elif p <= 0.75:
            rating = round(random.uniform(4.0, 4.5), 1)

        else:
            rating = round(random.uniform(4.6, 5.0), 1)

        restaurants.append({

            "RestaurantID": f"R{str(i).zfill(5)}",

            "RestaurantName": name,

            "Cuisine": random.choice(cuisines),

            "Rating": rating

        })

    return restaurants


if __name__ == "__main__":

    rests = generate_restaurants(5000)

    output_file = os.path.join(RAW_DATA_DIR, "Restaurants.csv")

    with open(output_file, "w", newline="", encoding="utf-8") as f:

        writer = csv.DictWriter(
            f,
            fieldnames=[
                "RestaurantID",
                "RestaurantName",
                "Cuisine",
                "Rating"
            ]
        )

        writer.writeheader()

        writer.writerows(rests)

    print(f"✅ Generated {len(rests)} restaurants → {output_file}")