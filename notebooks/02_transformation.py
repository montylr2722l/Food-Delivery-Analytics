# Databricks notebook source
# MAGIC %md
# MAGIC # 02 — Transformation
# MAGIC Calculate restaurant-level performance metrics:
# MAGIC - Average preparation delay
# MAGIC - Average driver wait time
# MAGIC - Total orders & revenue
# MAGIC - Delivery success rate

# COMMAND ----------

from pyspark.sql import SparkSession
from pyspark.sql.functions import col, avg, count, sum as spark_sum, round as spark_round, when

spark = SparkSession.builder.appName("FoodDelivery_Transformation").getOrCreate()

BASE_PATH = "/mnt/adls/raw"

orders_df      = spark.read.csv(f"{BASE_PATH}/Orders.csv",      header=True, inferSchema=True)
restaurants_df = spark.read.csv(f"{BASE_PATH}/Restaurants.csv", header=True, inferSchema=True)

# COMMAND ----------

# MAGIC %md
# MAGIC ## 1. Restaurant-Level Aggregations

# COMMAND ----------

restaurant_metrics = (
    orders_df
    .groupBy("RestaurantID")
    .agg(
        count("*").alias("TotalOrders"),
        spark_round(avg("PreparationDelayMins"), 2).alias("AvgPreparationDelay"),
        spark_round(avg("DriverWaitMins"), 2).alias("AvgDriverWait"),
        spark_round(avg("OrderAmount"), 2).alias("AvgOrderAmount"),
        spark_round(spark_sum("OrderAmount"), 2).alias("TotalRevenue"),
        spark_round(
            count(when(col("OrderStatus") == "Delivered", True)) / count("*") * 100, 2
        ).alias("DeliverySuccessRate")
    )
)

# COMMAND ----------

# MAGIC %md
# MAGIC ## 2. Join with Restaurant Details

# COMMAND ----------

restaurant_performance = (
    restaurant_metrics
    .join(restaurants_df, on="RestaurantID", how="left")
    .select(
        "RestaurantID",
        "RestaurantName",
        "Cuisine",
        "Rating",
        "TotalOrders",
        "AvgPreparationDelay",
        "AvgDriverWait",
        "AvgOrderAmount",
        "TotalRevenue",
        "DeliverySuccessRate"
    )
    .orderBy(col("TotalOrders").desc())
)

restaurant_performance.show(20, truncate=False)

# COMMAND ----------

# MAGIC %md
# MAGIC ## 3. Save to Azure SQL Warehouse
# MAGIC Uncomment and configure the JDBC connection for your Azure SQL instance.

# COMMAND ----------

# jdbc_url = "jdbc:sqlserver://<server>.database.windows.net:1433;database=<db>"
# connection_properties = {
#     "user": "<username>",
#     "password": "<password>",
#     "driver": "com.microsoft.sqlserver.jdbc.SQLServerDriver"
# }
#
# restaurant_performance.write.jdbc(
#     url=jdbc_url,
#     table="RestaurantPerformance",
#     mode="overwrite",
#     properties=connection_properties
# )
# print("✅ RestaurantPerformance written to Azure SQL Warehouse")
