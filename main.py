import polars as pl
import os
from sqlalchemy import create_engine
from dotenv import load_dotenv
from datetime import datetime

df_accounts = pl.read_csv("data/accounts.csv")
df_daily = pl.read_csv("data/daily_*.csv")
df_monthly = pl.read_csv("data/monthly_*.csv")
df_special = pl.read_csv("data/daily_20250110.csv")
# print(df_monthly)

special_date = datetime(2025,1,10)
df_special = df_special.with_columns(pl.lit(special_date).alias("changed_datetime"))
df_accounts = df_accounts.with_columns(pl.col("account_id").cast(pl.Int64))
df_monthly = df_monthly.with_columns(pl.col("account").cast(pl.Int64))
df_daily = df_daily.with_columns([
    pl.col("account").cast(pl.Int64),
    pl.col("changed_datetime").str.to_datetime(strict=False)
])

df_daily = pl.concat([df_daily, df_special])

load_dotenv()
db_password = os.getenv("DB_PASSWORD")
port = os.getenv("PORT")
db_name = os.getenv("DB_NAME")

connection = f"postgresql://postgres:{db_password}@localhost:{port}/{db_name}"
engine = create_engine(connection)

df_accounts.write_database(
    table_name="Accounts",
    connection=engine,
    if_table_exists="replace"
)

df_daily.write_database(
    table_name="Daily Status",
    connection=engine,
    if_table_exists="replace"
)

df_monthly.write_database(
    table_name="Monthly Status",
    connection=engine,
    if_table_exists="replace"
)

query = """SELECT a.account_id, a.name, a.address, ds.changed_datetime as latest_update_datetime, ds.queue, ds.status 
    FROM "Accounts" as a 
    LEFT JOIN "Daily Status" as ds ON a.account_id = ds.account 
    WHERE changed_datetime >= TO_DATE('2025-01-01','YYYY-MM-DD');
"""

df_rez = pl.read_database(query=query, connection=engine)
df_rez = df_rez.with_columns(pl.col("latest_update_datetime").dt.strftime("%Y-%m-%d %H:%M:%S"))
# print(df_rez)

df_rez.write_csv("results/rezultat_1-3.csv")

query = """SELECT a.account_id, a.name, a.address, ds.changed_datetime as latest_update_datetime, ds.queue, ds.status 
    FROM "Accounts" as a 
    LEFT JOIN "Daily Status" as ds ON a.account_id = ds.account
"""

df_rez = pl.read_database(query=query, connection=engine)

df_recentQ = (df_rez.filter(
        (pl.col("latest_update_datetime").dt.date() <= pl.date(2025,11,27)) & (pl.col("queue").is_in(["COLLECTIONS", "LEGAL"]))
    )
    .sort("latest_update_datetime", descending=True)
    .group_by("account_id")
    .first()
)

df_recentQ = df_recentQ.with_columns(pl.col("latest_update_datetime").dt.strftime("%Y-%m-%d %H:%M:%S"))
df_recentQ.write_csv("results/rezultat_4.csv")
# print(df_recentQ)