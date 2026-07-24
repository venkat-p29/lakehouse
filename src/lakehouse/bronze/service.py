from lakehouse.query.duckdb_client import DuckDBClient

class BronzeService:
    def __init__(self, db: DuckDBClient):
        self.db = db

    def materialize(self, table_name: str, source_uri: str, target_uri: str):
        self.db.execute(f"""
            CREATE OR REPLACE TABLE {table_name} AS
            SELECT *
            FROM read_parquet('{source_uri}');
        """) 

        self.db.execute(f"""
            COPY bronze_customers TO '{target_uri}' (FORMAT parquet);
        """)
