"""
generate_reviews.py
-------------------
Reads Orders.csv and generates customer reviews with sentiment.
- 40% of orders get a review
- Sentiment based on delivery time and preparation delays
Output: data/row/Reviews.csv
"""

import csv
import random
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from config.config import RAW_DATA_DIR


def generate_reviews():
    positive_reviews = [
        "Amazing food", "Excellent Service", "Quick delivery",
        "Loved the taste", "Perfect packaging", "Driver was very polite",
        "Will order again!", "Fresh and hot"
    ]
    neutral_reviews = [
        "It was okay", "Average experience", "Food was fine",
        "Delivery took a while", "Not bad"
    ]
    negative_reviews = [
        "Very late delivery", "Bad Packing", "Food was cold",
        "Terrible experience", "Driver was rude", "Missing items"
    ]

    orders_file = os.path.join(RAW_DATA_DIR, 'Orders.csv')
    output_file = os.path.join(RAW_DATA_DIR, 'Reviews.csv')

    print("Reading orders...")
    
    all_orders = []
    with open(orders_file, 'r', encoding='utf-8') as f_in:
        reader = csv.DictReader(f_in)
        for row in reader:
            all_orders.append(row)

    print(f"Total orders read: {len(all_orders)}")
    print("Selecting 200,000 orders for reviews...")
    
    # We want exactly 200,000 reviews
    if len(all_orders) < 200000:
        sampled_orders = all_orders
    else:
        sampled_orders = random.sample(all_orders, 200000)

    print("Generating reviews...")
    with open(output_file, 'w', newline='', encoding='utf-8') as f_out:
        fieldnames = ['OrderID', 'RestaurantID', 'Review', 'Sentiment']
        writer = csv.DictWriter(f_out, fieldnames=fieldnames)
        writer.writeheader()

        for row in sampled_orders:
            if row['OrderStatus'] != 'Delivered':
                sentiment = 'Negative'
                review_text = random.choice(negative_reviews)
            else:
                prep_delay = float(row['PreparationDelayMins']) if row['PreparationDelayMins'] else 15
                delivery_dur = float(row['DeliveryDurationMins']) if row['DeliveryDurationMins'] else 30

                if prep_delay > 35 or delivery_dur > 45:
                    prob = random.random()
                    if prob > 0.3:
                        sentiment = 'Negative'
                        review_text = random.choice(negative_reviews)
                    else:
                        sentiment = 'Neutral'
                        review_text = random.choice(neutral_reviews)
                elif prep_delay < 20 and delivery_dur < 25:
                    prob = random.random()
                    if prob > 0.1:
                        sentiment = 'Positive'
                        review_text = random.choice(positive_reviews)
                    else:
                        sentiment = 'Neutral'
                        review_text = random.choice(neutral_reviews)
                else:
                    sentiment = random.choices(
                        ['Positive', 'Neutral', 'Negative'],
                        weights=[50, 30, 20], k=1
                    )[0]
                    if sentiment == 'Positive':
                        review_text = random.choice(positive_reviews)
                    elif sentiment == 'Neutral':
                        review_text = random.choice(neutral_reviews)
                    else:
                        review_text = random.choice(negative_reviews)

            writer.writerow({
                'OrderID': row['OrderID'],
                'RestaurantID': row['RestaurantID'],
                'Review': review_text,
                'Sentiment': sentiment
            })

    print(f"✅ Finished generating {len(sampled_orders):,} reviews → {output_file}")


if __name__ == '__main__':
    random.seed(42) # Ensure reproducibility 
    generate_reviews()
