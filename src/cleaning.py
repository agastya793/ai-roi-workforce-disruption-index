import pandas as pd
import os

def clean_panel_data(input_path="data/processed/merged_panel_data.parquet", output_path="data/processed/cleaned_panel_data.parquet"):
    """
    Cleans and preprocesses the merged panel data.
    """
    if not os.path.exists(input_path):
        print(f"{input_path} not found. Please run data_collection.py first.")
        return None
        
    df = pd.read_parquet(input_path)
    
    # Handle any outliers (e.g., negative revenues)
    df = df[df["revenue"] > 0]
    df = df[df["headcount"] > 0]
    
    # Re-calculate rev per employee to ensure consistency
    df["rev_per_employee"] = df["revenue"] / df["headcount"]
    
    # Create date index for time series
    df['date'] = pd.to_datetime(df['year'].astype(str) + 'Q' + df['quarter'].astype(str))
    
    df.to_parquet(output_path, index=False)
    print(f"Cleaned data saved to {output_path}")
    return df
    
if __name__ == "__main__":
    clean_panel_data()
