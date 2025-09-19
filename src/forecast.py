from __future__ import annotations
import pandas as pd
from prophet import Prophet

def prepare_time_series(df: pd.DataFrame, skill: str) -> pd.DataFrame:
    d = df[df['Skill'].str.lower() == skill.lower()].copy()
    m = (d.groupby('Month').size().reset_index(name='y'))
    m = m.rename(columns={'Month':'ds'}).sort_values('ds')
    return m

def fit_forecast(df: pd.DataFrame, periods: int = 6):
    model = Prophet(seasonality_mode='additive', weekly_seasonality=False, daily_seasonality=False)
    model.add_seasonality(name='yearly', period=365.25, fourier_order=5)
    model.fit(df)  # df columns: ds, y
    future = model.make_future_dataframe(periods=periods, freq='MS')
    forecast = model.predict(future)
    return model, forecast