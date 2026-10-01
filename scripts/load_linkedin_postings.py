import os
from pathlib import Path

import pandas as pd
from dotenv import load_dotenv
from sqlalchemy import create_engine, text
from sqlalchemy.engine import URL

ROOT = Path(__file__).resolve().parent.parent
load_dotenv(ROOT / ".env")

engine = create_engine(URL.create(
    "mysql+pymysql",
    username=os.getenv("DB_USER"),
    password=os.getenv("DB_PASSWORD"),
    host=os.getenv("DB_HOST", "localhost"),
    database=os.getenv("DB_NAME", "job_market"),
))

COLS = [
    "job_id", "company_name", "title", "location", "company_id",
    "formatted_work_type", "work_type", "formatted_experience_level",
    "remote_allowed", "sponsored", "application_type", "posting_domain",
    "pay_period", "currency", "compensation_type",
    "min_salary", "med_salary", "max_salary", "normalized_salary",
    "views", "applies",
    "listed_time", "original_listed_time", "closed_time", "expiry",
    "skills_desc",
]
TIME_COLS = ["listed_time", "original_listed_time", "closed_time", "expiry"]

with engine.begin() as conn:
    conn.execute(text("TRUNCATE TABLE linkedin_postings"))

total = 0
for chunk in pd.read_csv(ROOT / "data" / "raw" / "postings.csv",
                         usecols=COLS, chunksize=10000):
    for c in TIME_COLS:
        chunk[c] = pd.to_datetime(chunk[c], unit="ms", errors="coerce")
    chunk = chunk[COLS]
    chunk.to_sql("linkedin_postings", engine, if_exists="append", index=False)
    total += len(chunk)
    print(f"Loaded {total:,} rows", flush=True)

print("Done")