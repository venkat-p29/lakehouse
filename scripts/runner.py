from lakehouse.storage.minio_client import MinIOClient
from lakehouse.ingestion.csv_to_parquet import csv_to_parquet
from lakehouse.query.duckdb_client import DuckDBClient

import os
from pathlib import Path
from dotenv import load_dotenv

load_dotenv()

PROJECT_ROOT = Path(__file__).resolve().parent.parent
MINIO_USER = os.getenv("MINIO_ROOT_USER")
MINIO_PWD = os.getenv("MINIO_ROOT_PASSWORD")

if __name__ == "__main__":
    file = PROJECT_ROOT / "sample_data/customers.parquet"

    client = MinIOClient()

    client.create_bucket("lakehouse")
    client.upload_file("lakehouse", "landing/customers/customers.parquet", file)

    db = DuckDBClient()
    db.create_minio_secret(
        endpoint="localhost:9000",
        access_key=MINIO_USER, 
        secret_key=MINIO_PWD
    )

    sql = """
    SELECT *
    FROM read_parquet(
        's3://lakehouse/landing/customers/customers.parquet'
    );
    """

    secrets = "select * from duckdb_secrets();"

    print(db.execute(secrets).pl())
    print(db.execute(sql).pl())
