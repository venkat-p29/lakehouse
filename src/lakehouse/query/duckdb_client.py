import duckdb


class DuckDBClient:
    def __init__(self):
        self.conn = duckdb.connect()
        self.conn.execute("INSTALL httpfs")
        self.conn.execute("LOAD httpfs")

    
    def create_minio_secret(
        self,
        endpoint: str, 
        access_key: str, 
        secret_key: str,
        use_ssl: bool = False,
    ):
        self.conn.execute(f"""
        CREATE OR REPLACE SECRET minio (
            TYPE s3,
            PROVIDER config,
            KEY_ID '{access_key}',
            SECRET '{secret_key}',
            ENDPOINT '{endpoint}',
            USE_SSL {use_ssl},
            URL_STYLE 'path'
        ); 
        """)


    def execute(self, sql: str):
        return self.conn.execute(sql)
