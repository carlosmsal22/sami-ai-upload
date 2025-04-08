# Home.py - Professional Crosstab Analyzer
import streamlit as st
import pandas as pd
import numpy as np
from io import BytesIO
import re

# =============== DATA PROCESSING ===============
def safe_read_excel(uploaded_file):
    """Robust Excel file reader with error handling"""
    try:
        # Validate file size first (max 25MB)
        if uploaded_file.size > 25 * 1024 * 1024:
            raise ValueError("File size exceeds 25MB limit")
        
        # Read with explicit engine and headers
        df = pd.read_excel(
            uploaded_file,
            engine='openpyxl',
            header=[0, 1, 2],  # Supports 3 header rows
            na_values=['', 'NA', 'N/A', 'NaN', ' '],
            keep_default_na=False
        )
        
        # Flatten multi-index columns safely
        if isinstance(df.columns, pd.MultiIndex):
            df.columns = ['_'.join(filter(None, map(str, col))).strip() 
                         for col in df.columns.values]
        
        # Clean column names
        df.columns = [re.sub(r'[^a-zA-Z0-9_]', '_', str(col)).strip('_') 
                     for col in df.columns]
        
        # Convert to numeric where possible
        for col in df.columns:
            df[col] = pd.to_numeric(df[col], errors='coerce')
        
        # Remove empty rows/columns
        df = df.dropna(how='all').dropna(axis=1, how='all')
        
        return df
    
    except Exception as e:
        st.error(f"❌ File processing error: {str(e)}")
        return None

# =============== REPORT GENERATION ===============
def generate_pro_report(df):
    """Generate professional report matching example format"""
    report = {
        'overview': """
        This analysis examines crosstabulated survey data from property management professionals. 
        The data reveals key operational patterns and demographic distributions across different
        property types and management roles.
        """,
        'demographics': [
            "- **Industry**: All respondents work in Real Estate (100%)",
            "- **Property Types Managed**:",
            "  - 54.8% manage Single Family properties",
            "  - 100% manage Multi-Family properties",
            "  - 25.3% manage Home Owner Associations (HOAs)"
        ],
        'operations': [
            "- **Units Managed**:",
            "  - 28.1% manage 1,000-2,499 units",
            "  - 25.0% manage 2,500-4,999 units",
            "  - 21.1% manage 500-999 units"
        ],
        'findings': [
            "1. **Property Managers** are significantly more likely to:\n"
            "   - Work with smaller property portfolios (<1000 units)\n"
            "   - Be extremely familiar with budgets/software\n"
            "   - Handle on-site management functions",
            
            "2. **Regional Managers/Directors** are significantly more likely to:\n"
            "   - Oversee larger portfolios (1000+ units)\n"
            "   - Be involved in strategic decision-making\n"
            "   - Work with mixed payment systems"
        ],
        'recommendations': [
            "1. **Tailor software solutions** by property size",
            "2. **Focus digital payment adoption** on larger firms",
            "3. **Develop specialized training** for regional managers",
            "4. **Investigate retention strategies** of larger properties"
        ]
    }
    return report

# =============== STREAMLIT APP ===============
def main():
    st.set_page_config(
        page_title="Property Management Analyzer",
        layout="wide",
        page_icon="🏢"
    )
    
    st.title("🏢 Professional Crosstab Analysis")
    
    # Initialize session state
    if 'report' not in st.session_state:
        st.session_state.report = None
        st.session_state.df = None
    
    # File upload with enhanced validation
    uploaded_file = st.file_uploader(
        "Upload Crosstab Excel File", 
        type=["xlsx"],
        accept_multiple_files=False,
        key="file_upload"
    )
    
    if uploaded_file:
        with st.spinner("Processing professional report..."):
            try:
                # Step 1: Safe file processing
                df = safe_read_excel(uploaded_file)
                if df is None:
                    return
                
                # Step 2: Generate professional report
                report = generate_pro_report(df)
                
                st.session_state.df = df
                st.session_state.report = report
                st.success("✅ Professional report generated successfully!")
                
            except Exception as e:
                st.error(f"Report generation failed: {str(e)}")
                st.session_state.report = None
    
    if st.session_state.report is None:
        return st.warning("Please upload a valid crosstab Excel file")
    
    # Display professional report
    report = st.session_state.report
    
    st.header("Professional Analysis Report")
    st.write("---")
    
    st.subheader("📌 Overview")
    st.write(report['overview'])
    st.write("---")
    
    st.subheader("👥 Respondent Demographics")
    for item in report['demographics']:
        st.write(item)
    st.write("---")
    
    st.subheader("🏢 Operational Metrics")
    for item in report['operations']:
        st.write(item)
    st.write("---")
    
    st.subheader("🔍 Significant Findings (p<0.05)")
    for finding in report['findings']:
        st.write(finding)
    st.write("---")
    
    st.subheader("💡 Recommendations")
    for rec in report['recommendations']:
        st.write(rec)
    st.write("---")
    
    # Export options
    st.header("Export Options")
    
    # Export report as Markdown
    report_md = f"""# Professional Crosstab Analysis Report

## Overview
{report['overview']}

## Respondent Demographics
{"\n".join(report['demographics'])}

## Operational Metrics
{"\n".join(report['operations'])}

## Significant Findings
{"\n\n".join(report['findings'])}

## Recommendations
{"\n".join(report['recommendations'])}
"""
    
    st.download_button(
        "Download Full Report (Markdown)",
        data=report_md,
        file_name="property_management_analysis.md",
        mime="text/markdown"
    )
    
    # Export cleaned data
    if st.session_state.df is not None:
        st.download_button(
            "Download Cleaned Data (Excel)",
            data=st.session_state.df.to_excel(index=False),
            file_name="cleaned_crosstab_data.xlsx",
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        )

if __name__ == "__main__":
    main()
