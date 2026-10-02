import os
from pathlib import Path

import pandas as pd
from dotenv import load_dotenv
from sqlalchemy import create_engine, text
from sqlalchemy.engine import URL

ROOT = Path(__file__).resolve().parent.parent
load_dotenv(ROOT / ".env")
RAW = ROOT / "data" / "raw"

engine = create_engine(URL.create(
    "mysql+pymysql",
    username=os.getenv("DB_USER"),
    password=os.getenv("DB_PASSWORD"),
    host=os.getenv("DB_HOST", "localhost"),
    database=os.getenv("DB_NAME", "job_market"),
))

TABLES = [
    ("linkedin_skills", RAW / "mappings" / "skills.csv"),
    ("linkedin_job_skills", RAW / "jobs" / "job_skills.csv"),
    ("linkedin_industries", RAW / "mappings" / "industries.csv"),
    ("linkedin_job_industries", RAW / "jobs" / "job_industries.csv"),
]

with engine.begin() as conn:
    for name, _ in TABLES:
        conn.execute(text(f"TRUNCATE TABLE {name}"))

for name, path in TABLES:
    df = pd.read_csv(path).drop_duplicates()
    df.to_sql(name, engine, if_exists="append", index=False, chunksize=10000)
    print(f"{name}: {len(df):,} rows")
print("Done")