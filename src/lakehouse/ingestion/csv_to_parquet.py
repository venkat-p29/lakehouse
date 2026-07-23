import polars as pl


def csv_to_parquet(csv_path: str, parquet_path: str) -> None:
    print(f"Reading {csv_path}")

    df = pl.read_csv(csv_path)

    print("Schema:")
    print(df.schema)

    print(f"Rows: {df.shape[0]}")

    print(f"Writing {parquet_path}")

    df.write_parquet(parquet_path)

    print("Done")


if __name__ == "__main__":
    csv_to_parquet(
        csv_path="./sample_data/customers.csv", 
        parquet_path="./sample_data/customers.parquet"
    )
