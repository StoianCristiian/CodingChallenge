import polars as pl
from dotenv import load_dotenv
from sqlalchemy import create_engine
import time, os

load_dotenv()
db_password = os.getenv("DB_PASSWORD")
port = os.getenv("PORT")
db_name = os.getenv("DB_NAME")

connection = f"postgresql://postgres:{db_password}@localhost:{port}/{db_name}"
engine = create_engine(connection)

timer_1 = time.time()

query_1 = 'SELECT * FROM "Accounts" AS a LEFT JOIN "Daily Status" AS ds ON a.account_id = ds.account'
df_slow = pl.read_database(query=query_1, connection=engine)
df_slow = df_slow.filter(pl.col("queue").is_in(["COLLECTIONS", "LEGAL"]))
end_1 = time.time()
print(f"Timp1: {end_1 - timer_1:.4f}")

timer_2 = time.time()
query_2 = """
SELECT a.account_id, a.name, ds.queue, ds.status, ds.changed_datetime
FROM "Accounts" AS a
JOIN "Daily Status" AS ds ON a.account_id = ds.account
WHERE ds.queue IN ('COLLECTIONS', 'LEGAL')
"""
# df_fast = pl.read_database_uri(query=query_2, uri=connection, engine="adbc")
df_fast = pl.read_database(query=query_2, connection=engine)
end_2 = time.time()
print(f"Timp2: {end_2 - timer_2:.4f}")

