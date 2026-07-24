from minio import Minio
import os
from pathlib import Path


class MinIOClient:
    def __init__(self):
        self.client = Minio(
            "localhost:9000",
            access_key=os.getenv("MINIO_ROOT_USER"),
            secret_key=os.getenv("MINIO_ROOT_PASSWORD"),
            secure=False
        )


    def create_bucket(self, bucket_name: str) -> None:
        client = self.client

        if client.bucket_exists(bucket_name):
            print(f"{bucket_name} exists")
        else:
            client.make_bucket(bucket_name)
            print(f"Created {bucket_name} bucket")


    def upload_file(self, bucket_name: str, object_name: str, file_path: Path) -> None:
        client = self.client

        client.fput_object(
            bucket_name,
            object_name,
            file_path
        )

        print(f"Uploaded {file_path} to {bucket_name}/{object_name}")



if __name__ == "__main__":
    client = MinIOClient()
    client.create_bucket("test")
