from dataclasses import dataclass, asdict
from datetime import date, datetime
from polars import Schema
import polars as pl


@dataclass
class Manifest:
    dataset: str
    source_file: str
    object_path: str
    row_count: int
    schema: dict[str, str] | Schema
    ingestion_date: date
    uploaded_at: datetime

    def to_dict(self) -> dict:
        self.ingestion_date = self.ingestion_date.isoformat()
        self.uploaded_at = self.uploaded_at.isoformat()

        if isinstance(self.schema, Schema):
            self.schema = {
                col: str(dtype)
                for col, dtype in self.schema.items()
            }

        return asdict(self)


if __name__ == "__main__":
    # This is a test, ignore full paths - will be deleted post-testing
    df = pl.read_parquet("/home/entropy/workspace/programming/lakehouse/sample_data/customers.parquet")
    schema = df.schema

    manifest = Manifest(
        dataset="customers",
        source_file="customers.parquet",
        object_path="loc/to/obj",
        row_count=4,
        schema=schema,
        ingestion_date=date.today(),
        uploaded_at=datetime.now()
    )

    print(manifest.to_dict())
