# 🚀 The AI Productivity Paradox: Enterprise AI ROI & Workforce Disruption Index


> **An end-to-end econometric data pipeline and interactive dashboard quantifying the actual ROI and workforce displacement of AI adoption across 45 publicly traded companies in 15 industries (2020-2026).**

---

## 🎯 Business Problem & Impact
Despite $300B+ in global AI investment since 2020, most companies cannot quantify their actual return on investment (ROI) from AI adoption. This project builds an empirical, data-driven framework to separate AI hype from reality. 


## 🛠️ Tech Stack & Skills Highlight
- **Data Engineering:** Python, Pandas, NumPy, Live API Integration (`yfinance`)
- **Statistical & ML Modeling:** `statsmodels` (Fixed Effects OLS, DiD), `scikit-learn` (Random Forest Predictor), Monte Carlo Simulations
- **Data Visualization & UI:** Streamlit (Interactive What-If Simulators), Plotly
- **Workflow:** Modular repository architecture, clean code practices

## 📊 Methodology (Hybrid Data Approach)
To ensure the pipeline is robust and production-ready while bypassing expensive paid API rate limits, the architecture uses a hybrid data approach:
1. **Live Financial Backbone:** Pulls real-time historical market data, revenue, headcount, and operating margins for 45 curated tickers (e.g., AAPL, JPM, WMT) using the Yahoo Finance API.
2. **AI Adoption Proxies:** Mathematically models NLP (10-K mentions) and Patent filing frequency over top of the real financial baseline to simulate AI adoption curves.

## 📁 Repository Architecture
```text
ai-roi-workforce-disruption-index/
├── dashboard/               # Streamlit web application & UI components
├── data/                    # Generated datasets and data dictionary
├── notebooks/               # Jupyter notebooks for exploratory data analysis
├── reports/                 # Markdown/PDF reports (Executive Summary, Methodology)
├── src/                     # Core Python modules
│   ├── data_collection.py   # Live API fetching (yfinance)
│   ├── cleaning.py          # Data preprocessing & outlier handling
│   ├── nlp_analysis.py      # NLP proxy simulations
│   ├── index_builder.py     # Aggregation for ROI and Disruption Indices
│   ├── scenario_simulator.py# Monte Carlo simulation engine
│   └── statistical_models.py# DiD and Panel Regression models
└── README.md
```

## 🚀 Quickstart (Run Locally)

**1. Clone & Install Dependencies:**
```bash
git clone <your-repo-url>
cd ai-roi-workforce-disruption-index
pip install pandas streamlit plotly yfinance statsmodels scikit-learn numpy
```

**2. Run the Data Pipeline (Generates live financial data & builds models):**
```bash
python -m src.data_collection
python -m src.cleaning
python -m src.nlp_analysis
python -m src.index_builder
python -m src.scenario_simulator
python -m src.statistical_models
```

**3. Launch the Dashboard:**
```bash
streamlit run dashboard/app.py
```

## 📜 License
MIT License
