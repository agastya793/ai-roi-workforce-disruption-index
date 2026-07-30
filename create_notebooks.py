import json
import os

notebooks = [
    "01_data_collection_sec_edgar.ipynb",
    "02_data_collection_bls_fred.ipynb",
    "03_data_cleaning_and_merging.ipynb",
    "04_exploratory_data_analysis.ipynb",
    "05_nlp_filing_analysis.ipynb",
    "06_panel_regression_analysis.ipynb",
    "07_did_causal_inference.ipynb",
    "08_index_construction.ipynb",
    "09_scenario_modeling.ipynb",
    "10_visualization_and_reporting.ipynb"
]

os.makedirs('notebooks', exist_ok=True)

for nb in notebooks:
    content = {
        "cells": [
            {
                "cell_type": "markdown",
                "metadata": {},
                "source": [f"# {nb.replace('_', ' ').replace('.ipynb', '').title()}\n\n", "This notebook is part of the AI ROI & Workforce Disruption Index analysis pipeline."]
            },
            {
                "cell_type": "code",
                "execution_count": None,
                "metadata": {},
                "outputs": [],
                "source": ["import pandas as pd\n", "import numpy as np\n", "import os\n", "import sys\n", "sys.path.append('..')"]
            }
        ],
        "metadata": {
            "kernelspec": {
                "display_name": "Python 3",
                "language": "python",
                "name": "python3"
            }
        },
        "nbformat": 4,
        "nbformat_minor": 4
    }
    with open(f'notebooks/{nb}', 'w') as f:
        json.dump(content, f, indent=2)

print("Notebooks created successfully.")
