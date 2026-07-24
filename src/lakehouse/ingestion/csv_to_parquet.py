import polars as pl
from pathlib import Path


def csv_to_parquet(csv_path: Path, parquet_path: Path) -> None:
    print(f"Reading {csv_path}")

    df = pl.read_csv(csv_path)

    print("Schema:")
    print(df.schema)

    print(f"Rows: {df.shape[0]}")

    print(f"Writing {parquet_path}")

    df.write_parquet(parquet_path)

    print("Done")
