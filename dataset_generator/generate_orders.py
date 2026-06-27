"""
generate_orders.py
------------------
Generates 100,000 realistic food delivery orders.
- Cuisine-based preparation times
- Peak-hour order distribution
- Driver wait time calculations
- Payment methods & order statuses
Output: data/raw/Orders.csv
"""

import csv
import random
import os
import sys
from datetime import datetime, timedelta

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from config.config import RAW_DATA_DIR
from dataset_generator.utils import (
    generate_order_time, get_preparation_time,
    get_driver_arrival_offset, get_delivery_duration
)


def load_data():
    restaurants = []
    with open(os.path.join(RAW_DATA_DIR, 'Restaurants.csv'), 'r', encoding='utf-8') as f:
        for row in csv.DictReader(f):
            restaurants.append(row)

    drivers = []
    with open(os.path.join(RAW_DATA_DIR, 'Drivers.csv'), 'r', encoding='utf-8') as f:
        for row in csv.DictReader(f):
            drivers.append(row)

    return restaurants, drivers


def get_restaurant_weights(restaurants):
    weights = []
    for r in restaurants:
        rating = float(r['Rating'])
        if rating >= 4.5:
            weights.append(50)
        elif rating >= 4.0:
            weights.append(25)
        elif rating >= 3.0:
            weights.append(10)
        else:
            weights.append(3)
    return weights


def generate_orders(num_orders=100000):
    restaurants, drivers = load_data()
    rest_weights = get_restaurant_weights(restaurants)

    # 3 months of data
    end_date = datetime.now()
    start_date = end_date - timedelta(days=90)

    payment_methods = ['Credit Card', 'Debit Card', 'UPI', 'Cash on Delivery', 'Wallet']
    order_statuses = ['Delivered'] * 90 + ['Cancelled'] * 5 + ['Refunded'] * 5

    output_file = os.path.join(RAW_DATA_DIR, 'Orders.csv')
    print(f"Generating {num_orders} orders...")

    with open(output_file, 'w', newline='', encoding='utf-8') as f:
        fieldnames = [
            'OrderID', 'RestaurantID', 'DriverID', 'OrderTime', 'FoodReadyTime',
            'DriverArrivalTime', 'PickupTime', 'DeliveryTime',
            'PreparationDelayMins', 'DriverWaitMins', 'DeliveryDurationMins',
            'OrderAmount', 'PaymentMethod', 'OrderStatus'
        ]
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()

        for i in range(1, num_orders + 1):
            if i % 10000 == 0:
                print(f"  Processed {i:,} / {num_orders:,} orders...")

            rest = random.choices(restaurants, weights=rest_weights, k=1)[0]
            driver = random.choice(drivers)

            order_time = generate_order_time(start_date, end_date)
            prep_time = get_preparation_time(rest['Cuisine'], float(rest['Rating']))
            food_ready_time = order_time + timedelta(minutes=prep_time)

            driver_offset = get_driver_arrival_offset()
            driver_arrival_time = order_time + timedelta(minutes=driver_offset)
            pickup_time = max(food_ready_time, driver_arrival_time) + timedelta(minutes=random.randint(1, 4))

            delivery_dur = get_delivery_duration()
            delivery_time = pickup_time + timedelta(minutes=delivery_dur)

            prep_delay = (food_ready_time - order_time).total_seconds() / 60.0
            driver_wait = (pickup_time - driver_arrival_time).total_seconds() / 60.0

            amt = round(random.uniform(150, 2500), 2)
            payment = random.choice(payment_methods)
            status = random.choice(order_statuses)

            if status != 'Delivered':
                delivery_time_str = ''
                delivery_dur_str = ''
            else:
                delivery_time_str = delivery_time.strftime('%Y-%m-%d %H:%M:%S')
                delivery_dur_str = round(delivery_dur, 1)

            writer.writerow({
                'OrderID': f"O{str(i).zfill(7)}",
                'RestaurantID': rest['RestaurantID'],
                'DriverID': driver['DriverID'],
                'OrderTime': order_time.strftime('%Y-%m-%d %H:%M:%S'),
                'FoodReadyTime': food_ready_time.strftime('%Y-%m-%d %H:%M:%S'),
                'DriverArrivalTime': driver_arrival_time.strftime('%Y-%m-%d %H:%M:%S'),
                'PickupTime': pickup_time.strftime('%Y-%m-%d %H:%M:%S'),
                'DeliveryTime': delivery_time_str,
                'PreparationDelayMins': round(prep_delay, 1),
                'DriverWaitMins': round(driver_wait, 1),
                'DeliveryDurationMins': delivery_dur_str,
                'OrderAmount': amt,
                'PaymentMethod': payment,
                'OrderStatus': status
            })

    print(f"✅ Finished generating {num_orders:,} orders → {output_file}")


if __name__ == '__main__':
    generate_orders(100000)