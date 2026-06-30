"""
generate_orders.py
------------------
Generates 500,000 realistic food delivery orders.

Output:
data/row/Orders.csv
"""

import csv
import random
import os
import sys
from datetime import datetime, timedelta

# Add project root
sys.path.insert(
    0,
    os.path.dirname(
        os.path.dirname(
            os.path.abspath(__file__)
        )
    )
)

from config.config import RAW_DATA_DIR

from dataset_generator.utils import (
    generate_order_time,
    get_preparation_time,
    get_driver_arrival_offset,
    get_delivery_duration
)


# -------------------------------------------------------
# Load Restaurants and Drivers
# -------------------------------------------------------

def load_data():

    restaurants = []

    with open(
        os.path.join(RAW_DATA_DIR, "Restaurants.csv"),
        "r",
        encoding="utf-8"
    ) as f:

        reader = csv.DictReader(f)

        for row in reader:
            restaurants.append(row)

    drivers = []

    with open(
        os.path.join(RAW_DATA_DIR, "Drivers.csv"),
        "r",
        encoding="utf-8"
    ) as f:

        reader = csv.DictReader(f)

        for row in reader:
            drivers.append(row)

    return restaurants, drivers


# -------------------------------------------------------
# Restaurant Weight based on Rating
# -------------------------------------------------------

def get_restaurant_weights(restaurants):

    weights = []

    for r in restaurants:

        rating = float(r["Rating"])

        if rating >= 4.6:

            weights.append(50)

        elif rating >= 4.0:

            weights.append(30)

        elif rating >= 3.5:

            weights.append(15)

        else:

            weights.append(5)

    return weights


# -------------------------------------------------------
# Generate Orders
# -------------------------------------------------------

def generate_orders(num_orders=500000):

    restaurants, drivers = load_data()

    rest_weights = get_restaurant_weights(restaurants)

    # 1 Year Data

    end_date = datetime.now()

    start_date = end_date - timedelta(days=365)

    payment_methods = [
        "UPI",
        "Cash",
        "Credit Card",
        "Debit Card",
        "Wallet"
    ]

    order_statuses = (
        ["Delivered"] * 92 +
        ["Cancelled"] * 5 +
        ["Pending"] * 3
    )

    output_file = os.path.join(
        RAW_DATA_DIR,
        "Orders.csv"
    )

    print(f"\nGenerating {num_orders:,} Orders...\n")

    fieldnames = [

        "OrderID",

        "RestaurantID",

        "DriverID",

        "OrderTime",

        "FoodReadyTime",

        "DriverArrivalTime",

        "PickupTime",

        "DeliveryTime",

        "PreparationDelayMins",

        "DriverWaitMins",

        "DeliveryDurationMins",

        "OrderAmount",

        "PaymentMethod",

        "OrderStatus"

    ]

    with open(
        output_file,
        "w",
        newline="",
        encoding="utf-8"
    ) as f:

        writer = csv.DictWriter(
            f,
            fieldnames=fieldnames
        )

        writer.writeheader()

        for i in range(1, num_orders + 1):

            if i % 50000 == 0:

                print(
                    f"Processed {i:,} / {num_orders:,} Orders..."
                )

            # -------------------------------
            # Random Restaurant & Driver
            # -------------------------------

            restaurant = random.choices(
                restaurants,
                weights=rest_weights,
                k=1
            )[0]

            driver = random.choice(drivers)

            # -------------------------------
            # Order Time
            # -------------------------------

            order_time = generate_order_time(
                start_date,
                end_date
            )

            prep_time = get_preparation_time(
                restaurant["Cuisine"],
                float(restaurant["Rating"])
            )

            food_ready_time = order_time + timedelta(
                minutes=prep_time
            )

            driver_offset = get_driver_arrival_offset()

            driver_arrival_time = order_time + timedelta(
                minutes=driver_offset
            )

            pickup_time = max(
                food_ready_time,
                driver_arrival_time
            ) + timedelta(
                minutes=random.randint(1, 4)
            )

            delivery_duration = get_delivery_duration()

            delivery_time = pickup_time + timedelta(
                minutes=delivery_duration
            )

            preparation_delay = round(
                (
                    food_ready_time - order_time
                ).total_seconds() / 60,
                1
            )

            driver_wait = round(
                (
                    pickup_time - driver_arrival_time
                ).total_seconds() / 60,
                1
            )

            order_amount = round(
                random.uniform(99, 1999),
                2
            )

            payment = random.choice(
                payment_methods
            )

            status = random.choice(
                order_statuses
            )

            if status == "Delivered":

                delivery_time_str = delivery_time.strftime(
                    "%Y-%m-%d %H:%M:%S"
                )

                delivery_duration_str = round(
                    delivery_duration,
                    1
                )

            else:

                delivery_time_str = ""

                delivery_duration_str = ""

            writer.writerow({

                "OrderID":
                    f"O{str(i).zfill(7)}",

                "RestaurantID":
                    restaurant["RestaurantID"],

                "DriverID":
                    driver["DriverID"],

                "OrderTime":
                    order_time.strftime(
                        "%Y-%m-%d %H:%M:%S"
                    ),

                "FoodReadyTime":
                    food_ready_time.strftime(
                        "%Y-%m-%d %H:%M:%S"
                    ),

                "DriverArrivalTime":
                    driver_arrival_time.strftime(
                        "%Y-%m-%d %H:%M:%S"
                    ),

                "PickupTime":
                    pickup_time.strftime(
                        "%Y-%m-%d %H:%M:%S"
                    ),

                "DeliveryTime":
                    delivery_time_str,

                "PreparationDelayMins":
                    preparation_delay,

                "DriverWaitMins":
                    driver_wait,

                "DeliveryDurationMins":
                    delivery_duration_str,

                "OrderAmount":
                    order_amount,

                "PaymentMethod":
                    payment,

                "OrderStatus":
                    status

            })

        print(f"\n✅ Successfully Generated {num_orders:,} Orders")
    print(f"📂 Saved to : {output_file}")


# -------------------------------------------------------
# Main
# -------------------------------------------------------

if __name__ == "__main__":

    random.seed(42)     # Same dataset every time (optional)

    generate_orders(
        num_orders=500000
    )