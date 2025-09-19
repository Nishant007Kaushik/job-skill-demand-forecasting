# ------------------ Imports ------------------
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime

# Import your own modules from src folder
from src.data_load import load_dataset
from src.preprocess import preprocess
from src.features import (
    skill_counts_monthly, rolling_trend, sector_split,
    city_split, salary_stats, experience_distribution
)
from src.forecast import prepare_time_series, fit_forecast
from src.viz import line_trend, heatmap_by_location, salary_box, experience_hist, forecast_plot
from src.utils import top_n
import plotly.express as px  # used for pie charts

# ------------------ Page Configuration ------------------
# Set the Streamlit page title, icon and layout
st.set_page_config(page_title="Job Skill Demand Forecasting", page_icon="📈", layout="wide")

# Path to your synthetic dataset
DATA_PATH = "D:/job-skill-demand-forecasting/data/synthetic_job_postings_2023_2025.csv"

# ------------------ Data Loading ------------------
@st.cache_data(show_spinner=False)
def get_data():
    """
    Load the dataset from disk and preprocess it once.
    This is cached to avoid reloading every time.
    """
    df = load_dataset(DATA_PATH)
    df = preprocess(df)
    return df

# Load preprocessed data into df
df = get_data()

# ------------------ Sidebar Filters ------------------
st.sidebar.header("Filters")

# Top N skills dropdown
skills = top_n(df['Skill'], n=25)
skill = st.sidebar.selectbox("Select a Skill", skills, index=0)

# Date range filter
min_date, max_date = df['Date'].min(), df['Date'].max()
date_range = st.sidebar.date_input("Date range", (min_date, max_date), min_value=min_date, max_value=max_date)

# Location filter
locations = ["All"] + sorted(df['Location'].dropna().unique().tolist())
loc_choice = st.sidebar.selectbox("Location", locations, index=0)

# Industry filter
industries = ["All"] + sorted(df['Industry'].dropna().unique().tolist())
ind_choice = st.sidebar.selectbox("Industry", industries, index=0)

# Work type filter
work_types = ["All"] + sorted(df['Work_Type'].dropna().unique().tolist())
work_choice = st.sidebar.selectbox("Work Type", work_types, index=0)

# Apply filters to df
mask = (df['Date'].between(pd.to_datetime(date_range[0]), pd.to_datetime(date_range[1])))
if loc_choice != "All":
    mask &= (df['Location'] == loc_choice)
if ind_choice != "All":
    mask &= (df['Industry'] == ind_choice)
if work_choice != "All":
    mask &= (df['Work_Type'] == work_choice)

# Filtered dataframe used in tabs
dff = df.loc[mask].copy()

# ------------------ Dashboard Title ------------------
st.title("📊 Job Skill Demand Forecasting (Synthetic)")
st.caption("India • 2023–2025 • Streamlit + Plotly • Prophet")

# ------------------ Top KPIs ------------------
# Show metrics (Total postings, postings for selected skill, median salary, avg experience)
total_posts = len(dff)
skill_posts = (dff['Skill'].str.lower() == skill.lower()).sum()
pct = (skill_posts / total_posts * 100.0) if total_posts else 0.0
col1, col2, col3, col4 = st.columns(4)
col1.metric("Total Postings (filtered)", f"{total_posts:,}")
col2.metric(f"Postings for {skill}", f"{skill_posts:,}", f"{pct:.1f}%")

# Salary and experience metrics for selected skill
if 'Salary_Mid' in dff.columns and skill_posts > 0:
    sal = dff.loc[dff['Skill'].str.lower()==skill.lower(),'Salary_Mid']
    col3.metric("Median Salary (INR)", f"{int(sal.median()):,}")
    col4.metric("Avg Experience (yrs)",
                f"{dff.loc[dff['Skill'].str.lower()==skill.lower(),'Experience_Years'].mean():.1f}")
else:
    col3.metric("Median Salary (INR)", "—")
    col4.metric("Avg Experience (yrs)", "—")

# ------------------ Tabs ------------------
tab1, tab2, tab3, tab4, tab5 = st.tabs(
    ["Overview", "Trends", "Forecast", "Salary & Experience", "Summary"]
)

# ------------------ Tab 1: Overview ------------------
with tab1:
    # Left: cities; Right: industry split
    c1, c2 = st.columns([2,1])
    city_df = city_split(dff, skill)
    ind_df = sector_split(dff, skill)

    c1.subheader(f"Top Cities for {skill}")
    # Show line chart of monthly demand by city for selected skill
    if not city_df.empty:
        c1.plotly_chart(
            line_trend(
                (dff[dff['Skill'].str.lower()==skill.lower()]
                 .groupby(['Month','Location']).size().reset_index(name='count')
                 .rename(columns={'Location':'Skill'})),
                title=f"{skill} Monthly Demand by City (multi-series)"
            ),
            use_container_width=True
        )

    c2.subheader("Industry Split")
    if not ind_df.empty:
        c2.dataframe(ind_df, use_container_width=True, height=400)

# ------------------ Tab 2: Trends ------------------
with tab2:
    st.subheader(f"Monthly Trend — {skill}")
    # Line chart with rolling mean
    ts = skill_counts_monthly(dff, skill)
    ts = rolling_trend(ts, window=3)
    st.plotly_chart(line_trend(ts, title=f"{skill} — Monthly Demand & 3M Rolling Mean"), use_container_width=True)

    st.subheader("Heatmap by Location")
    st.plotly_chart(heatmap_by_location(dff, skill), use_container_width=True)

# ------------------ Tab 3: Forecast ------------------
with tab3:
    st.subheader(f"Prophet Forecast — {skill}")
    # Prepare time series and forecast next 6 months if enough history
    ts_all = prepare_time_series(dff, skill)
    if len(ts_all) >= 6:
        model, fc = fit_forecast(ts_all, periods=6)
        st.plotly_chart(
            forecast_plot(fc[['ds','yhat','yhat_lower','yhat_upper']],
                          title=f"{skill} Forecast (next 6 months)"),
            use_container_width=True
        )
        st.dataframe(fc.tail(6)[['ds','yhat','yhat_lower','yhat_upper']].rename(columns={'ds':'Month'}),
                     use_container_width=True)
    else:
        st.info("Not enough history to forecast. Try widening the date range or pick another skill.")

# ------------------ Tab 4: Salary & Experience ------------------
with tab4:
    st.subheader(f"Salary by Location — {skill}")
    st.plotly_chart(salary_box(dff, skill), use_container_width=True)

    st.subheader("Experience Required — Histogram")
    st.plotly_chart(experience_hist(dff, skill), use_container_width=True)

    st.subheader("Salary Stats")
    st.dataframe(salary_stats(dff, skill), use_container_width=True)

    st.subheader("Top Companies (Filtered)")
    top_companies = (dff[dff['Skill'].str.lower()==skill.lower()]
                     .groupby('Company').size().reset_index(name='count')
                     .sort_values('count', ascending=False).head(20))
    st.dataframe(top_companies, use_container_width=True)

# ------------------ Tab 5: Summary (Pie Charts) ------------------
with tab5:
    st.subheader("📊 Final Summary Insights")
    st.write("Columns in current data:", dff.columns.tolist())
    
    # … your pie charts …
    st.subheader("🔥 Top 10 Skills in Current Filter")
    skill_counts = dff['Skill'].value_counts().head(10).reset_index()
    skill_counts.columns = ['Skill', 'Job Postings']
    st.dataframe(skill_counts, use_container_width=True)



    # Pie chart: Top 5 trending jobs
    if 'Job_Title' in dff.columns:
        top_jobs = dff['Job_Title'].value_counts().head(5).reset_index()
        top_jobs.columns = ['Job_Title', 'Count']
        fig1 = px.pie(top_jobs, names='Job_Title', values='Count', title='Top 5 Trending Jobs')
        st.plotly_chart(fig1, use_container_width=True)

    # Pie chart: Top 5 highest paying jobs
    if 'Salary_Mid' in dff.columns and 'Job_Title' in dff.columns:
        top_pay = (dff.groupby('Job_Title')['Salary_Mid']
                   .median().sort_values(ascending=False)
                   .head(5).reset_index())
        top_pay.columns = ['Job_Title', 'Median Salary']
        fig2 = px.pie(top_pay, names='Job_Title', values='Median Salary', title='Top 5 Highest Paying Jobs')
        st.plotly_chart(fig2, use_container_width=True)

    # Pie chart: Top 5 cities by job demand
    if 'Location' in dff.columns:
        top_cities = dff['Location'].value_counts().head(5).reset_index()
        top_cities.columns = ['City', 'Count']
        fig3 = px.pie(top_cities, names='City', values='Count', title='Top 5 Cities by Job Demand')
        st.plotly_chart(fig3, use_container_width=True)

    # Pie chart: Top 5 companies hiring most
    if 'Company' in dff.columns:
        top_companies = dff['Company'].value_counts().head(5).reset_index()
        top_companies.columns = ['Company', 'Count']
        fig4 = px.pie(top_companies, names='Company', values='Count', title='Top 5 Companies Hiring Most')
        st.plotly_chart(fig4, use_container_width=True)

# ------------------ Extra Section: Compare Multiple Skills ------------------
st.subheader("📊 Compare Multiple Skills")

# Multi-select skills for comparison
selected_skills = st.multiselect("Select skills to compare:", df["Skill"].unique())

if selected_skills:
    # Filter and group by month for selected skills
    skill_data = df[df["Skill"].isin(selected_skills)].copy()
    skill_data['month'] = pd.to_datetime(skill_data['Date']).dt.to_period('M')
    skill_trends = skill_data.groupby(['month', 'Skill']).size().reset_index(name='count')

    # Plot multiple lines
    fig, ax = plt.subplots(figsize=(10, 5))
    for skill_ in selected_skills:
        trend = skill_trends[skill_trends["Skill"] == skill_]
        ax.plot(trend["month"].astype(str), trend["count"], marker="o", label=skill_)

    ax.set_title("Job Posting Trends for Selected Skills")
    ax.set_xlabel("Month")
    ax.set_ylabel("Number of Job Postings")
    ax.legend()
    st.pyplot(fig)
