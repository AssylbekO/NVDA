from data_loader import download_nvda_data, load_nvda_data
from preprocessing import add_return_columns, preprocess_prices
from analysis import print_data_overview, print_descriptive_statistics

# %%
def main() -> None:
    # Step 1: download (or refresh) the NVDA dataset and save it as CSV.
    download_nvda_data()

    # Step 2: load the saved dataset from disk.
    df = load_nvda_data()

    # Step 3: basic preprocessing of price data.
    df = preprocess_prices(df)

    # Step 4: data description and descriptive statistics for price/volume.
    print_data_overview(df)
    print_descriptive_statistics(
        df,
        columns=["Open", "High", "Low", "Close", "Volume"],
        title="Price and volume descriptive statistics",
    )

    # Step 5: transform stock prices into stock returns (simple and log).
    df = add_return_columns(df, price_column="Close")
    print_descriptive_statistics(
        df,
        columns=["Return_simple", "Return_log"],
        title="Return descriptive statistics",
    )
    # %%

# %%
if __name__ == "__main__":
    main()
