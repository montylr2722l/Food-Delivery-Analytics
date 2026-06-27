# Databricks notebook source
# MAGIC %md
# MAGIC # 03 — Sentiment Analysis
# MAGIC Aggregate review sentiments per restaurant and compute positive review percentages.

# COMMAND ----------

from pyspark.sql import SparkSession
from pyspark.sql.functions import col, count, when, round as spark_round

spark = SparkSession.builder.appName("FoodDelivery_Sentiment").getOrCreate()

BASE_PATH = "/mnt/adls/raw"

reviews_df     = spark.read.csv(f"{BASE_PATH}/Reviews.csv",     header=True, inferSchema=True)
restaurants_df = spark.read.csv(f"{BASE_PATH}/Restaurants.csv", header=True, inferSchema=True)

# COMMAND ----------

# MAGIC %md
# MAGIC ## 1. Sentiment Distribution (Overall)

# COMMAND ----------

reviews_df.groupBy("Sentiment").agg(count("*").alias("Count")).show()

# COMMAND ----------

# MAGIC %md
# MAGIC ## 2. Restaurant-Level Sentiment Aggregation

# COMMAND ----------

sentiment_metrics = (
    reviews_df
    .groupBy("RestaurantID")
    .agg(
        count("*").alias("TotalReviews"),
        count(when(col("Sentiment") == "Positive", True)).alias("PositiveCount"),
        count(when(col("Sentiment") == "Neutral",  True)).alias("NeutralCount"),
        count(when(col("Sentiment") == "Negative", True)).alias("NegativeCount"),
    )
    .withColumn(
        "PositiveReviewPct",
        spark_round(col("PositiveCount") / col("TotalReviews") * 100, 2)
    )
    .withColumn(
        "NegativeReviewPct",
        spark_round(col("NegativeCount") / col("TotalReviews") * 100, 2)
    )
)

# COMMAND ----------

# MAGIC %md
# MAGIC ## 3. Join with Restaurant Names

# COMMAND ----------

review_summary = (
    sentiment_metrics
    .join(restaurants_df, on="RestaurantID", how="left")
    .select(
        "RestaurantID",
        "RestaurantName",
        "TotalReviews",
        "PositiveCount",
        "NeutralCount",
        "NegativeCount",
        "PositiveReviewPct",
        "NegativeReviewPct"
    )
    .orderBy(col("TotalReviews").desc())
)

review_summary.show(20, truncate=False)

# COMMAND ----------

# MAGIC %md
# MAGIC ## 4. Save to Azure SQL Warehouse
# MAGIC Uncomment and configure the JDBC connection for your Azure SQL instance.

# COMMAND ----------

# jdbc_url = "jdbc:sqlserver://<server>.database.windows.net:1433;database=<db>"
# connection_properties = {
#     "user": "<username>",
#     "password": "<password>",
#     "driver": "com.microsoft.sqlserver.jdbc.SQLServerDriver"
# }
#
# review_summary.write.jdbc(
#     url=jdbc_url,
#     table="ReviewsSentiment",
#     mode="overwrite",
#     properties=connection_properties
# )
# print("✅ ReviewsSentiment written to Azure SQL Warehouse")
