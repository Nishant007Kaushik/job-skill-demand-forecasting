from __future__ import annotations
import pandas as pd
from .utils import month_floor

def skill_counts_monthly(df: pd.DataFrame, skill: str | None = None) -> pd.DataFrame:
    d = df.copy()
    if skill:
        d = d[d['Skill'].str.lower() == str(skill).lower()]
    g = (d.groupby(['Month','Skill']).size()
           .reset_index(name='count')
           .sort_values(['Skill','Month']))
    return g

def rolling_trend(ts: pd.DataFrame, window: int = 3) -> pd.DataFrame:
    ts = ts.sort_values('Month')
    ts['rolling_mean'] = ts['count'].rolling(window=window, min_periods=1).mean()
    return ts

def sector_split(df: pd.DataFrame, skill: str) -> pd.DataFrame:
    d = df[df['Skill'].str.lower() == skill.lower()]
    g = d.groupby(['Industry']).size().reset_index(name='count').sort_values('count', ascending=False)
    return g

def city_split(df: pd.DataFrame, skill: str) -> pd.DataFrame:
    d = df[df['Skill'].str.lower() == skill.lower()]
    g = d.groupby(['Location']).size().reset_index(name='count').sort_values('count', ascending=False)
    return g

def salary_stats(df: pd.DataFrame, skill: str) -> pd.DataFrame:
    d = df[df['Skill'].str.lower() == skill.lower()]
    cols = ['Salary_Min','Salary_Max','Salary_Mid']
    stats = d[cols].describe(percentiles=[0.25,0.5,0.75]).T.reset_index().rename(columns={'index':'metric'})
    return stats

def experience_distribution(df: pd.DataFrame, skill: str) -> pd.DataFrame:
    d = df[df['Skill'].str.lower() == skill.lower()]
    return d[['Experience_Years']].dropna()