# Azure to Fabric Migration Strategy

## Goal

Show how a traditional Azure data platform can evolve into Microsoft Fabric without discarding existing design principles.

## Migration Approach

### Phase 1 — Stabilize Azure

- Standardize ADF ingestion
- Organize ADLS using Bronze, Silver, and Gold zones
- Add validation and audit outputs

### Phase 2 — Introduce Fabric

- Create Fabric Lakehouse
- Use OneLake shortcuts where appropriate
- Rebuild selected PySpark transformations in Fabric notebooks

### Phase 3 — Modernize Analytics

- Move Gold tables into Fabric Lakehouse
- Expose data through SQL Analytics Endpoint
- Build Power BI semantic model on trusted Gold tables