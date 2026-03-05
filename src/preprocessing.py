from __future__ import annotations

from typing import Iterable, Optional

import numpy as np
import pandas as pd


def preprocess_prices(df: pd.DataFrame) -> pd.DataFrame:
    """
    Basic preprocessing for NVDA price data:
    - Ensure the index is sorted.
    - Drop duplicate index entries, keeping the first.
    - Optionally drop rows with all-NaN price fields.
    """
    df = df.copy()

    df = df.sort_index()
    df = df[~df.index.duplicated(keep="first")]

    price_cols = [col for col in ["Open", "High", "Low", "Close"] if col in df.columns]
    if price_cols:
        df = df.dropna(axis=0, how="all", subset=price_cols)

    return df


def add_return_columns(
    df: pd.DataFrame,
    price_column: str = "Close",
    simple_return_name: str = "Return_simple",
    log_return_name: str = "Return_log",
) -> pd.DataFrame:
    """
    Add simple and log return columns based on a given price column.
    """
    df = df.copy()

    if price_column not in df.columns:
        raise KeyError(f"{price_column!r} column not found in DataFrame.")

    price_series = pd.to_numeric(df[price_column], errors="coerce")

    df[simple_return_name] = price_series.pct_change()
    df[log_return_name] = np.log(price_series).diff()

    return df

