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