import pandas as pd
# pyrefly: ignore [missing-import]
from statsmodels.formula.api import ols
import numpy as np
from sklearn.ensemble import RandomForestRegressor

def run_regression_analysis(data_path="data/processed/cleaned_panel_data.parquet"):
    """
    Panel data regression (fixed effects proxy via OLS with dummies) 
    to measure AI adoption's causal impact on productivity.
    """
    try:
        df = pd.read_parquet(data_path)
    except FileNotFoundError:
        print("Data not found.")
        return None
        
    # We want to estimate: log(rev_per_employee) ~ ai_adoption_score + log(rnd_spending) + industry_fixed_effects
    # To avoid log(0), we add 1
    df['log_rev_per_employee'] = np.log(df['rev_per_employee'] + 1)
    df['log_rnd_spending'] = np.log(df['rnd_spending'] + 1)
    
    # Simple OLS with industry fixed effects
    model = ols('log_rev_per_employee ~ ai_adoption_score + log_rnd_spending + C(industry)', data=df).fit()
    print("--- OLS Regression Results (Rev per Employee) ---")
    print(model.summary().tables[1])
    
    # Headcount regression
    df['log_headcount'] = np.log(df['headcount'] + 1)
    model_hc = ols('log_headcount ~ ai_adoption_score + log_rnd_spending + C(industry)', data=df).fit()
    print("\n--- OLS Regression Results (Headcount) ---")
    print(model_hc.summary().tables[1])
    
    return model, model_hc

def run_did_analysis(data_path="data/processed/cleaned_panel_data.parquet"):
    """
    Difference-in-Differences (DiD) comparing high-AI-adopting vs. 
    low-AI-adopting firms within the same industry.
    """
    try:
        df = pd.read_parquet(data_path)
    except FileNotFoundError:
        print("Data not found.")
        return None
        
    # Post-treatment period definition (e.g., after 2023)
    df['post'] = (df['year'] >= 2023).astype(int)
    
    # Treatment group (is_adopter)
    df['treatment'] = df['is_adopter'].astype(int)
    
    # DiD interaction term
    df['did'] = df['post'] * df['treatment']
    
    model = ols('rev_per_employee ~ treatment + post + did + C(industry)', data=df).fit()
    print("\n--- Difference-in-Differences Results ---")
    print(model.summary().tables[1])
    
    return model

def run_ml_feature_importance(data_path="data/processed/cleaned_panel_data.parquet"):
    """
    Trains a Random Forest Regressor to predict Revenue per Employee 
    and extracts feature importance to compare AI adoption against other factors.
    """
    try:
        df = pd.read_parquet(data_path)
    except FileNotFoundError:
        print("Data not found.")
        return None
        
    features = ['ai_adoption_score', 'rnd_spending', 'operating_margin', 'headcount']
    X = df[features].fillna(0)
    y = df['rev_per_employee'].fillna(0)
    
    rf = RandomForestRegressor(n_estimators=100, random_state=42)
    rf.fit(X, y)
    
    importance = rf.feature_importances_
    fi_df = pd.DataFrame({
        'Feature': ['AI Adoption Score', 'R&D Spending', 'Operating Margin', 'Headcount Size'],
        'Importance': importance
    }).sort_values('Importance', ascending=False)
    
    fi_df.to_csv("data/processed/feature_importance.csv", index=False)
    print("Feature importance saved to data/processed/feature_importance.csv")
    return fi_df

if __name__ == "__main__":
    run_regression_analysis()
    run_did_analysis()
    run_ml_feature_importance()
