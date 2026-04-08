import polars as pl
import os
from sqlalchemy import create_engine
from dotenv import load_dotenv

df = pl.DataFrame({
    "id": [1,2,3],
    "user_name": ["mama", "tata", "frate"],
    "signup_date": ["2023-01-01", "2023-05-01", "2024-04-03"],
    "is_active": [True,False,False]
})

load_dotenv()
db_password = os.getenv("DB_PASSWORD")
port = os.getenv("PORT")
db_name = os.getenv("DB_NAME")

connection = f"postgresql://postgres:{db_password}@localhost:{port}/{db_name}"
engine = create_engine(connection)

df.write_database(
    table_name="users_table",
    connection=engine,
    if_table_exists="replace"
)