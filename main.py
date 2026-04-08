import polars as pl
import os
from sqlalchemy import create_engine
from dotenv import load_dotenv

df_accounts = pl.read_csv("data/accounts.csv")
df_daily = pl.read_csv("data/daily_*.csv")
df_monthly = pl.read_csv("data/monthly_*.csv")
# print(df_monthly)

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