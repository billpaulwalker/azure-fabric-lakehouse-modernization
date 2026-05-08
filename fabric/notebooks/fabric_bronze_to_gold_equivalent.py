from pyspark.sql.functions import (
    col,
    countDistinct,
    current_timestamp,
    round,
    sum as spark_sum,
    to_date,
    trim,
    upper,
)

bronze_orders_path = "Files/bronze/sample_api/orders/"

orders_df = (
    spark.read
    .option("multiline", "true")
    .json(bronze_orders_path)
)

silver_orders_df = (
    orders_df
    .withColumn("order_id", trim(col("order_id")))
    .withColumn("customer_id", trim(col("customer_id")))
    .withColumn("order_status", upper(trim(col("order_status"))))
    .withColumn("currency", upper(trim(col("currency"))))
    .withColumn("order_date", to_date(col("order_date")))
    .withColumn("silver_processed_at_utc", current_timestamp())
    .filter(col("order_id").isNotNull())
    .filter(col("customer_id").isNotNull())
    .filter(col("order_date").isNotNull())
    .filter(col("order_total") >= 0)
)

silver_orders_df.write.mode("overwrite").format("delta").saveAsTable("silver_orders")

gold_sales_summary_df = (
    silver_orders_df
    .groupBy("order_date", "currency")
    .agg(
        countDistinct("order_id").alias("order_count"),
        countDistinct("customer_id").alias("unique_customer_count"),
        round(spark_sum("order_total"), 2).alias("gross_sales_amount"),
    )
    .withColumn("gold_processed_at_utc", current_timestamp())
)

gold_sales_summary_df.write.mode("overwrite").format("delta").saveAsTable(
    "gold_sales_summary_by_day"
)