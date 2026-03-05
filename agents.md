## Agents and Automation Plan for the NVDA Project

### 1. Goals for agent assistance

- **Reduce manual work** in repetitive tasks:
  - Data downloading and re-downloading with the same parameters.
  - Regenerating descriptive statistics and plots after small changes.
  - Running standard time series diagnostics and model evaluations.
- **Improve consistency and reproducibility**:
  - Use scripted, agent-assisted workflows so the same analysis can be rerun on demand.
- **Support documentation**:
  - Help draft and refine `research.md`, `spec.md`, and course deliverables using a consistent structure.

### 2. Roles for this AI assistant

- **Design and planning assistant**:
  - Help design the project structure (`src/`, `data/`, docs).
  - Propose analysis pipelines and model choices consistent with time series theory and course requirements.
- **Coding assistant (when you choose to implement)**:
  - Generate boilerplate code for:
    - Data download (`yfinance` calls for NVDA).
    - Data cleaning and feature engineering.
    - Descriptive statistics and plotting.
    - Time series diagnostics and models (e.g., ARIMA).
    - Machine learning models for prediction using scikit-learn.
  - Refactor and document code where needed, following your style.
- **Review and debugging assistant**:
  - Inspect error messages and stack traces.
  - Suggest fixes for common library and modeling issues.
  - Review modeling results and discuss possible improvements.
- **Reporting assistant**:
  - Help structure and refine written reports for both courses.
  - Ensure that the narrative in Section 4 explicitly uses findings from Section 3.

### 3. Automation boundaries

- **What the agent will NOT do automatically**:
  - Execute trades or connect to brokerage APIs.
  - Make real-money investment recommendations.
  - Push commits or modify remote repositories without your explicit instruction.
- **What the agent CAN automate with your approval**:
  - Creation and modification of local project files (`src/*.py`, docs).
  - Running local commands (e.g., `git status`) to understand project state.
  - Keeping a structured TODO list of tasks and updating their status as work progresses.

### 4. Planned agent-driven workflows (no implementation yet)

- **Workflow 1 – Data download and refresh**
  - Define a function (e.g., in `src/data_loader.py`) that:
    - Downloads NVDA data using `yfinance` with:
      - Ticker: `"NVDA"`.
      - Start: `"2021-01-01"`.
      - End: `"2026-03-05"`.
      - `auto_adjust=True`.
    - Saves data to `data/nvda_raw.csv`.
  - Use the agent to:
    - Generate and refine this function.
    - Add safe checks and clear logging messages.

- **Workflow 2 – Analysis pipeline runs**
  - Create scripts or notebooks for:
    - Descriptive statistics and plots.
    - Time series diagnostics (ADF tests, ACF/PACF).
    - Model training and evaluation.
  - Use the agent to:
    - Propose modular functions for each step.
    - Add or adjust visualizations and tables.
    - Ensure each step ties back to the project specification in `spec.md`.

- **Workflow 3 – Model iteration**
  - Use the agent to:
    - Suggest alternative model specifications when diagnostics suggest mis-specification (e.g., residual autocorrelation).
    - Compare models with different lags or feature sets.
    - Interpret results in the language required by your courses.

- **Workflow 4 – Documentation and reporting**
  - Use the agent to:
    - Keep `research.md` aligned with what the code actually does.
    - Draft course-specific sections that emphasize the right aspects (theory vs prediction).
    - Help you transform notebooks/outputs into clean figures and tables for submission.

### 5. Current status and next steps for agents

- **Current status**:
  - This `agents.md` file outlines how this AI assistant will be used going forward.
  - No automated scripts or pipelines have been implemented yet; everything is still in the planning and specification phase.
- **Next steps**:
  - When you are ready to implement:
    - Start with the **data download** function for NVDA in `src/`.
    - Then implement the **descriptive statistics** and **time series diagnostics** modules.
    - Use this agent to generate and refine code in small, testable steps, updating TODOs as each milestone is completed.

