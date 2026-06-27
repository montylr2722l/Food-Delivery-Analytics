# 🍕 Food Delivery Restaurant Performance Analytics Pipeline

An end-to-end **Azure Data Engineering** project that processes food delivery data to rank restaurant reliability, analyze delivery bottlenecks, and perform sentiment analysis on customer reviews.

## 🏗️ Architecture

```
Raw CSVs → ADLS Gen2 → Azure Data Factory → Databricks (PySpark) → Azure SQL Warehouse → Power BI
```

See [docs/architecture.md](docs/architecture.md) for the detailed data flow diagram.

## 📁 Project Structure

```
Food-Delivery-Analytics/
│
├── config/                     # Centralized configuration
│   └── config.py
│
├── dataset_generator/          # Python scripts to generate realistic mock data
│   ├── utils.py                # Helper functions (time, prep delay logic)
│   ├── generate_restaurants.py # → data/raw/Restaurants.csv
│   ├── generate_drivers.py     # → data/raw/Drivers.csv
│   ├── generate_orders.py      # → data/raw/Orders.csv  (100,000 records)
│   └── generate_reviews.py     # → data/raw/Reviews.csv  (~40,000 records)
│
├── data/
│   └── raw/                    # Generated CSV files (gitignored)
│
├── notebooks/                  # Databricks PySpark notebooks
│   ├── 01_data_exploration.py  # Schema checks, stats, data quality
│   ├── 02_transformation.py    # Compute RestaurantPerformance metrics
│   └── 03_sentiment_analysis.py# Aggregate review sentiments
│
├── sql/                        # Azure SQL Warehouse DDL
│   └── create_tables.sql       # OrdersFact, RestaurantPerformance, ReviewsSentiment
│
├── adf/                        # Azure Data Factory
│   └── pipeline.json           # Pipeline definition (reference)
│
├── powerbi/                    # Power BI setup guide
│   └── README.md
│
├── docs/                       # Documentation
│   └── architecture.md         # Full architecture diagram
│
├── screenshots/                # Dashboard screenshots (add after creating dashboards)
├── .gitignore
├── requirements.txt
└── README.md
```

## 🛠️ Tech Stack

| Service | Purpose |
|---|---|
| **ADLS Gen2** | Store raw CSV data |
| **Azure Data Factory** | Orchestrate and schedule the pipeline |
| **Azure Databricks** | Transform data with PySpark |
| **Azure SQL Warehouse** | Store processed analytics tables |
| **Power BI** | Interactive dashboards and reporting |
| **Python** | Dataset generation and utilities |

## 🚀 Getting Started

### 1. Clone the Repository
```bash
git clone https://github.com/<your-username>/Food-Delivery-Analytics.git
cd Food-Delivery-Analytics
```

### 2. Install Dependencies
```bash
pip install -r requirements.txt
```

### 3. Generate the Dataset
```bash
python dataset_generator/generate_restaurants.py
python dataset_generator/generate_drivers.py
python dataset_generator/generate_orders.py
python dataset_generator/generate_reviews.py
```

This produces 4 CSV files in `data/raw/`:
| File | Records | Description |
|---|---|---|
| `Restaurants.csv` | 250 | Restaurant profiles with cuisines and ratings |
| `Drivers.csv` | 500 | Driver profiles with ratings |
| `Orders.csv` | 100,000 | Orders with timestamps, amounts, statuses |
| `Reviews.csv` | ~40,000 | Customer reviews with sentiment labels |

### 4. Azure Pipeline Setup
1. Upload `data/raw/*.csv` to your **ADLS Gen2** container
2. Import notebooks from `notebooks/` into **Databricks**
3. Run `sql/create_tables.sql` on your **Azure SQL Warehouse**
4. Configure the **ADF pipeline** using `adf/pipeline.json` as reference
5. Connect **Power BI** to Azure SQL (see `powerbi/README.md`)

## 📊 Key Metrics Computed

- **Average Preparation Delay** — per restaurant, by cuisine
- **Average Driver Wait Time** — time driver waits at restaurant
- **Delivery Success Rate** — percentage of successfully delivered orders
- **Sentiment Analysis** — positive/neutral/negative review breakdown
- **Revenue per Restaurant** — total and average order amounts

## 📝 Resume Description

> Built an end-to-end Azure Data Engineering pipeline using ADLS Gen2, Azure Data Factory, Databricks (PySpark), Azure SQL Warehouse, and Power BI to process 100K+ food delivery orders. Calculated preparation delays, driver wait times, and review sentiment to deliver interactive dashboards highlighting top-performing restaurants and delivery bottlenecks.

## 📄 License

This project is for educational purposes.