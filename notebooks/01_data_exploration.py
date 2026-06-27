# Databricks notebook source
# MAGIC %md
# MAGIC # 01 — Data Exploration
# MAGIC Load raw CSVs from ADLS and explore schema, row counts, and basic statistics.

# COMMAND ----------

# MAGIC %md
# MAGIC ## 1. Load Data

# COMMAND ----------

from pyspark.sql import SparkSession
from pyspark.sql.functions import col, count, avg, min, max

spark = SparkSession.builder.appName("FoodDelivery_Exploration").getOrCreate()

# Update these paths when running on Databricks with ADLS mount
# Example: "abfss://raw@<storage_account>.dfs.core.windows.net/Restaurants.csv"
BASE_PATH = "/mnt/adls/raw"

restaurants_df = spark.read.csv(f"{BASE_PATH}/Restaurants.csv", header=True, inferSchema=True)
drivers_df     = spark.read.csv(f"{BASE_PATH}/Drivers.csv",     header=True, inferSchema=True)
orders_df      = spark.read.csv(f"{BASE_PATH}/Orders.csv",      header=True, inferSchema=True)
reviews_df     = spark.read.csv(f"{BASE_PATH}/Reviews.csv",     header=True, inferSchema=True)

# COMMAND ----------

# MAGIC %md
# MAGIC ## 2. Schema & Row Counts

# COMMAND ----------

print("=== Restaurants ===")
restaurants_df.printSchema()
print(f"Row count: {restaurants_df.count()}")

print("\n=== Drivers ===")
drivers_df.printSchema()
print(f"Row count: {drivers_df.count()}")

print("\n=== Orders ===")
orders_df.printSchema()
print(f"Row count: {orders_df.count()}")

print("\n=== Reviews ===")
reviews_df.printSchema()
print(f"Row count: {reviews_df.count()}")

# COMMAND ----------

# MAGIC %md
# MAGIC ## 3. Basic Statistics

# COMMAND ----------

print("--- Restaurant Rating Distribution ---")
restaurants_df.describe("Rating").show()

print("--- Order Amount Statistics ---")
orders_df.describe("OrderAmount").show()

print("--- Preparation Delay Statistics ---")
orders_df.describe("PreparationDelayMins").show()

print("--- Driver Wait Time Statistics ---")
orders_df.describe("DriverWaitMins").show()

# COMMAND ----------

# MAGIC %md
# MAGIC ## 4. Order Status Breakdown

# COMMAND ----------

orders_df.groupBy("OrderStatus").agg(count("*").alias("Count")).show()

# COMMAND ----------

# MAGIC %md
# MAGIC ## 5. Top 10 Restaurants by Order Volume

# COMMAND ----------

(orders_df
    .groupBy("RestaurantID")
    .agg(count("*").alias("TotalOrders"))
    .orderBy(col("TotalOrders").desc())
    .limit(10)
    .show())
