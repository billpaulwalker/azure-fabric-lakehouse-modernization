from pyspark.sql import SparkSession
from pyspark.sql.functions import col, current_timestamp, input_file_name, lit, to_date, trim, upper, when
from pyspark.sql.types import StructField, StructType, StringType, DoubleType

spark = SparkSession.builder.getOrCreate()

storage_account_name = "<storage-account-name>"
container_name = "datalake"
load_date = "2026-05-07"

base_path = f"abfss://{container_name}@{storage_account_name}.dfs.core.windows.net"
bronze_path = f"{base_path}/bronze/sample_api/orders/load_date={load_date}/*.json"
silver_path = f"{base_path}/silver/orders"
quarantine_path = f"{base_path}/quarantine/orders/load_date={load_date}"

orders_schema = StructType([
    StructField("order_id", StringType(), True),
    StructField("customer_id", StringType(), True),
    StructField("order_date", StringType(), True),
    StructField("order_status", StringType(), True),
    StructField("order_total", DoubleType(), True),
    StructField("currency", StringType(), True),
    StructField("source_system", StringType(), True),
])

raw_orders_df = (
    spark.read
    .schema(orders_schema)
    .option("multiline", "true")
    .json(bronze_path)
    .withColumn("source_file", input_file_name())
    .withColumn("bronze_load_date", lit(load_date))
    .withColumn("bronze_loaded_at_utc", current_timestamp())
)

standardized_orders_df = (
    raw_orders_df
    .withColumn("order_id", trim(col("order_id")))
    .withColumn("customer_id", trim(col("customer_id")))
    .withColumn("order_status", upper(trim(col("order_status"))))
    .withColumn("currency", upper(trim(col("currency"))))
    .withColumn("order_date", to_date(col("order_date")))
    .withColumn(
        "source_system",
        when(col("source_system").isNull(), lit("sample_api")).otherwise(col("source_system"))
    )
    .withColumn("silver_processed_at_utc", current_timestamp())
)

valid_orders_df = (
    standardized_orders_df
    .filter(col("order_id").isNotNull())
    .filter(col("customer_id").isNotNull())
    .filter(col("order_date").isNotNull())
    .filter(col("order_total") >= 0)
)

invalid_orders_df = standardized_orders_df.subtract(valid_orders_df)

(
    invalid_orders_df
    .write
    .mode("overwrite")
    .format("parquet")
    .save(quarantine_path)
)

(
    valid_orders_df
    .write
    .mode("append")
    .format("parquet")
    .partitionBy("order_date")
    .save(silver_path)
)

print(f"Bronze rows read: {raw_orders_df.count()}")
print(f"Valid silver rows written: {valid_orders_df.count()}")
print(f"Invalid quarantine rows written: {invalid_orders_df.count()}")