from __future__ import annotations

from typing import Iterable, Optional

import matplotlib.pyplot as plt  # pyright: ignore[reportMissingImports]
import pandas as pd
import seaborn as sns  # pyright: ignore[reportMissingModuleSource]


def print_data_overview(df: pd.DataFrame) -> None:
    """
    Print a high-level overview of the dataset: shape, index range, and columns.
    """
    print("=== Data overview ===")
    print(f"Number of rows: {len(df)}")
    print(f"Columns: {list(df.columns)}")

    if not df.empty and isinstance(df.index, pd.DatetimeIndex):
        print(f"Date range: {df.index.min()} -> {df.index.max()}")

    print()


def print_descriptive_statistics(
    df: pd.DataFrame,
    columns: Optional[Iterable[str]] = None,
    title: str = "Descriptive statistics",
) -> None:
    """
    Print basic descriptive statistics for selected columns.
    """
    cols = list(columns) if columns is not None else list(df.columns)
    cols = [col for col in cols if col in df.columns]

    if not cols:
        print(f"{title}: no matching columns found.")
        print()
        return

    print(f"=== {title} ===")
    print(df[cols].describe())
    print()


def check_daily_time_series(df: pd.DataFrame) -> None:
    """
    Print diagnostics about the time index to verify a daily (trading day) series.
    """
    print("=== Time index diagnostics ===")

    if not isinstance(df.index, pd.DatetimeIndex):
        print("Index is not a DatetimeIndex; cannot run daily time-series checks.")
        print()
        return

    idx = df.index.sort_values()
    print(f"First date: {idx.min()}")
    print(f"Last date:  {idx.max()}")

    # Differences between consecutive dates
    diffs = idx.to_series().diff().dropna()
    gap_counts = diffs.value_counts().sort_index()

    print("\nDistinct time gaps between observations:")
    for delta, count in gap_counts.items():
        print(f"  {delta}: {count} times")

    # Compare with business-day calendar to highlight missing business days
    bdays = pd.date_range(idx.min(), idx.max(), freq="B")
    missing_bdays = bdays.difference(idx)

    print(f"\nNumber of observations: {len(idx)}")
    print(f"Number of business days in full range: {len(bdays)}")
    print(f"Missing business days (likely holidays): {len(missing_bdays)}")
    print()


def _extended_stats_for_series(series: pd.Series) -> pd.Series:
    """
    Compute extended descriptive stats for a 1D numeric series.
    """
    s = pd.to_numeric(series, errors="coerce").dropna()
    desc = s.describe()

    q1 = desc["25%"]
    q3 = desc["75%"]
    data_range = desc["max"] - desc["min"]
    iqr = q3 - q1

    variance = s.var(ddof=1)
    skewness = s.skew()
    # pandas' kurtosis is excess kurtosis (0 for normal)
    excess_kurtosis = s.kurt()
    kurtosis = excess_kurtosis + 3.0

    return pd.Series(
        {
            "mean": desc["mean"],
            "variance": variance,
            "std": desc["std"],
            "min": desc["min"],
            "max": desc["max"],
            "range": data_range,
            "Q1": q1,
            "median": desc["50%"],
            "Q3": q3,
            "IQR": iqr,
            "skewness": skewness,
            "kurtosis": kurtosis,
            "excess_kurtosis": excess_kurtosis,
        }
    )


def extended_descriptive_table(
    df: pd.DataFrame,
    columns: Iterable[str],
    title: str = "Extended descriptive statistics",
) -> pd.DataFrame:
    """
    Return and print an extended statistics table for selected columns.
    """
    cols = [col for col in columns if col in df.columns]
    if not cols:
        print(f"{title}: no matching columns found.")
        return pd.DataFrame()

    stats = {col: _extended_stats_for_series(df[col]) for col in cols}
    table = pd.DataFrame(stats)

    print(f"=== {title} ===")
    print(table)
    print()

    return table


def plot_price_series(df: pd.DataFrame, price_column: str = "Close") -> None:
    """
    Plot the price series over time.
    """
    if price_column not in df.columns:
        print(f"Column {price_column!r} not found; cannot plot price series.")
        return

    if not isinstance(df.index, pd.DatetimeIndex):
        print("Index is not DatetimeIndex; plotting against row number instead.")
        x = range(len(df))
    else:
        x = df.index

    plt.figure(figsize=(12, 4))
    plt.plot(x, df[price_column], label=price_column)
    plt.title(f"{price_column} over time")
    plt.xlabel("Date")
    plt.ylabel("Price")
    plt.grid(True, alpha=0.3)
    plt.legend()
    plt.tight_layout()
    plt.show()


def plot_return_series(
    df: pd.DataFrame,
    columns: Iterable[str] = ("Return_simple", "Return_log"),
) -> None:
    """
    Plot one or more return series over time.
    """
    cols = [col for col in columns if col in df.columns]
    if not cols:
        print("No return columns found to plot.")
        return

    if not isinstance(df.index, pd.DatetimeIndex):
        x = range(len(df))
        x_label = "Observation"
    else:
        x = df.index
        x_label = "Date"

    plt.figure(figsize=(12, 4))
    for col in cols:
        plt.plot(x, df[col], label=col, alpha=0.8)

    plt.title("Return series over time")
    plt.xlabel(x_label)
    plt.ylabel("Return")
    plt.axhline(0.0, color="black", linewidth=0.8, linestyle="--", alpha=0.6)
    plt.grid(True, alpha=0.3)
    plt.legend()
    plt.tight_layout()
    plt.show()


def plot_distribution(
    df: pd.DataFrame,
    column: str,
    bins: int = 50,
    title: Optional[str] = None,
) -> None:
    """
    Plot the distribution (histogram + KDE) of a single column.
    """
    if column not in df.columns:
        print(f"Column {column!r} not found; cannot plot distribution.")
        return

    data = pd.to_numeric(df[column], errors="coerce").dropna()

    plt.figure(figsize=(8, 4))
    sns.histplot(data, bins=bins, kde=True)
    plt.xlabel(column)
    plt.ylabel("Frequency")
    plt.title(title or f"Distribution of {column}")
    plt.tight_layout()
    plt.show()

