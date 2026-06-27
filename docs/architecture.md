# Architecture — Food Delivery Restaurant Performance Analytics Pipeline

## Data Flow

```
┌─────────────────────────────────┐
│   Raw Data Sources              │
│   (Orders, Drivers, Reviews,    │
│    Restaurants)                  │
└──────────────┬──────────────────┘
               │
               ▼
┌─────────────────────────────────┐
│   Azure Data Lake Storage Gen2  │
│   Container: raw/               │
│   ├── Orders.csv                │
│   ├── Drivers.csv               │
│   ├── Restaurants.csv           │
│   └── Reviews.csv               │
└──────────────┬──────────────────┘
               │
               ▼
┌─────────────────────────────────┐
│   Azure Data Factory            │
│   Pipeline: FoodDeliveryPipeline│
│   - Scheduled trigger (4x/day) │
│   - Copies raw → staging        │
│   - Calls Databricks notebooks  │
└──────────────┬──────────────────┘
               │
               ▼
┌─────────────────────────────────┐
│   Azure Databricks              │
│   Notebooks:                    │
│   01 → Data Exploration         │
│   02 → Transformation (PySpark) │
│   03 → Sentiment Analysis       │
│                                 │
│   Outputs:                      │
│   - RestaurantPerformance       │
│   - ReviewsSentiment            │
└──────────────┬──────────────────┘
               │  JDBC write
               ▼
┌─────────────────────────────────┐
│   Azure SQL Warehouse           │
│   Tables:                       │
│   - OrdersFact                  │
│   - RestaurantPerformance       │
│   - ReviewsSentiment            │
└──────────────┬──────────────────┘
               │
               ▼
┌─────────────────────────────────┐
│   Power BI Dashboard            │
│   - Top Restaurants             │
│   - Avg Preparation Delay       │
│   - Sentiment Breakdown         │
│   - Delivery Bottlenecks        │
└─────────────────────────────────┘
```

## Key Design Decisions

| Decision | Rationale |
|---|---|
| CSV as raw format | Simple, widely supported, easy to inspect |
| PySpark for transformations | Scalable, runs natively on Databricks |
| Keyword-based sentiment | Lightweight, no ML model needed for MVP |
| Azure SQL for serving layer | Fast queries for Power BI, supports JDBC |
| ADF for orchestration | Native Azure integration, scheduling, monitoring |
