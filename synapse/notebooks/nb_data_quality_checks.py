from pyspark.sql import SparkSession
from pyspark.sql.functions import col, current_timestamp, lit

spark = SparkSession.builder.getOrCreate()

storage_account_name = "<storage-account-name>"
container_name = "datalake"
load_date = "2026-05-07"

base_path = f"abfss://{container_name}@{storage_account_name}.dfs.core.windows.net"
silver_orders_path = f"{base_path}/silver/orders"
dq_results_path = f"{base_path}/audit/data_quality/orders/load_date={load_date}"

orders_df = spark.read.format("parquet").load(silver_orders_path)

checks = []


def add_check(check_name: str, failed_count: int, severity: str = "ERROR"):
    checks.append((check_name, int(failed_count), severity))


add_check("order_id_not_null", orders_df.filter(col("order_id").isNull()).count())
add_check("customer_id_not_null", orders_df.filter(col("customer_id").isNull()).count())
add_check("order_total_non_negative", orders_df.filter(col("order_total") < 0).count())
add_check("order_date_not_null", orders_df.filter(col("order_date").isNull()).count())

dq_df = (
    spark.createDataFrame(checks, ["check_name", "failed_count", "severity"])
    .withColumn("load_date", lit(load_date))
    .withColumn("checked_at_utc", current_timestamp())
)

(
    dq_df
    .write
    .mode("overwrite")
    .format("parquet")
    .save(dq_results_path)
)

failed_error_count = dq_df.filter(
    (col("severity") == "ERROR") & (col("failed_count") > 0)
).count()

if failed_error_count > 0:
    raise Exception("Data quality validation failed. Review audit output for details.")

print("Data quality checks passed.")