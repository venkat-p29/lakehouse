import duckdb
from pathlib import Path


sql = """
SELECT * FROM customers;
"""

create_table = """
CREATE TABLE IF NOT EXISTS customers(
    id INTEGER,
    name VARCHAR
)
"""

insert_vals = """
INSERT INTO customers VALUES
(1, 'Alice'),
(2, 'Burgers')
"""


conn = duckdb.connect()

#conn.execute(create_table)
#conn.execute(insert_vals)

#print(conn.execute(sql).fetchall())


file_path = Path("/home/entropy/workspace/programming/lakehouse/sample_data/customers.parquet")

id_plan = (
    conn.execute(f"""
    EXPLAIN ANALYZE
    SELECT customer_id
    FROM read_parquet('{file_path}')
    """).pl().item(0, 1)
)

id_2_plan = (
    conn.execute(f"""
    EXPLAIN ANALYZE
    SELECT customer_id
    FROM read_parquet('{file_path}')
    WHERE customer_id = 2
    """).pl().item(0, 1)
)

print("ID PLAN --------")
print(id_plan)

print("ID PLAN 2 --------")
print(id_2_plan)
