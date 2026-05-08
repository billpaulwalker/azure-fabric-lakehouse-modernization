from pyspark.sql import SparkSession
from pyspark.sql.functions import countDistinct, current_timestamp, round, sum as spark_sum

spark = SparkSession.builder.getOrCreate()

storage_account_name = "<storage-account-name>"
container_name = "datalake"

base_path = f"abfss://{container_name}@{storage_account_name}.dfs.core.windows.net"
silver_orders_path = f"{base_path}/silver/orders"
gold_sales_summary_path = f"{base_path}/gold/sales_summary_by_day"

orders_df = spark.read.format("parquet").load(silver_orders_path)

gold_sales_summary_df = (
    orders_df
    .groupBy("order_date", "currency")
    .agg(
        countDistinct("order_id").alias("order_count"),
        countDistinct("customer_id").alias("unique_customer_count"),
        round(spark_sum("order_total"), 2).alias("gross_sales_amount"),
    )
    .withColumn("gold_processed_at_utc", current_timestamp())
)

(
    gold_sales_summary_df
    .write
    .mode("overwrite")
    .format("parquet")
    .partitionBy("order_date")
    .save(gold_sales_summary_path)
)

print(f"Gold rows written: {gold_sales_summary_df.count()}")