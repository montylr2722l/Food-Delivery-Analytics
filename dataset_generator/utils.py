import random
from datetime import datetime, timedelta

def get_random_date(start_date, end_date):
    """Generates a random datetime between start_date and end_date."""
    delta = end_date - start_date
    int_delta = (delta.days * 24 * 60 * 60) + delta.seconds
    random_second = random.randrange(int_delta)
    return start_date + timedelta(seconds=random_second)

def generate_order_time(start_date, end_date):
    """Generates an order time slightly skewed towards peak hours."""
    date_obj = get_random_date(start_date, end_date)
    # Weights for each hour 0-23 (peak lunch 12-14, peak dinner 18-20)
    weights = [1, 1, 1, 1, 1, 2,  
               3, 5, 8, 10, 15, 25, 
               30, 25, 15, 10, 15, 25, 
               35, 40, 35, 20, 10, 5]
    hour = random.choices(population=range(24), weights=weights, k=1)[0]
    return date_obj.replace(hour=hour, minute=random.randint(0, 59), second=random.randint(0, 59))

def is_weekend(date_obj):
    return date_obj.weekday() >= 5

def get_preparation_time(cuisine, rating):
    """Calculates food preparation time based on cuisine and a random variation."""
    base_time = {
        'Fast Food': 10,
        'Pizza': 15,
        'Italian': 20,
        'Indian': 25,
        'Chinese': 18,
        'Healthy': 12,
        'Desserts': 8,
        'Mexican': 15
    }.get(cuisine, 15)
    
    # Highly rated restaurants might be slightly more consistent
    variation = random.randint(-3, 8)
    return max(5, base_time + variation)

def get_driver_arrival_offset():
    """Driver usually arrives between 2 to 20 minutes after order is placed."""
    return random.randint(2, 20)

def get_delivery_duration():
    """Time taken to deliver from the moment of pickup (8 to 45 mins)."""
    return random.randint(8, 45)
