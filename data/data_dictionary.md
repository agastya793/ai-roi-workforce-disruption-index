# Data Dictionary

| Variable Name | Source | Description | Type |
|---------------|--------|-------------|------|
| `company_id` | yfinance | Unique ticker symbol for the company | String |
| `industry` | Manual Mapping | One of the 15 predefined industry categories | String |
| `year` | Temporal | Year of the observation | Integer |
| `quarter` | Temporal | Quarter of the observation (1-4) | Integer |
| `revenue` | Alpha Vantage | Quarterly revenue in USD millions | Float |
| `headcount` | SEC 10-K | Total reported full-time employees | Integer |
| `rnd_spending` | SEC 10-K | Research and Development spending in USD millions | Float |
| `operating_margin` | yfinance | Operating Income / Total Revenue | Float |
| `ai_patents` | USPTO | Number of AI-related patents filed in the period | Integer |
| `ai_adoption_score` | NLP Model | NLP-derived score representing AI intensity in 10-K | Float (0-1) |
| `rev_per_employee` | Calculated | `revenue` / `headcount` | Float |
| `industry_ai_roi_index` | Calculated | Composite index measuring AI ROI (0-100) | Float |
| `workforce_disruption_index`| Calculated | Composite index measuring workforce disruption risk (0-100) | Float |
