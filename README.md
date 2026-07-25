# Retailmart Finance Analytics

An end-to-end data analytics project to extract, profile, clean, analyze, and visualize finance records for **Retailmart**. This project establishes a production-ready python workspace for Exploratory Data Analysis (EDA), financial KPI calculations, and business insights.

---

## 1. Project Architecture

This project is built using a modular and clean software engineering architecture, separating database operations, configuration, helper functions, and raw data from the analysis notebooks.

```text
Cross functional dashboard/
├── data/                       # Pantries for raw & clean files
│   ├── raw/                    # Raw extracts from PostgreSQL (CSV format)
│   └── processed/              # Cleaned datasets ready for KPI/EDA
├── notebooks/                  # Jupyter notebooks for step-by-step EDA
│   ├── 01_database_connection.ipynb
│   ├── 02_data_profiling.ipynb
│   ├── 03_data_cleaning.ipynb
│   ├── 04_exploratory_data_analysis.ipynb
│   ├── 05_finance_kpis.ipynb
│   ├── 06_business_insights.ipynb
│   └── 07_visualizations.ipynb
├── reports/                    # Generated PDF/HTML reports & charts
│   ├── figures/                # Exported PNG/JPG visualization figures
│   └── project.log             # Running application log file
├── src/                        # Source python package code
│   ├── config/
│   │   └── config.py           # Loads settings & DB URIs from environment
│   ├── database/
│   │   └── connection.py       # SQLAlchemy engine pooling & session connector
│   ├── extraction/
│   │   └── extract.py          # Script to download database tables
│   └── utils/
│       ├── logger.py           # Application-wide logger configuration
│       └── helpers.py          # Time profiling & file save utilities
├── .env                        # Local database credentials (ignored in git)
├── .env.example                # Configuration template for developers
├── .gitignore                  # Instructs git which files to ignore
├── requirements.txt            # Project python dependencies
└── README.md                   # This instruction guide
```

---

## 2. Prerequisites

- **Python** (version 3.10 or higher recommended)
- **PostgreSQL Database** running locally or in the cloud.
- **Git** (for version control)

---

## 3. Getting Started

Follow these steps to set up the project on your local machine:

### Step 1: Initialize a Python Virtual Environment
Creating a virtual environment ensures that the libraries you install for this project do not conflict with libraries in other projects.

Run in your terminal (PowerShell or Bash) from the project root folder:
```bash
# Create the virtual environment named 'venv'
python -m venv venv

# Activate it (Windows PowerShell)
.\venv\Scripts\Activate.ps1

# Activate it (Mac / Linux)
source venv/bin/activate
```

### Step 2: Install Project Dependencies
Use `pip` to install all the required data libraries:
```bash
pip install -r requirements.txt
```

### Step 3: Configure Environment Variables
1. Duplicate the `.env.example` file and rename it to `.env`.
2. Open `.env` and fill in your actual PostgreSQL credentials:
   ```ini
   DB_HOST=localhost
   DB_PORT=5432
   DB_NAME=retailmart_db
   DB_USER=postgres
   DB_PASSWORD=your_actual_password
   DB_SCHEMA=public
   ```

---

## 4. How to Run Data Extraction

To extract tables from PostgreSQL and save them as CSV files in the `data/raw/` folder, run the extraction pipeline module directly:

```bash
# Make sure virtual environment is active
python -m src.extraction.extract
```
This script will:
1. Connect to PostgreSQL via SQLAlchemy.
2. Read the list of target tables.
3. Extract each table into a Pandas DataFrame.
4. Save the resulting file to `data/raw/<table_name>.csv`.
5. Write execution timestamps and statistics to the console and to `reports/project.log`.

---

## 5. Notebook Workflow Guide

Once the data is extracted, open Jupyter Notebook and run the sequence in order:

1. **`01_database_connection.ipynb`**: Verifies that the connection to the database is working interactively.
2. **`02_data_profiling.ipynb`**: Loads the raw CSVs from `data/raw/` and inspects column types, distributions, and missing values.
3. **`03_data_cleaning.ipynb`**: Performs data cleaning (imputing missing values, removing duplicates, casting date columns) and exports clean datasets to `data/processed/`.
4. **`04_exploratory_data_analysis.ipynb`**: Studies trends, correlations, outliers, and sales distributions.
5. **`05_finance_kpis.ipynb`**: Formulates and calculates metrics (Revenue, COGS, profit margins).
6. **`06_business_insights.ipynb`**: Converts data calculations into findings (best regions, seasonal fluctuations).
7. **`07_visualizations.ipynb`**: Draws final presentation-ready charts for stakeholder decks.

---

## 6. Development Standards

- **PEP 8:** Code follows PEP 8 standards (snake_case functions, 4-space indentation, docstrings, type hinting).
- **Logging:** No `print()` calls are used. All updates are logged using the structured logger in `src.utils.logger`.
- **Security:** Databases credentials are read from `.env`. Never commit `.env` or data files to git.
