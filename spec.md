## NVDA Time Series and Prediction Project – Technical Specification

### 1. Objectives and scope

- **Project A – Capital markets / time series project**
  - Analyze the historical behavior of NVDA stock prices and returns.
  - Focus on:
    - Data description and summary statistics.
    - Time series properties (stationarity, autocorrelation, volatility).
    - Interpretation in a capital markets context (efficiency, risk, volatility).
- **Project B – Prediction project**
  - Build and evaluate models that forecast NVDA prices or returns.
  - Focus on:
    - Model design informed by time series diagnostics.
    - Out-of-sample prediction performance.
    - Comparison of simple benchmarks vs more advanced models.
- **Shared design principle**
  - Use a **single cleaned NVDA dataset** and a **4-section report structure** so most of the work is shared:
    1. Data description.
    2. Descriptive statistics.
    3. Time series analysis.
    4. Prediction models and evaluation.

### 2. Data pipeline specification

#### 2.1 Data source

- **Provider**: Yahoo Finance, accessed via the `yfinance` Python library.
- **Ticker**: `NVDA`.
- **Date range**:
  - Start: `2021-01-01`.
  - End: `2026-03-05`.
- **Frequency**: Daily prices on trading days.
- **Download call (to be implemented later)**:
  - Conceptually: `yf.download("NVDA", start="2021-01-01", end="2026-03-05", auto_adjust=True)`
  - `auto_adjust=True` ensures prices are adjusted for splits/dividends at the download stage.

#### 2.2 Raw data schema

- Expected columns:
  - `Open`, `High`, `Low`, `Close`, `Volume`.
- Index:
  - Datetime index of trading days.
- Storage:
  - Planned location (to create later): `data/nvda_raw.csv`.

#### 2.3 Cleaning and transformation steps

- **Data integrity checks**:
  - Verify there are no duplicate dates.
  - Check for missing values in price/volume columns.
  - Confirm chronological ordering of observations.
- **Handling missing data**:
  - If isolated missing values exist:
    - Consider forward-filling prices or dropping affected days (to be justified in the report).
  - For volume, decide whether missing values indicate non-trading days or data issues.
- **Derived variables**:
  - **Log returns**:
    - \( r_t = \ln(P_t) - \ln(P_{t-1}) \) using adjusted `Close`.
  - **Simple returns**:
    - \( r_t = \frac{P_t - P_{t-1}}{P_{t-1}} \).
  - **Rolling statistics**:
    - Moving averages of price or returns (e.g. 20-day, 60-day).
    - Rolling standard deviation (volatility).
  - **Volume-related features**:
    - Rolling average volume.
    - Volume z-scores or indicators of unusually high activity.

### 3. Analysis modules

#### 3.1 Descriptive statistics module

- **Inputs**: Cleaned price and returns DataFrame.
- **Outputs**:
  - Summary tables for:
    - Prices.
    - Returns.
    - Volume.
  - Visualizations:
    - Time series plots of prices, returns, and volume.
    - Histograms and density plots of returns.
    - Boxplots to examine outliers in returns.
- **Key functions (conceptual)**:
  - `compute_summary_statistics(df) -> tables`.
  - `plot_price_and_volume(df) -> figures`.
  - `plot_return_distributions(df) -> figures`.

#### 3.2 Time series diagnostics module

- **Objectives**:
  - Assess stationarity.
  - Characterize autocorrelation in returns and volatility.
  - Guide model selection in the prediction stage.
- **Methods**:
  - **Stationarity tests**:
    - Augmented Dickey–Fuller (ADF) tests on:
      - Price series.
      - Return series.
      - Possibly differenced prices.
  - **Autocorrelation analysis**:
    - ACF and PACF plots for:
      - Returns.
      - Squared or absolute returns.
- **Outputs**:
  - Test statistics and p-values.
  - ACF/PACF plots.
  - Written interpretation:
    - Whether prices are non-stationary.
    - Whether returns are approximately stationary.
    - Presence of serial correlation in returns and/or volatility clustering.

#### 3.3 Modeling and prediction module

- **Targets**:
  - Primary: Daily returns (log or simple).
  - Secondary: Price forecasts derived from return forecasts (if needed for interpretation).
- **Baseline models**:
  - Naïve “no-change” model.
  - Historical mean return model.
- **Time series models**:
  - AR/ARIMA-type models on returns:
    - Orders chosen based on ACF/PACF and information criteria (AIC/BIC) from diagnostics.
- **Machine learning models (for prediction project)**:
  - Feature set:
    - Lagged returns.
    - Rolling statistics (moving averages, rolling volatility).
    - Volume-based features.
  - Candidate algorithms:
    - Linear regression / Ridge / Lasso.
    - Possibly tree-based models if appropriate for the course.
- **Evaluation design**:
  - Time-based split:
    - Training: early sub-period (e.g., first 4 years).
    - Testing: later sub-period (e.g., final year).
  - Metrics:
    - RMSE, MAE on predicted vs actual prices or returns.
    - Directional accuracy (sign prediction).
  - Possible extension:
    - Rolling-window evaluation for more realistic backtesting.

### 4. Software architecture and directory layout

- **Planned structure** (some parts already created, others to be added later):
  - `src/`
    - `main.py` – entry point script (currently empty, to remain so until implementation).
    - (Planned) `data_loader.py` – functions to download and load NVDA data.
    - (Planned) `analysis.py` – descriptive statistics and plotting utilities.
    - (Planned) `ts_models.py` – time series models and diagnostics.
    - (Planned) `ml_models.py` – prediction models using scikit-learn.
  - `data/`
    - (Planned) `nvda_raw.csv` – raw downloaded data.
    - (Planned) `nvda_processed.csv` – cleaned and enriched dataset.
  - `notebooks/` (optional)
    - Exploratory Jupyter notebooks for interactive analysis.
  - `research.md` – high-level research narrative (already drafted).
  - `spec.md` – this technical specification.
  - `agents.md` – design for agent/automation assistance (to be drafted).

### 5. Dependencies and environment

- **Core libraries** (already listed in `requirements.txt`, not yet used in code):
  - `numpy`
  - `pandas`
  - `matplotlib`
  - `seaborn`
  - `statsmodels`
  - `scikit-learn`
  - `yfinance`
  - `jupyter`
- **Environment setup (conceptual)**:
  - Create and activate a virtual environment.
  - Install dependencies from `requirements.txt`.
  - Use the environment consistently in scripts and notebooks.

### 6. Git and reproducibility

- **Current status (from `git status`)**:
  - A Git repository is **already initialized** with branch `main` tracking `origin/main`.
  - New files `.gitignore`, `requirements.txt`, and `src/` are currently **untracked**.
- **Planned Git workflow**:
  - Stage and commit:
    - The updated `.gitignore`.
    - `requirements.txt`.
    - The `src/` directory and future analysis/modeling files.
  - Use meaningful commit messages linked to milestones:
    - “Add data download and cleaning pipeline.”
    - “Implement descriptive statistics and plots.”
    - “Add ARIMA modeling and evaluation.”
    - “Add ML prediction models and backtests.”
- **Reproducibility plan**:
  - Store:
    - Exact data download parameters (ticker, date range, `auto_adjust` flag).
    - Scripts for data preparation and modeling.
  - Optionally fix random seeds in models where relevant.

### 7. Mapping to your drafted approach

- **Your 4-section structure is solid**:
  - Section 1 – Data description.
  - Section 2 – Descriptive statistics.
  - Section 3 – Time series analysis.
  - Section 4 – Prediction model.
- **Key refinement**:
  - This specification makes explicit that **Section 4 must be grounded in Section 3**:
    - Use stationarity and autocorrelation findings to choose:
      - Whether to model prices or returns.
      - ARIMA order ranges.
      - Whether to consider volatility models or additional transformations.
- **Efficiency alignment**:
  - One NVDA dataset, one core analysis, two outputs:
    - A capital-markets-focused write-up.
    - A prediction-focused write-up.

### 8. Implementation phases (high-level TODOs)

- **Phase 1 – Data acquisition and structure**
  - Implement the `yfinance` download logic (NVDA, 2021–2026, `auto_adjust=True`).
  - Save and verify the raw dataset.
- **Phase 2 – Cleaning and feature engineering**
  - Implement transformations and quality checks described in the data pipeline.
- **Phase 3 – Descriptive and time series analysis**
  - Implement summary tables and visualizations.
  - Implement ADF tests, ACF/PACF, and interpret results.
- **Phase 4 – Modeling and evaluation**
  - Implement baseline and ARIMA models.
  - Implement ML models if appropriate.
  - Run evaluations with time-based splits.
- **Phase 5 – Reporting**
  - Finalize course-specific reports using `research.md` as a backbone and this `spec.md` as the technical reference.

