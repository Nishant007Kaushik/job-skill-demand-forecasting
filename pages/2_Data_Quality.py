from pathlib import Path

import pandas as pd
import plotly.express as px
import streamlit as st

st.set_page_config(page_title="Data Quality", page_icon="🔍", layout="wide")

ROOT = Path(__file__).resolve().parent.parent
SYNTH = ROOT / "data" / "synthetic_job_postings_2023_2025.csv"
SUMMARIES = ROOT / "data" / "summaries"


@st.cache_data
def load_synthetic():
    df = pd.read_csv(SYNTH)
    df.columns = [c.lower() for c in df.columns]
    df["date"] = pd.to_datetime(df["date"])
    df["salary_mid"] = (df["salary_min"] + df["salary_max"]) / 2
    df["exp_years"] = df["experience_required"].str.extract(r"(\d+)", expand=False).astype(float)
    return df


df = load_synthetic()
st.title("Data Quality: what I found in each dataset")

st.header("1. Synthetic dataset (IIT submission and forecast)")
m1, m2, m3, m4 = st.columns(4)
m1.metric("Rows", f"{len(df):,}")
m2.metric("Missing values", int(df.isna().sum().sum()))
m3.metric("Duplicate rows", int(df.duplicated().sum()))
m4.metric("Salary min > max", int((df["salary_min"] > df["salary_max"]).sum()))
st.write("Structurally the data is clean. The problem is that its columns look independent of each other.")

st.subheader("Skills are close to evenly demanded")
counts = df["skill"].value_counts()
st.write(
    f"Postings per skill range from {counts.min():,} to {counts.max():,} across {len(counts)} skills. "
    f"The most common skill has only {counts.max() / counts.min():.2f}x the postings of the least common, "
    "which is what random assignment looks like."
)

st.subheader("Pay does not rise with experience")
by_exp = df.groupby("exp_years")["salary_mid"].mean().reset_index()
fig = px.line(by_exp, x="exp_years", y="salary_mid", markers=True,
              title="Average mid salary by years of experience (synthetic)",
              labels={"exp_years": "Years of experience", "salary_mid": "Average mid salary"})
fig.update_yaxes(rangemode="tozero")
st.plotly_chart(fig, width="stretch")
st.caption("In the real LinkedIn data, median pay rises clearly with seniority.")

st.subheader("Skills and job titles are paired at random")
pairs = df.groupby(["skill", "job_title"]).size()
st.write(
    f"There are {len(pairs)} skill and title pairs, averaging {pairs.mean():.0f} postings each "
    f"with a maximum of {pairs.max()}. Several of the most frequent pairs are unrealistic combinations:"
)
st.dataframe(pairs.sort_values(ascending=False).head(5).reset_index(name="postings"),
             width="stretch", hide_index=True)

st.subheader("The trending flag does nothing")
flag = df.groupby("trending_skill_flag")["application_count"].agg(["count", "mean"]).reset_index()
flag.columns = ["trending_skill_flag", "postings", "avg_applications"]
st.dataframe(flag.round(1), width="stretch", hide_index=True)

st.subheader("Monthly postings have no trend")
monthly = df.groupby(df["date"].dt.to_period("M").astype(str)).size().reset_index(name="postings")
monthly.columns = ["month", "postings"]
fig = px.line(monthly, x="month", y="postings", title="Postings per month (synthetic)")
fig.update_yaxes(rangemode="tozero")
st.plotly_chart(fig, width="stretch")

st.info(
    "Takeaway: the synthetic data is good for demonstrating the pipeline and the forecasting method, "
    "but its patterns are not market findings. That is why the project also analyses real postings."
)

st.header("2. Real dataset (LinkedIn postings, Mar-Apr 2024)")
cov = pd.read_csv(SUMMARIES / "coverage_and_cleaning.csv").iloc[0]
st.write(
    f"Of {int(cov['total_postings']):,} postings, {int(cov['usd_with_pay']):,} list a USD salary and "
    f"{int(cov['kept_after_cleaning']):,} remain after cleaning. The rules, all judgment calls, were:"
)
st.markdown(
    "- Use USD salaries only. Nearly all salaries were USD.\n"
    "- Postings labelled HOURLY with a maximum of $1,000 or more were treated as annual figures "
    "(30 of the 38 salaries above $1M were labelled hourly).\n"
    "- Keep annual pay between $15,000 and $1,000,000.\n"
    "- Skill and industry tags whose job ID is not in the postings file "
    "(4,711 and 4,712 IDs) were excluded through views.\n"
    "- Blank values are reported as 'Not specified', and a blank remote flag is not treated as on-site."
)
st.caption(
    "Limitations: a four-week snapshot, US-focused, pay available for under a third of postings, "
    "and the pay cut-offs have not been validated against a source of truth."
)