import pandas as pd
import random
from pathlib import Path
from faker import Faker

fake = Faker("en_IN")

# ==============================
# Create Project Paths
# ==============================

BASE_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = BASE_DIR / "data"
DATA_DIR.mkdir(exist_ok=True)

OUTPUT_FILE = DATA_DIR / "Drivers.csv"

# ==============================
# Data Lists
# ==============================

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

vehicles = [
    "Bike",
    "Scooter"
]

status = [
    "Active",
    "Inactive"
]

# ==============================
# Generate Drivers
# ==============================

drivers = []

for i in range(1, 501):

    drivers.append({

        "DriverID": i,

        "DriverName": fake.name(),

        "ExperienceYears": random.randint(1, 10),

        "Vehicle": random.choice(vehicles),

        "City": random.choice(cities),

        "Rating": round(random.uniform(3.5, 5.0), 1),

        "Status": random.choices(
            status,
            weights=[90, 10]
        )[0]

    })

# ==============================
# DataFrame
# ==============================

df = pd.DataFrame(drivers)

df.to_csv(OUTPUT_FILE, index=False)

print("\n✅ Drivers.csv Generated Successfully")
print(f"\n📂 File Saved At:\n{OUTPUT_FILE}")
print(f"\n🚚 Total Drivers: {len(df)}")