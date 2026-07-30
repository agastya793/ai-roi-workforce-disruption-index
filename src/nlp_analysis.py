import pandas as pd
import numpy as np

def run_nlp_analysis(data_path="data/processed/cleaned_panel_data.parquet"):
    """
    Stub for NLP topic modeling (BERTopic) on 10-K filings.
    Since we don't have raw 10-K text in our mock data, this function
    will use the existing `ai_adoption_score` to build the NLP features output.
    """
    try:
        df = pd.read_parquet(data_path)
    except FileNotFoundError:
        print("Data not found. Run data_collection and cleaning first.")
        return
        
    # Simulate BERTopic NLP extracted features
    # Assuming the nlp pipeline extracts AI mention frequency and sentiment
    nlp_df = df[['company_id', 'year', 'quarter', 'ai_adoption_score', 'industry']].copy()
    
    # Introduce proxy NLP metrics
    nlp_df['ai_mention_count'] = (nlp_df['ai_adoption_score'] * np.random.uniform(50, 200, size=len(nlp_df))).astype(int)
    nlp_df['ai_sentiment'] = nlp_df['ai_adoption_score'] * np.random.normal(0.6, 0.2, size=len(nlp_df))
    
    # Scale sentiment to -1 to 1
    nlp_df['ai_sentiment'] = nlp_df['ai_sentiment'].clip(-1, 1)
    
    output_path = "data/processed/nlp_features.parquet"
    nlp_df.to_parquet(output_path, index=False)
    print(f"NLP features saved to {output_path}")
    
    return nlp_df

if __name__ == "__main__":
    run_nlp_analysis()
