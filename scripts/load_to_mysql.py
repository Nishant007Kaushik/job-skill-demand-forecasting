import os
from pathlib import Path

import pandas as pd
from dotenv import load_dotenv
from sqlalchemy import create_engine, text
from sqlalchemy.engine import URL

ROOT = Path(__file__).resolve().parent.parent
load_dotenv(ROOT / ".env")

url = URL.create(
    "mysql+pymysql",
    username=os.getenv("DB_USER"),
    password=os.getenv("DB_PASSWORD"),
    host=os.getenv("DB_HOST", "localhost"),
    database=os.getenv("DB_NAME", "job_market"),
)
engine = create_engine(url)

df = pd.read_csv(ROOT / "data" / "synthetic_job_postings_2023_2025.csv", parse_dates=["Date"])
df.columns = [c.lower() for c in df.columns]
df = df.rename(columns={"date": "posting_date"})

with engine.begin() as conn:
    conn.execute(text("TRUNCATE TABLE job_postings"))
df.to_sql("job_postings", engine, if_exists="append", index=False, chunksize=2000)
print(f"Loaded {len(df):,} rows into job_postings")