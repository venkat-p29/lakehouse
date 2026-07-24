from lakehouse.storage.minio_client import MinIOClient
from lakehouse.ingestion.csv_to_parquet import csv_to_parquet
from lakehouse.query.duckdb_client import DuckDBClient
from lakehouse.storage.object_paths import landing_customer_path
from lakehouse.metadata.manifest import Manifest

import os
from pathlib import Path
from dotenv import load_dotenv
from datetime import date, datetime
import polars as pl
import json

load_dotenv()

PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent.parent
MINIO_USER = os.getenv("MINIO_ROOT_USER")
MINIO_PWD = os.getenv("MINIO_ROOT_PASSWORD")


def ingest_customers():
    # CSV to Parquet
    csv_file = PROJECT_ROOT / "sample_data/customers.csv"
    parquet_file = PROJECT_ROOT / "sample_data/customers.parquet"
    object_path = landing_customer_path("customers.parquet", date.today())
    json_object_path = landing_customer_path("manifest.json", date.today())

    csv_to_parquet(csv_file, parquet_file)
    df = pl.read_parquet(parquet_file)

    # Upload parquet to MinIO
    client = MinIOClient()
    client.create_bucket("lakehouse")
    client.upload_file("lakehouse", object_path, parquet_file)

    # Upload manifest.json 
    manifest = Manifest(
        dataset="customers",
        source_file=str(parquet_file),
        object_path=str(object_path),
        row_count=df.shape[0],
        schema=df.schema,
        ingestion_date=date.today(),
        uploaded_at=datetime.now()
    )
    jstr = json.dumps(manifest.to_dict())
    json_file = PROJECT_ROOT / "sample_data/manifest.json"
    with open(json_file, "w", encoding="utf-8") as f:
        f.write(jstr)

    client.upload_file("lakehouse", json_object_path, json_file)

    # Query using DuckDB
    db = DuckDBClient()
    db.create_minio_secret(
        endpoint="localhost:9000",
        access_key=MINIO_USER, 
        secret_key=MINIO_PWD
    )

    sql = f"""
    SELECT *
    FROM read_parquet(
        's3://lakehouse/{object_path}'
    );
    """

    print(db.execute(sql).pl())
    print(f"Successfully read from s3://lakehouse/{object_path}")


if __name__ == "__main__":
    ingest_customers()
