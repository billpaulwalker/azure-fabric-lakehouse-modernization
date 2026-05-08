# Architecture

## Overview

This project demonstrates a modern Azure lakehouse architecture using Azure Data Factory, ADLS Gen2, Synapse Spark, and Synapse SQL.

## Current-State Azure Architecture

```text
REST API / CSV Files
        ↓
Azure Data Factory
        ↓
ADLS Gen2 Bronze
        ↓
Synapse Spark / PySpark
        ↓
ADLS Gen2 Silver
        ↓
ADLS Gen2 Gold
        ↓
Synapse SQL Views
        ↓
Power BI
```

## Design Principles
- Separate raw, cleaned, and business-ready data
- Use reusable ingestion patterns
- Parameterize pipelines
- Validate data before serving it
- Keep the architecture Fabric-ready