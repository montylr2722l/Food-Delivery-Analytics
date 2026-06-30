"""
generate_drivers.py
-------------------
Generates 500 drivers with ratings and delivery counts.
Output: data/raw/Drivers.csv
"""

import csv
import random
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from config.config import RAW_DATA_DIR


def generate_drivers(num_drivers=10000):
    drivers = []
    for i in range(1, num_drivers + 1):
        prob = random.random()
        if prob > 0.7:
            rating = round(random.uniform(4.5, 5.0), 1)
        elif prob > 0.2:
            rating = round(random.uniform(3.8, 4.4), 1)
        else:
            rating = round(random.uniform(2.0, 3.7), 1)

        drivers.append({
            'DriverID': f"D{str(i).zfill(5)}",
            'DriverRating': rating,
            'TotalDeliveries': random.randint(50, 5000)
        })
    return drivers


if __name__ == '__main__':
    drivers = generate_drivers(10000)
    output_file = os.path.join(RAW_DATA_DIR, 'Drivers.csv')
    with open(output_file, 'w', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=['DriverID', 'DriverRating', 'TotalDeliveries'])
        writer.writeheader()
        writer.writerows(drivers)
    print(f"✅ Generated {len(drivers)} drivers → {output_file}")