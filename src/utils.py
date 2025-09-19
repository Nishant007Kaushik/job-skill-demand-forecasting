from __future__ import annotations
import pandas as pd

def month_floor(dt: pd.Series) -> pd.Series:
    return pd.to_datetime(dt).dt.to_period('M').dt.to_timestamp()

def top_n(series: pd.Series, n: int = 20) -> list[str]:
    return series.value_counts().head(n).index.tolist()