## NVDA Capital Markets and Forecasting Project – Research Plan

### 1. Project overview

- **Main goal**: Use a single NVDA stock dataset (≈5 years of daily data from Yahoo Finance via `yfinance`) to support **two related projects**:
  - **Project A – Capital markets / time series project**: Focus on understanding the behavior of NVDA’s price process over time (data description, descriptive statistics, time series properties).
  - **Project B – Prediction project**: Build and evaluate models that **forecast NVDA prices** (or returns) using the same dataset plus potentially additional explanatory variables.
- **Key efficiency idea**: Use **one well-prepared dataset** and structure both reports into **four sections** so that ~80% of the data work and analysis overlaps.

### 2. Data description (Section 1)

- **Asset**: NVIDIA Corporation (NVDA) common stock.
- **Data source**: Yahoo Finance via the `yfinance` Python library.
- **Intended date range**:
  - Start: `2021-01-01`
  - End: `2026-03-05`
  - This covers a bit more than 5 calendar years, ensuring **≥ 365 observations** even if you later restrict to business days or a shorter analytical window.
- **Variables (columns) expected from `yf.download(\"NVDA\", start=\"2021-01-01\", end=\"2026-03-05\", auto_adjust=True)`**:
  - **`Open`**: Opening price for each trading day.
  - **`High`**: Highest traded price in the day.
  - **`Low`**: Lowest traded price in the day.
  - **`Close`**: Adjusted closing price (corporate actions reflected because of `auto_adjust=True`).
  - **`Volume`**: Number of shares traded in the day.
  - (Sometimes `Adj Close` is produced separately when not using `auto_adjust`; here, auto-adjustment is applied to `Open`, `High`, `Low`, and `Close`.)
- **Sampling frequency**: Daily observations on trading days (no weekends/holidays).
- **Planned transformations**:
  - Construct **log returns** and/or **simple returns** from the adjusted `Close`:
    - \( r_t = \ln(P_t) - \ln(P_{t-1}) \) or \( r_t = \frac{P_t - P_{t-1}}{P_{t-1}} \).
  - Optionally compute:
    - Rolling volatility (e.g., 20-day, 60-day).
    - Rolling averages (moving averages) of prices or returns.
    - Volume-based indicators (e.g., average volume, volume spikes).

### 3. Descriptive statistics (Section 2)

For both projects, you can share the same descriptive-statistics section, then add **project-specific commentary**:

- **Basic descriptive statistics**:
  - For **prices** (e.g., `Close`):
    - Mean, median, min, max, standard deviation.
    - Selected quantiles (e.g., 5%, 25%, 75%, 95%).
  - For **returns**:
    - Mean and median daily return.
    - Standard deviation (volatility) of returns.
    - Skewness and kurtosis to assess tail behavior and asymmetry.
  - For **volume**:
    - Average daily volume.
    - Standard deviation and extreme values to highlight unusually active periods.
- **Tabular summaries**:
  - One summary table for prices.
  - One summary table for returns.
  - One summary table for volume.
- **Visual descriptive analysis**:
  - Time series plots of:
    - Adjusted `Close` price over time.
    - Daily returns over time.
    - Trading volume over time.
  - Histograms and/or density plots of returns.
  - Boxplots of returns to visualize outliers.
- **Interpretation (Capital markets focus)**:
  - Discuss typical price level and volatility over the sample.
  - Note any major trends, crashes, rallies, or regime changes visible in the price or return plots.
  - Highlight periods of unusually high volume and relate them to market events if relevant.

### 4. Time series analysis (Section 3)

This section is especially important for the **capital markets/time series** course but will also **inform the design of the prediction model** in Section 4.

- **Stationarity diagnostics**:
  - Visual inspection:
    - Plot the price series and the returns series.
    - Expect prices to **look non-stationary** (trending), while returns may be closer to stationary.
  - Statistical tests:
    - Apply unit-root tests (e.g., Augmented Dickey–Fuller (ADF)) to:
      - Prices.
      - Returns.
      - Possibly first differences of prices.
  - Conclusion: Decide whether to model **returns** instead of prices for most models.
- **Autocorrelation analysis**:
  - Compute and plot **ACF (autocorrelation function)** and **PACF (partial autocorrelation function)**:
    - For returns.
    - For squared returns or absolute returns (to detect volatility clustering).
  - Use ACF/PACF patterns to:
    - Identify potential ARMA/ARIMA orders.
    - Detect serial correlation in returns and in volatility.
- **Volatility and risk properties**:
  - Look for signs of **volatility clustering** (periods of high and low volatility).
  - Consider models like **GARCH** conceptually (even if not implemented) as a possible extension.
- **Seasonality or calendar effects (optional)**:
  - Check for day-of-week effects in returns.
  - Consider effects around earnings announcements or macro events (narrative only if not modeled).

### 5. Prediction models (Section 4)

Section 4 for both projects should **explicitly build on Section 3’s time series findings**:

- **Modeling target**:
  - Prefer modelling **returns** rather than raw prices if prices are non-stationary.
  - Optionally convert return forecasts back into **price-level forecasts** for interpretation.
- **Baseline models**:
  - **Naïve benchmark**: random walk / “no-change” model (e.g., tomorrow’s price = today’s price, or tomorrow’s return = 0).
  - **Simple average model**: predict future returns as the historical mean return.
- **Time series models (statistical)**:
  - **AR/ARIMA models for returns**:
    - Use ACF/PACF and information criteria (AIC/BIC) from Section 3 to pick orders.
    - Emphasize that model specification follows from stationarity and autocorrelation analysis.
  - (Optional extension) **GARCH-type models** for conditional volatility if required by the course.
- **Machine learning models (for prediction project)**:
  - Supervised learning using lagged features and possibly other factors:
    - Features:
      - Lagged returns and/or prices (e.g., \( r_{t-1}, r_{t-2}, \dots \)).
      - Rolling statistics (moving averages, rolling volatility).
      - Volume-based features.
    - Candidate models:
      - Linear regression (with time-series features).
      - Regularized linear models (Ridge/Lasso).
      - Tree-based models (Random Forest, Gradient Boosting) if allowed and appropriate.
  - Emphasize that any ML model must respect **time ordering** (no shuffling across time that leaks future information into the past).
- **Evaluation strategy**:
  - Use **time-based train-test split** (e.g., first 4 years for training, last 1 year for testing).
  - Optionally use **rolling/expanding window backtesting**.
  - Metrics:
    - For prices: RMSE, MAE, MAPE.
    - For returns: RMSE, MAE; possibly directional accuracy (hit rate of predicting sign).
- **Connection back to Section 3**:
  - Explicitly explain how:
    - Stationarity tests guided the choice of modelling returns vs prices.
    - ACF/PACF guided AR/ARIMA lag choices.
    - Evidence of volatility clustering motivates using volatility models or transforming features.

### 6. Overlap between the two projects

- **Shared components (≈80% overlap)**:
  - Data download and cleaning.
  - Construction of derived variables (returns, rolling measures).
  - Descriptive statistics and plots.
  - Time series diagnostics (stationarity tests, ACF/PACF).
- **Differences for each project**:
  - **Capital markets/time series project**:
    - Emphasis on **theoretical interpretation** of time series properties.
    - Discussion of market efficiency, random walk hypothesis, volatility behavior, and risk.
  - **Prediction project**:
    - Emphasis on **forecast performance**, model comparison, and practical predictability.
    - Possible extension to include additional explanatory variables (if available).

### 7. Tools and libraries (conceptual, not yet implemented)

- **Planned Python stack** (already reflected in `requirements.txt`, not yet implemented in code):
  - `numpy`, `pandas` for data structures and numerical work.
  - `matplotlib`, `seaborn` for visualization.
  - `statsmodels` for time series models and diagnostic tests (ADF, ACF/PACF, ARIMA).
  - `scikit-learn` for general predictive modeling and model evaluation.
  - `yfinance` for downloading NVDA price data.
  - `jupyter` for exploratory notebooks if desired.

### 8. Next steps (without implementation yet)

- **Data layer**:
  - Use `yfinance` to download NVDA data for the desired date range with `auto_adjust=True`.
  - Save the raw dataset to a CSV file (e.g., `data/nvda_raw.csv`) for reproducibility.
- **Analysis layer**:
  - Implement the descriptive statistics, plots, and time series diagnostics using the planned stack.
- **Modeling layer**:
  - Implement baseline and more advanced models.
  - Carry out train-test splits and evaluate predictive performance.
- **Reporting**:
  - Use this `research.md` as the **narrative backbone** for both course reports, customizing emphasis and interpretation for each subject.

