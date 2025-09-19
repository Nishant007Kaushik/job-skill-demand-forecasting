from __future__ import annotations
import pandas as pd
from functools import lru_cache

@lru_cache(maxsize=4)
def load_dataset(path: str) -> pd.DataFrame:
    df = pd.read_csv(path, parse_dates=['Date'])
    return df