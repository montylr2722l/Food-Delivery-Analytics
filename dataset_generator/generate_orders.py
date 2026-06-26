import pandas as pd
import random
from pathlib import Path
from faker import Faker
from datetime import datetime, timedelta

fake = Faker("en_IN")

# ======================================================
# Project Paths
# ======================================================

BASE_DIR = Path(__file__).resolve().parent.parent

DATA_DIR = BASE_DIR / "data"

OUTPUT_FILE = DATA_DIR / "Orders.csv"

# ======================================================
# Load Existing CSV Files
# ======================================================

restaurants = pd.read_csv(DATA_DIR / "Restaurants.csv")
drivers = pd.read_csv(DATA_DIR / "Drivers.csv")

print("Restaurants Loaded :", len(restaurants))
print("Drivers Loaded     :", len(drivers))

# ======================================================
# Constants
# ======================================================

TOTAL_ORDERS = 100000

payment_methods = [
    "UPI",
    "Credit Card",
    "Debit Card",
    "Cash"
]

order_status = [
    "Delivered",
    "Cancelled"
]

cities = [
    "Jaipur",
    "Delhi",
    "Mumbai",
    "Pune",
    "Bengaluru",
    "Hyderabad",
    "Ahmedabad",
    "Chandigarh",
    "Lucknow",
    "Indore"
]

orders = []

print("\nGenerating Orders...\n")

# ======================================================
# Helper Function: Generate Random Date
# ======================================================

def generate_order_date():
    """
    Returns a random date between
    1 Jan 2025 and 31 Dec 2025
    """

    start_date = datetime(2025, 1, 1)
    end_date = datetime(2025, 12, 31)

    days = (end_date - start_date).days

    return start_date + timedelta(days=random.randint(0, days))


# ======================================================
# Helper Function: Generate Order Time
# ======================================================

def generate_order_time():

    hour_probability = random.random()

    # Breakfast
    if hour_probability < 0.10:
        hour = random.randint(7, 10)

    # Lunch Rush
    elif hour_probability < 0.45:
        hour = random.randint(12, 15)

    # Evening
    elif hour_probability < 0.60:
        hour = random.randint(16, 18)

    # Dinner Rush
    elif hour_probability < 0.95:
        hour = random.randint(19, 22)

    # Night
    else:
        hour = random.randint(23, 24) % 24

    minute = random.randint(0, 59)
    second = random.randint(0, 59)

    return hour, minute, second

# ======================================================
# Generate Orders
# ======================================================

for order_id in range(1, TOTAL_ORDERS + 1):

    restaurant = restaurants.sample(1).iloc[0]

    driver = drivers.sample(1).iloc[0]

    order_date = generate_order_date()

    hour, minute, second = generate_order_time()

    order_datetime = order_date.replace(
        hour=hour,
        minute=minute,
        second=second
    )

    orders.append({

        "OrderID": order_id,

        "CustomerID": random.randint(100000, 999999),

        "RestaurantID": restaurant["RestaurantID"],

        "DriverID": driver["DriverID"],

        "OrderDate": order_datetime.strftime("%Y-%m-%d"),

        "OrderTime": order_datetime.strftime("%H:%M:%S"),

        "City": restaurant["City"]

    })

    if order_id % 10000 == 0:
        print(f"{order_id} Orders Generated...")

        # ======================================================
# Save CSV
# ======================================================

orders_df = pd.DataFrame(orders)

orders_df.to_csv(OUTPUT_FILE, index=False)

print("\nOrders.csv Generated Successfully!")

print(f"\nTotal Orders : {len(orders_df)}")

print(f"\nSaved At : {OUTPUT_FILE}")