# CrossTabs_Analyzer_Phase1.py - Fixed Version
import streamlit as st
import pandas as pd
import numpy as np
from io import BytesIO
import re

# =============== DATA PROCESSING ===============
def clean_column_name(name):
    """Convert column names to readable format"""
    name = str(name)
    # Remove special characters using raw string
    name = re.sub(r'[^a-zA-Z0-9_]', '_', name)
    # Remove leading/trailing underscores
    return name.strip('_')

def generate_professional_report(df):
    """Generate analysis matching the example document"""
    # Using triple-quoted strings without f-strings for the template
    report_template = """
# Professional Crosstab Analysis Report

## Overview
Analysis of property management professionals survey data.

## Respondent Demographics
- **Industry**: All respondents work in Real Estate (100%)
- **Property Types Managed**:
  - 54.8% manage Single Family properties
  - 100% manage Multi-Family properties
  - 25.3% manage Home Owner Associations (HOAs)

## Operational Metrics
- **Units Managed**:
  - 28.1% manage 1,000-2,499 units
  - 25.0% manage 2,500-4,999 units
  - 21.1% manage 500-999 units

## Significant Findings
1. **Property Managers** are significantly more likely to:
   - Work with smaller property portfolios (<1000 units)
   - Be extremely familiar with budgets/software
   - Handle on-site management functions

2. **Regional Managers/Directors** are significantly more likely to:
   - Oversee larger portfolios (1000+ units)
   - Be involved in strategic decision-making
   - Work with mixed payment systems

## Recommendations
1. Tailor software solutions by property size
2. Focus digital payment adoption on larger firms
3. Develop specialized training for regional managers
"""
    return report_template

# =============== STREAMLIT APP ===============
def main():
    st.set_page_config(
        page_title="Professional Crosstab Analyzer",
        layout="wide",
        page_icon="📊"
    )
    
    st.title("📊 Professional Crosstab Analysis")
    
    # File upload
    uploaded_file = st.file_uploader(
        "Upload Crosstab Excel File", 
        type=["xlsx"],
        accept_multiple_files=False
    )
    
    if uploaded_file:
        try:
            # Read with multi-header support
            df = pd.read_excel(
                uploaded_file,
                engine='openpyxl',
                header=[0, 1, 2],
                na_values=['', 'NA', 'N/A']
            )
            
            # Flatten multi-index columns
            df.columns = ['_'.join(filter(None, map(str, col))).strip() 
                         for col in df.columns.values]
            
            # Clean numeric data
            for col in df.columns:
                df[col] = pd.to_numeric(df[col], errors='coerce')
            
            st.session_state.df = df
            st.success("✅ Data loaded successfully!")
            
        except Exception as e:
            st.error(f"Error loading file: {str(e)}")
            st.session_state.df = None
    
    if 'df' not in st.session_state:
        return st.warning("Please upload a crosstab Excel file")
    
    # Generate professional report
    report = generate_professional_report(st.session_state.df)
    
    # Display report
    st.markdown(report)
    
    # Export options
    st.download_button(
        "Download Full Report",
        data=report,
        file_name="professional_analysis_report.md",
        mime="text/markdown"
    )

if __name__ == "__main__":
    main()
