from datetime import date


def landing_customer_path(file_name: str, ingestion_date: date) -> str:
    return (
        f"landing/customers/"
        f"ingestion_date={ingestion_date.isoformat()}/"
        f"{file_name}"
    )


def bronze_customer_path(file_name: str, ingestion_date: date) -> str:
    return (
        f"bronze/customers/"
        f"ingestion_date={ingestion_date.isoformat()}/"
        f"{file_name}"
    )
