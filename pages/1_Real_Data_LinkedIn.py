from pathlib import Path

import pandas as pd
import plotly.express as px
import streamlit as st

st.set_page_config(page_title="Real Data: LinkedIn Postings", page_icon="📊", layout="wide")

SUMMARIES = Path(__file__).resolve().parent.parent / "data" / "summaries"
EXP_ORDER = ["Internship", "Entry level", "Associate", "Mid-Senior level",
             "Director", "Executive", "Not specified"]


@st.cache_data
def load(name):
    return pd.read_csv(SUMMARIES / f"{name}.csv")


def hbar(df, x, y, title, top=None):
    d = df.head(top) if top else df
    fig = px.bar(d.sort_values(x), x=x, y=y, orientation="h", title=title)
    st.plotly_chart(fig, width="stretch")


st.title("Real Data: LinkedIn Job Postings")
snap = load("snapshot_info").iloc[0]
cov = load("coverage_and_cleaning").iloc[0]

c1, c2, c3 = st.columns(3)
c1.metric("Postings", f"{int(snap['total_postings']):,}")
c2.metric("With a skill tag", f"{cov['with_skill_tag'] / cov['total_postings']:.1%}")
c3.metric("Salaries kept after cleaning", f"{int(cov['kept_after_cleaning']):,}")
st.caption(
    f"Snapshot of postings listed {str(snap['first_listed'])[:10]} to {str(snap['last_listed'])[:10]}. "
    f"Postings are US-focused and pay is in USD; only {cov['usd_with_pay'] / cov['total_postings']:.0%} "
    "of postings list pay. Skill categories are LinkedIn's broad job functions (for example Sales or "
    "Information Technology), not tools like Python."
)

left, right = st.columns(2)
with left:
    st.subheader("Most common skill categories")
    hbar(load("top_skill_categories"), "postings", "skill_name", "Postings by skill category", top=15)
with right:
    st.subheader("Most common industries")
    hbar(load("top_industries"), "postings", "industry_name", "Postings by industry")

st.subheader("Median annual pay (USD, cleaned)")
a, b = st.columns(2)
with a:
    pay_exp = load("median_pay_by_experience")
    fig = px.bar(pay_exp, x="category", y="median_pay_usd", hover_data=["n"],
                 title="By experience level",
                 labels={"category": "", "median_pay_usd": "Median pay (USD)"})
    fig.update_xaxes(categoryorder="array", categoryarray=EXP_ORDER)
    st.plotly_chart(fig, width="stretch")
with b:
    pay_wt = load("median_pay_by_work_type")
    pay_wt = pay_wt[pay_wt["n"] >= 30]
    fig = px.bar(pay_wt, x="category", y="median_pay_usd", hover_data=["n"],
                 title="By work type",
                 labels={"category": "", "median_pay_usd": "Median pay (USD)"})
    st.plotly_chart(fig, width="stretch")
st.caption(
    "Work types with fewer than 30 salaries are hidden. Contract pay may be affected by how hourly "
    "rates are annualised."
)

hbar(load("median_pay_by_skill_category"), "median_pay_usd", "category",
     "Median annual pay by skill category (categories overlap)", top=15)

c, d = st.columns(2)
with c:
    st.subheader("Explicitly remote-allowed share")
    hbar(load("remote_share_by_skill"), "pct_remote_allowed", "skill_name",
         "% of postings flagged remote-allowed", top=15)
with d:
    st.subheader("Applications per posting")
    ap = load("applies_by_experience")
    fig = px.bar(ap, x="experience_level", y="avg_applies", hover_data=["postings_with_count"],
                 title="Average applications by experience level",
                 labels={"experience_level": "", "avg_applies": "Average applications"})
    fig.update_xaxes(categoryorder="array", categoryarray=EXP_ORDER)
    st.plotly_chart(fig, width="stretch")
st.caption("A blank remote flag means unknown, not on-site. Application counts exist for only some postings.")

st.subheader("Skill categories that appear together")
st.dataframe(load("skill_pairs"), width="stretch", hide_index=True)
st.caption(
    "Management + Manufacturing is the largest pair but probably reflects how postings are tagged, "
    "so treat it with caution."
)