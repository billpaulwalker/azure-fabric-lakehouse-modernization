CREATE OR ALTER VIEW dbo.vw_sales_summary_by_day AS
SELECT
    order_date,
    currency,
    order_count,
    unique_customer_count,
    gross_sales_amount,
    CASE
        WHEN unique_customer_count = 0 THEN NULL
        ELSE gross_sales_amount / unique_customer_count
    END AS sales_per_customer,
    gold_processed_at_utc
FROM dbo.ext_gold_sales_summary_by_day;
GO