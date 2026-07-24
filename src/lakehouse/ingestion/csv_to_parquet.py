import polars as pl
from pathlib import Path


def csv_to_parquet(csv_path: Path, parquet_path: Path) -> None:
    print(f"Reading csv file: {csv_path}")

    df = pl.read_csv(csv_path)

    print(f"Schema: {df.schema}")
    print(f"Rows: {df.shape[0]}")

    print(f"Writing as parquet to: {parquet_path}")

    df.write_parquet(parquet_path)

    print("Written successfully!")
