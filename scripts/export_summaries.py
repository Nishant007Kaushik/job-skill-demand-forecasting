import os
from pathlib import Path

import pandas as pd
from dotenv import load_dotenv
from sqlalchemy import create_engine, text
from sqlalchemy.engine import URL

ROOT = Path(__file__).resolve().parent.parent
load_dotenv(ROOT / ".env")
OUT = ROOT / "data" / "summaries"
OUT.mkdir(parents=True, exist_ok=True)

engine = create_engine(URL.create(
    "mysql+pymysql",
    username=os.getenv("DB_USER"),
    password=os.getenv("DB_PASSWORD"),
    host=os.getenv("DB_HOST", "localhost"),
    database=os.getenv("DB_NAME", "job_market"),
))


def median_by(label_expr, from_clause, min_n=0):
    """Median annual pay per group. MySQL has no MEDIAN, so take the middle row(s)."""
    return f"""
    SELECT label, MAX(cnt) AS n, ROUND(AVG(pay)) AS median_pay_usd FROM (
      SELECT {label_expr} AS label, c.annual_pay_usd AS pay,
             ROW_NUMBER() OVER (PARTITION BY {label_expr} ORDER BY c.annual_pay_usd) AS rn,
             COUNT(*) OVER (PARTITION BY {label_expr}) AS cnt
      FROM {from_clause}
    ) x
    WHERE rn IN (FLOOR((cnt + 1) / 2), CEIL((cnt + 1) / 2))
    GROUP BY label HAVING n >= {min_n}
    ORDER BY median_pay_usd DESC
    """


QUERIES = {
    "snapshot_info": """
        SELECT COUNT(*) AS total_postings,
               MIN(listed_time) AS first_listed, MAX(listed_time) AS last_listed
        FROM linkedin_postings""",

    "coverage_and_cleaning": """
        SELECT COUNT(*) AS total_postings,
          SUM(EXISTS (SELECT 1 FROM linkedin_job_skills js WHERE js.job_id = p.job_id)) AS with_skill_tag,
          SUM(EXISTS (SELECT 1 FROM linkedin_job_industries ji WHERE ji.job_id = p.job_id)) AS with_industry_tag,
          SUM(p.currency = 'USD' AND p.normalized_salary IS NOT NULL) AS usd_with_pay,
          (SELECT COUNT(*) FROM v_salary_clean) AS kept_after_cleaning
        FROM linkedin_postings p""",

    "top_skill_categories": """
        SELECT skill_name, COUNT(DISTINCT job_id) AS postings,
               ROUND(100 * COUNT(DISTINCT job_id) / (SELECT COUNT(*) FROM linkedin_postings), 1) AS pct_of_postings
        FROM v_posting_skills GROUP BY skill_name ORDER BY postings DESC""",

    "top_industries": """
        SELECT industry_name, COUNT(DISTINCT job_id) AS postings
        FROM v_posting_industries GROUP BY industry_name ORDER BY postings DESC LIMIT 15""",

    "work_type_mix": """
        SELECT formatted_work_type AS work_type, COUNT(*) AS postings
        FROM linkedin_postings GROUP BY formatted_work_type ORDER BY postings DESC""",

    "experience_mix": """
        SELECT formatted_experience_level AS experience_level, COUNT(*) AS postings
        FROM linkedin_postings GROUP BY formatted_experience_level ORDER BY postings DESC""",

    "median_pay_by_experience": median_by(
        "c.formatted_experience_level", "v_salary_clean c"),

    "median_pay_by_work_type": median_by(
        "c.formatted_work_type", "v_salary_clean c"),

    "median_pay_by_skill_category": median_by(
        "ps.skill_name",
        "v_salary_clean c JOIN v_posting_skills ps ON ps.job_id = c.job_id", min_n=200),

    "remote_share_by_skill": """
        SELECT ps.skill_name, COUNT(*) AS postings,
               ROUND(100 * SUM(p.remote_allowed = 1) / COUNT(*), 1) AS pct_remote_allowed
        FROM linkedin_postings p JOIN v_posting_skills ps ON ps.job_id = p.job_id
        GROUP BY ps.skill_name HAVING postings >= 500
        ORDER BY pct_remote_allowed DESC""",

    "applies_by_experience": """
        SELECT formatted_experience_level AS experience_level,
               COUNT(*) AS postings_with_count, ROUND(AVG(applies), 1) AS avg_applies
        FROM linkedin_postings WHERE applies IS NOT NULL
        GROUP BY formatted_experience_level ORDER BY avg_applies DESC""",

    "skill_pairs": """
        SELECT a.skill_name AS skill_a, b.skill_name AS skill_b, COUNT(*) AS postings_together
        FROM v_posting_skills a
        JOIN v_posting_skills b ON a.job_id = b.job_id AND a.skill_abr < b.skill_abr
        GROUP BY a.skill_name, b.skill_name
        ORDER BY postings_together DESC LIMIT 15""",
}

with engine.connect() as conn:
    for name, sql in QUERIES.items():
        df = pd.read_sql(text(sql), conn)
        df = df.rename(columns={"label": "category"}) if "label" in df.columns else df
        df = df.fillna("Not specified")
        df.to_csv(OUT / f"{name}.csv", index=False)
        print(f"{name}.csv: {len(df)} rows")

print("Done. Files are in data/summaries/")