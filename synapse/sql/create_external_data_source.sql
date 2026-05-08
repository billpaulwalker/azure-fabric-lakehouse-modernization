CREATE MASTER KEY ENCRYPTION BY PASSWORD = 'Replace_With_Strong_Demo_Password_123!';
GO

CREATE DATABASE SCOPED CREDENTIAL WorkspaceIdentity
WITH IDENTITY = 'Managed Identity';
GO

CREATE EXTERNAL DATA SOURCE AzureDataLake
WITH (
    LOCATION = 'abfss://datalake@<storage-account-name>.dfs.core.windows.net',
    CREDENTIAL = WorkspaceIdentity
);
GO

CREATE EXTERNAL FILE FORMAT ParquetFileFormat
WITH (
    FORMAT_TYPE = PARQUET
);
GO