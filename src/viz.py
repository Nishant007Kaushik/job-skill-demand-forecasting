from __future__ import annotations
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

def line_trend(ts: pd.DataFrame, title: str = "Skill Demand Over Time"):
    fig = px.line(ts, x='Month', y='count', color='Skill', markers=True, title=title)
    if 'rolling_mean' in ts.columns and ts['rolling_mean'].notna().any():
        fig.add_trace(go.Scatter(x=ts['Month'], y=ts['rolling_mean'], mode='lines', name='Rolling Mean'))
    fig.update_layout(hovermode='x unified')
    return fig

def heatmap_by_location(df: pd.DataFrame, skill: str):
    d = df[df['Skill'].str.lower() == skill.lower()].copy()
    p = d.groupby(['Location','Month']).size().reset_index(name='count')
    pivot = p.pivot(index='Location', columns='Month', values='count').fillna(0)
    fig = px.imshow(pivot, aspect='auto', title=f"Heatmap: {skill} Demand by Location")
    return fig

def salary_box(df: pd.DataFrame, skill: str):
    d = df[df['Skill'].str.lower() == skill.lower()].copy()
    fig = px.box(d, x='Location', y='Salary_Mid', title=f"Salary by Location - {skill}")
    return fig

def experience_hist(df: pd.DataFrame, skill: str):
    d = df[df['Skill'].str.lower() == skill.lower()].copy()
    fig = px.histogram(d, x='Experience_Years', nbins=12, title=f"Experience Required Histogram - {skill}")
    return fig

def forecast_plot(forecast: pd.DataFrame, title: str):
    fig = px.line(forecast, x='ds', y=['yhat','yhat_lower','yhat_upper'], title=title)
    return fig