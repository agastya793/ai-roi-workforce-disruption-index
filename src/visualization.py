import pandas as pd
# pyrefly: ignore [missing-import]
import plotly.express as px

def generate_roi_heatmap(index_df):
    """Generates the Industry ROI Heatmap."""
    fig = px.density_heatmap(
        index_df, 
        x="industry", 
        y="ai_roi_index", 
        z="operating_margin",
        color_continuous_scale="Viridis",
        title="Industry ROI Heatmap by Operating Margin"
    )
    return fig

def generate_workforce_displacement_chart(panel_df):
    """Generates Workforce Displacement Timeline."""
    agg_df = panel_df.groupby(['date', 'industry'])['headcount'].mean().reset_index()
    fig = px.line(
        agg_df, 
        x="date", 
        y="headcount", 
        color="industry",
        title="Workforce Displacement Timeline"
    )
    return fig

def generate_scatter_productivity(index_df):
    """Generates AI Investment vs Productivity Scatter."""
    fig = px.scatter(
        index_df, 
        x="ai_adoption_score", 
        y="rev_per_employee", 
        size="ai_roi_index",
        color="industry",
        hover_name="industry",
        title="AI Adoption vs. Productivity Gains"
    )
    return fig
