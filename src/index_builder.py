import pandas as pd
import numpy as np

def build_indices(data_path="data/processed/cleaned_panel_data.parquet", nlp_path="data/processed/nlp_features.parquet"):
    """
    Builds the AI ROI Index and Workforce Disruption Index by industry.
    """
    try:
        df = pd.read_parquet(data_path)
        nlp_df = pd.read_parquet(nlp_path)
        
        # Merge data
        merged = pd.merge(df, nlp_df[['company_id', 'year', 'quarter', 'ai_mention_count', 'ai_sentiment']], 
                          on=['company_id', 'year', 'quarter'], how='left')
    except FileNotFoundError:
        print("Data missing.")
        return None
        
    # Aggregate to industry level across all time
    ind_grp = merged.groupby('industry').agg({
        'rev_per_employee': 'mean',
        'headcount': 'mean',
        'rnd_spending': 'mean',
        'operating_margin': 'mean',
        'ai_adoption_score': 'mean',
        'ai_mention_count': 'mean',
        'ai_sentiment': 'mean'
    }).reset_index()
    
    # Normalize values for indices (Min-Max scaling 0 to 100)
    for col in ['rev_per_employee', 'operating_margin', 'ai_adoption_score']:
        min_val = ind_grp[col].min()
        max_val = ind_grp[col].max()
        ind_grp[f'{col}_norm'] = 100 * (ind_grp[col] - min_val) / (max_val - min_val + 1e-9)
        
    # Composite AI ROI Index = (Rev_per_emp_norm * 0.4) + (Op_margin_norm * 0.4) + (AI_adoption_norm * 0.2)
    ind_grp['ai_roi_index'] = (
        ind_grp['rev_per_employee_norm'] * 0.4 +
        ind_grp['operating_margin_norm'] * 0.4 +
        ind_grp['ai_adoption_score_norm'] * 0.2
    ).round(2)
    
    # Normalize inverse variables for disruption
    # Higher headcount reduction (lower headcount vs peer) -> higher disruption
    hc_max = ind_grp['headcount'].max()
    hc_min = ind_grp['headcount'].min()
    ind_grp['headcount_reduction_norm'] = 100 * (1 - (ind_grp['headcount'] - hc_min) / (hc_max - hc_min + 1e-9))
    
    # Workforce Disruption Index = (Headcount reduction * 0.6) + (AI mention * 0.4)
    ment_min = ind_grp['ai_mention_count'].min()
    ment_max = ind_grp['ai_mention_count'].max()
    ind_grp['ai_mention_norm'] = 100 * (ind_grp['ai_mention_count'] - ment_min) / (ment_max - ment_min + 1e-9)
    
    ind_grp['workforce_disruption_index'] = (
        ind_grp['headcount_reduction_norm'] * 0.6 +
        ind_grp['ai_mention_norm'] * 0.4
    ).round(2)
    
    output_df = ind_grp[['industry', 'ai_roi_index', 'workforce_disruption_index', 'ai_adoption_score', 'rev_per_employee', 'operating_margin']].sort_values(by='ai_roi_index', ascending=False)
    
    output_path = "data/processed/index_scores.csv"
    output_df.to_csv(output_path, index=False)
    print(f"Indices saved to {output_path}")
    
    return output_df

if __name__ == "__main__":
    build_indices()
