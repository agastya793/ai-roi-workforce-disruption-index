import streamlit as st
import pandas as pd
import sys
import os
import plotly.express as px

# Ensure src is in path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.visualization import (
    generate_roi_heatmap, 
    generate_workforce_displacement_chart, 
    generate_scatter_productivity
)
from src.scenario_simulator import run_monte_carlo_scenarios

# Page Config
st.set_page_config(
    page_title="AI Productivity Paradox Dashboard",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for dark theme adjustments if needed
st.markdown("""
<style>
    .reportview-container {
        background: #121212;
    }
    .sidebar .sidebar-content {
        background: #1e1e1e;
    }
</style>
""", unsafe_allow_html=True)

st.title("🤖 The AI Productivity Paradox (2020-2026)")
st.markdown("Quantifying Enterprise AI ROI and Workforce Displacement Across 15 Industries.")

# Load Data
@st.cache_data
def load_data():
    try:
        panel_df = pd.read_parquet("data/processed/cleaned_panel_data.parquet")
        index_df = pd.read_csv("data/processed/index_scores.csv")
        try:
            fi_df = pd.read_csv("data/processed/feature_importance.csv")
        except:
            fi_df = None
        return panel_df, index_df, fi_df
    except Exception as e:
        st.error(f"Error loading data: {e}. Make sure to run the data pipelines first.")
        return None, None, None

panel_df, index_df, fi_df = load_data()

if panel_df is not None and index_df is not None:
    st.sidebar.header("Navigation")
    page = st.sidebar.radio("Go to", ["Executive Summary", "Company Deep Dive", "Industry ROI", "Workforce Displacement", "Scenario Modeling"])
    
    if page == "Executive Summary":
        st.header("Executive Summary")
        col1, col2, col3 = st.columns(3)
        col1.metric("Total Industries Analyzed", len(index_df))
        col2.metric("High ROI Industries", len(index_df[index_df['ai_roi_index'] > 75]))
        col3.metric("Avg Rev/Employee Gain", "12.3%") # Mocked metric from report
        
        st.plotly_chart(generate_scatter_productivity(index_df), use_container_width=True)
        
        if fi_df is not None:
            st.subheader("Machine Learning Feature Importance (Random Forest)")
            fig = px.bar(fi_df, x='Importance', y='Feature', orientation='h', title="Top Predictors of Revenue per Employee", color='Importance', color_continuous_scale='viridis')
            fig.update_layout(yaxis={'categoryorder':'total ascending'})
            st.plotly_chart(fig, use_container_width=True)
            
    elif page == "Company Deep Dive":
        st.header("Interactive Company Deep Dive & What-If Simulator")
        
        company = st.selectbox("Select a Company", sorted(panel_df['company_id'].unique()))
        comp_df = panel_df[panel_df['company_id'] == company].copy()
        
        st.subheader(f"Historical Trend for {company}")
        fig = px.line(comp_df, x='date', y='rev_per_employee', title=f"{company}: Actual Revenue per Employee ($M)")
        st.plotly_chart(fig, use_container_width=True)
        
        st.subheader("What-If Simulator")
        st.markdown("Use the slider to simulate the effect of increasing this company's AI investment.")
        
        # Base stats
        current_ai = comp_df['ai_adoption_score'].iloc[-1]
        current_rev = comp_df['rev_per_employee'].iloc[-1]
        
        boost = st.slider("Increase AI Adoption By (%)", min_value=0, max_value=100, value=0, step=5)
        
        # Simple projection model based on DiD coefficients (~10% rev boost for full 1.0 score bump)
        new_rev = current_rev * (1 + ((boost/100.0) * 0.10))
        
        col1, col2 = st.columns(2)
        col1.metric("Current AI Adoption Score", f"{current_ai:.2f}")
        col2.metric("Projected Revenue per Employee ($M)", f"${new_rev:,.2f}M", f"+${(new_rev - current_rev):,.2f}M")
        
    elif page == "Industry ROI":
        st.header("Industry ROI Heatmap")
        st.plotly_chart(generate_roi_heatmap(index_df), use_container_width=True)
        st.dataframe(index_df[['industry', 'ai_roi_index', 'ai_adoption_score']].style.background_gradient(cmap='viridis'))
        
    elif page == "Workforce Displacement":
        st.header("Workforce Displacement Over Time")
        st.plotly_chart(generate_workforce_displacement_chart(panel_df), use_container_width=True)
        
    elif page == "Scenario Modeling":
        st.header("Monte Carlo Scenario Projections (2030)")
        if st.button("Run Monte Carlo Simulations"):
            with st.spinner("Running 1000 simulations per scenario..."):
                scenario_df = run_monte_carlo_scenarios("data/processed/index_scores.csv")
                st.success("Simulations complete!")
                st.dataframe(scenario_df)
else:
    st.warning("Please generate the dataset by running `python -m src.data_collection` and `python -m src.cleaning` first.")
