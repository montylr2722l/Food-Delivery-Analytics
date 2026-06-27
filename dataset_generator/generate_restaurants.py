"""
generate_restaurants.py
-----------------------
Generates 250 restaurants with cuisines, names, and ratings.
Output: data/raw/Restaurants.csv
"""

import csv
import random
import os
import sys

# Add project root to path for config import
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from config.config import RAW_DATA_DIR


def generate_restaurants(num_restaurants=250):
    cuisines = ['Fast Food', 'Pizza', 'Italian', 'Indian', 'Chinese', 'Healthy', 'Desserts', 'Mexican']
    names_part1 = ['Taste of', 'Spice', 'Golden', 'Urban', 'The', 'Happy', 'Hot', 'Quick', 'Fresh']
    names_part2 = ['Bites', 'Bowl', 'Plate', 'Grill', 'Wok', 'Spoon', 'Oven', 'Kitchen', 'Diner']

    restaurants = []
    for i in range(1, num_restaurants + 1):
        name = f"{random.choice(names_part1)} {random.choice(names_part2)}"
        name = f"{name} {i}" if any(r['RestaurantName'] == name for r in restaurants) else name

        # Rating skew: more 4-5 star restaurants than 2-3 star
        rating_prob = random.random()
        if rating_prob > 0.8:
            rating = round(random.uniform(4.5, 5.0), 1)
        elif rating_prob > 0.4:
            rating = round(random.uniform(3.8, 4.4), 1)
        else:
            rating = round(random.uniform(2.5, 3.7), 1)

        restaurants.append({
            'RestaurantID': f"R{str(i).zfill(4)}",
            'RestaurantName': name,
            'Cuisine': random.choice(cuisines),
            'Rating': rating
        })

    return restaurants


if __name__ == '__main__':
    rests = generate_restaurants(250)
    output_file = os.path.join(RAW_DATA_DIR, 'Restaurants.csv')
    with open(output_file, 'w', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=['RestaurantID', 'RestaurantName', 'Cuisine', 'Rating'])
        writer.writeheader()
        writer.writerows(rests)
    print(f"✅ Generated {len(rests)} restaurants → {output_file}")