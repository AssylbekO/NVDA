from pathlib import Path

import pandas as pd
import yfinance as yf


DATA_DIR = Path(__file__).resolve().parent.parent / "data"
RAW_FILENAME = "nvda_raw.csv"


def download_nvda_data(
    ticker: str = "NVDA",
    start: str = "2021-01-01",
    end: str = "2026-03-05",
    auto_adjust: bool = True,
    filename: str = RAW_FILENAME,
) -> pd.DataFrame:
    """
    Download NVDA daily data for the specified period and save it as a CSV file.
    """
    DATA_DIR.mkdir(parents=True, exist_ok=True)

    df = yf.download(ticker, start=start, end=end, auto_adjust=auto_adjust)
    output_path = DATA_DIR / filename
    df.to_csv(output_path)

    print(f"Downloaded {len(df)} rows for {ticker} and saved to {output_path}")

    if len(df) < 365:
        print(
            "Warning: fewer than 365 observations were downloaded. "
            "Check the date range or data source."
        )

    return df


def load_nvda_data(filename: str = RAW_FILENAME) -> pd.DataFrame:
    """
    Load NVDA data from the CSV file created by download_nvda_data.
    """
    csv_path = DATA_DIR / filename
    if not csv_path.exists():
        raise FileNotFoundError(
            f"{csv_path} not found. Run the download step first to create the dataset."
        )

    # Handle the CSV structure produced by yfinance, which may include
    # extra header-like rows such as 'Ticker' and 'Date' in the first column.
    df = pd.read_csv(csv_path)

    if "Price" in df.columns:
        # Drop non-data rows where the first column is a label.
        df = df[~df["Price"].isin(["Ticker", "Date"])]

        # Interpret the first column as the date index.
        df = df.rename(columns={"Price": "Date"})
        df["Date"] = pd.to_datetime(df["Date"])
        df = df.set_index("Date").sort_index()

    # Coerce remaining columns to numeric where possible.
    for col in df.columns:
        df[col] = pd.to_numeric(df[col], errors="coerce")

    return df


