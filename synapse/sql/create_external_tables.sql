CREATE EXTERNAL TABLE dbo.ext_gold_sales_summary_by_day
(
    order_date DATE,
    currency VARCHAR(10),
    order_count BIGINT,
    unique_customer_count BIGINT,
    gross_sales_amount FLOAT,
    gold_processed_at_utc DATETIME2
)
WITH (
    LOCATION = '/gold/sales_summary_by_day/',
    DATA_SOURCE = AzureDataLake,
    FILE_FORMAT = ParquetFileFormat
);
GO