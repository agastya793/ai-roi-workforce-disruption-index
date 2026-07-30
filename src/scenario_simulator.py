import pandas as pd
import numpy as np

def run_monte_carlo_scenarios(index_path="data/processed/index_scores.csv", n_simulations=1000):
    """
    Monte Carlo simulation for 3 scenarios (conservative, moderate, aggressive AI adoption).
    Returns a dataframe of projected industry ROI and Headcount impacts in 2030.
    """
    try:
        df = pd.read_csv(index_path)
    except FileNotFoundError:
        print("Index data not found.")
        return None
        
    scenarios = {
        'Conservative': {'mean_growth': 1.05, 'std_dev': 0.02},
        'Moderate': {'mean_growth': 1.15, 'std_dev': 0.05},
        'Aggressive': {'mean_growth': 1.30, 'std_dev': 0.10}
    }
    
    results = []
    
    for _, row in df.iterrows():
        industry = row['industry']
        base_roi = row['ai_roi_index']
        
        for scenario_name, params in scenarios.items():
            # Simulate 2030 ROI
            simulations = np.random.normal(
                loc=base_roi * params['mean_growth'],
                scale=base_roi * params['std_dev'],
                size=n_simulations
            )
            simulations = np.clip(simulations, 0, 100) # Cap at 100
            
            projected_roi = np.mean(simulations)
            confidence_interval = np.percentile(simulations, [5, 95])
            
            results.append({
                'industry': industry,
                'scenario': scenario_name,
                'projected_roi_2030': projected_roi,
                'ci_lower': confidence_interval[0],
                'ci_upper': confidence_interval[1]
            })
            
    res_df = pd.DataFrame(results)
    res_df.to_csv("data/processed/scenario_projections.csv", index=False)
    print("Scenario projections saved to data/processed/scenario_projections.csv")
    
    return res_df

if __name__ == "__main__":
    run_monte_carlo_scenarios()
