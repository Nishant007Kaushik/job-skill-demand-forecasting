from __future__ import annotations
import pandas as pd
import numpy as np
from .utils import month_floor

def preprocess(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()
    df.columns = [c.strip().replace(' ', '_') for c in df.columns]
    df['Date'] = pd.to_datetime(df['Date'])
    df['Month'] = month_floor(df['Date'])
    if 'Salary_Min' in df.columns and 'Salary_Max' in df.columns:
        df['Salary_Min'] = pd.to_numeric(df['Salary_Min'], errors='coerce')
        df['Salary_Max'] = pd.to_numeric(df['Salary_Max'], errors='coerce')
        swap_idx = df['Salary_Min'] > df['Salary_Max']
        df.loc[swap_idx, ['Salary_Min','Salary_Max']] = df.loc[swap_idx, ['Salary_Max','Salary_Min']].values
        df['Salary_Mid'] = (df['Salary_Min'] + df['Salary_Max']) / 2.0
    for col in ['Skill','Job_Title','Company','Location','Industry','Work_Type','Education_Level']:
        if col in df.columns:
            df[col] = df[col].astype(str).str.strip()
    if 'Experience_Required' in df.columns:
        df['Experience_Years'] = (
            df['Experience_Required'].astype(str).str.extract(r'(\d+)').astype(float)
        )
    return df