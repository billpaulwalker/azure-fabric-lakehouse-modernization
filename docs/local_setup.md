# Local Setup

## Purpose

This project is designed as an Azure data engineering portfolio project. Some components are templates meant for Azure Data Factory, Synapse, and Fabric environments.

## Prerequisites

- Git
- VS Code
- Python 3.11+
- Azure subscription
- Azure Data Factory workspace
- ADLS Gen2 storage account
- Synapse workspace or Fabric workspace

## Clone the Repository

```bash
git clone https://github.com/billpaulwalker/azure-fabric-lakehouse-modernization.git
cd azure-fabric-lakehouse-modernization
```

## Install Development Dependencies
pip install -r requirements-dev.txt

## Run Local Validation
ruff check synapse/ fabric/ tests/
pytest -q

## Environment Variables

Copy .env.example and create a local .env file.

cp .env.example .env

Do not commit .env.