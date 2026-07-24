from lakehouse.storage.minio_client import MinIOClient
from lakehouse.ingestion.csv_to_parquet import csv_to_parquet

from pathlib import Path
from dotenv import load_dotenv

load_dotenv()

PROJECT_ROOT = Path(__file__).resolve().parent.parent

if __name__ == "__main__":
    file = PROJECT_ROOT / "sample_data/customers.parquet"

    client = MinIOClient()

    client.create_bucket("lakehouse")
    client.upload_file("lakehouse", "landing/customers/customers.parquet", file)
