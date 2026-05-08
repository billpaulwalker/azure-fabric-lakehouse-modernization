# Data Quality Strategy

## Purpose

Data quality is handled as part of the transformation process instead of being treated as an afterthought.

## Validation Rules

- `order_id` must not be null
- `customer_id` must not be null
- `order_date` must be valid
- `order_total` must be greater than or equal to zero

## Quarantine Pattern

Invalid records are written to a quarantine path for review.

```text
/quarantine/orders/load_date=YYYY-MM-DD/
``

## Fail-Fast Behavior

Critical validation failures raise an exception so orchestration tools can detect pipeline failure quickly.