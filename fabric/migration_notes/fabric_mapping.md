# Azure to Fabric Migration Mapping

## Purpose

This document explains how the traditional Azure data platform pattern in this project maps to Microsoft Fabric.

The goal is to show that the current Azure architecture is not wasted work. It can be modernized into Fabric using similar lakehouse principles.

---

## Component Mapping

| Current Azure Component | Fabric Equivalent | Notes |
|---|---|---|
| Azure Data Factory | Fabric Data Pipelines | Used for orchestration and movement |
| ADLS Gen2 | OneLake / Lakehouse Files | Centralized lake storage |
| Synapse Spark | Fabric Notebooks | PySpark transformation layer |
| Parquet files | Delta tables | Fabric favors Delta for lakehouse tables |
| Synapse SQL external views | SQL Analytics Endpoint | SQL access over Lakehouse tables |
| Power BI dataset | Power BI Semantic Model | Reporting and analytics layer |

---

## Migration Strategy

### Phase 1 — Stabilize Current Azure Platform
- Keep ADF as the orchestration layer
- Standardize ADLS Bronze, Silver, and Gold zones
- Add validation and monitoring
- Avoid one-off pipelines

### Phase 2 — Introduce Fabric
- Create Fabric Lakehouse
- Use OneLake shortcuts to existing ADLS data
- Rebuild selected transformations as Fabric notebooks
- Validate row counts and business metrics

### Phase 3 — Modernize Serving Layer
- Move Gold tables into Fabric Lakehouse
- Expose tables through SQL Analytics Endpoint
- Build Power BI semantic model on trusted Gold tables

---

## Interview Positioning

A strong way to explain this project:

> I designed the Azure platform so it supports current-state ADF, ADLS, and Synapse patterns while also being easy to map into Fabric. The same medallion design, PySpark transformation logic, and Gold serving concepts carry forward into Fabric with less platform complexity.