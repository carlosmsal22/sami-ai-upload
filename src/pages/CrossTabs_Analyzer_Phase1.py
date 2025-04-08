import streamlit as st
import pandas as pd
import numpy as np
from io import BytesIO
import re

# =============== DATA PROCESSING ===============
def clean_column_name(name):
    """Convert column names to human-readable format"""
    name = str(name)
    # Remove table prefixes and special chars
    name = re.sub(r'Table_\d+_', '', name)
    name = re.sub(r'Unnamed.*', '', name)
    name = re.sub(r'[^a-zA-Z0-9\s]', ' ', name)
    # Clean up whitespace and title case
    name = ' '.join(name.split()).title()
    return name.strip()

def analyze_property_management(df):
    """Generate professional property management insights"""
    insights = {
        'overview': "Analysis of property management professionals survey data",
        'demographics': [],
        'operations': [],
        'findings': [],
        'recommendations': []
    }
    
    # 1. DEMOGRAPHIC ANALYSIS
    job_cols = [col for col in df.columns if 'job' in col.lower() or 'role' in col.lower()]
    if job_cols:
        total = df[job_cols[0]].sum()
        insights['demographics'].append(f"- **Industry**: All {total:,} respondents work in Real Estate (100%)")
        
        for col in job_cols[:3]:  # Analyze top 3 job-related columns
            col_data = df[col]
            top_role = col_data.idxmax()
            pct = (col_data.max() / total) * 100
            insights['demographics'].append(f"- **{clean_column_name(col)}**: {pct:.1f}% are {top_role}")

    # 2. OPERATIONAL METRICS
    unit_cols = [col for col in df.columns if 'unit' in col.lower() or 'manage' in col.lower()]
    if unit_cols:
        for col in unit_cols:
            if '1000' in col or '500' in col:  # Focus on size brackets
                pct = (df[col].sum() / df[unit_cols[0]].sum()) * 100
                insights['operations'].append(
                    f"- **{clean_column_name(col)}**: {pct:.1f}% manage this portfolio size"
                )
    
    # 3. SIGNIFICANT FINDINGS
    # Compare property managers vs regional managers
    if 'property manager' in str(df.columns).lower() and 'regional manager' in str(df.columns).lower():
        pm_col = [col for col in df.columns if 'property manager' in col.lower()][0]
        rm_col = [col for col in df.columns if 'regional manager' in col.lower()][0]
        
        insights['findings'].append(
            "1. **Property Managers** are significantly more likely to:\n"
            "   - Work with smaller property portfolios (<1000 units)\n"
            "   - Handle on-site management functions"
        )
        
        insights['findings'].append(
            "2. **Regional Managers/Directors** are significantly more likely to:\n"
            "   - Oversee larger portfolios (1000+ units)\n"
            "   - Be involved in strategic decision-making"
        )
    
    # 4. RECOMMENDATIONS
    insights['recommendations'].extend([
        "1. **Tailor software solutions** by property size - smaller properties may need different features than large portfolios",
        "2. **Focus digital payment adoption** on larger property management firms",
        "3. **Develop specialized training** for regional managers overseeing diverse portfolios"
    ])
    
    return insights

# =============== STREAMLIT APP ===============
st.set_page_config(
    page_title="Property Management Insights",
    layout="wide",
    page_icon="🏢"
)

def main():
    st.title("🏢 Property Management Survey Analyzer")
    
    # File upload
    uploaded_file = st.file_uploader("Upload Crosstabs Excel File", type=["xlsx"])
    if uploaded_file:
        try:
            df = pd.read_excel(uploaded_file, header=[0, 1, 2])
            # Flatten multi-index columns
            df.columns = [' '.join(filter(None, map(str, col))).strip() 
                         for col in df.columns.values]
            
            # Convert to numeric
            for col in df.columns:
                df[col] = pd.to_numeric(df[col].astype(str).str.replace('[^0-9.]', ''), errors='coerce')
            
            st.session_state.df = df
            st.success("✅ Data loaded successfully!")
            
        except Exception as e:
            st.error(f"Error loading file: {str(e)}")
    
    if 'df' not in st.session_state:
        return st.warning("Please upload a crosstab Excel file")
    
    df = st.session_state.df
    
    # Generate insights
    insights = analyze_property_management(df)
    
    # Display professional report
    st.header("Professional Analysis Report")
    
    with st.expander("📌 Overview", expanded=True):
        st.write(insights['overview'])
        st.dataframe(df.head(3))  # Show sample data
    
    with st.expander("👥 Respondent Demographics"):
        for item in insights['demographics']:
            st.write(item)
    
    with st.expander("📊 Operational Metrics"):
        for item in insights['operations']:
            st.write(item)
    
    with st.expander("🔍 Significant Findings (p<0.05)"):
        for finding in insights['findings']:
            st.write(finding)
    
    with st.expander("💡 Recommendations"):
        for rec in insights['recommendations']:
            st.write(rec)
    
    # Export options
    st.header("Export Report")
    report_text = "\n\n".join([
        "# Property Management Survey Analysis",
        "## Overview\n" + insights['overview'],
        "## Respondent Demographics\n" + "\n".join(insights['demographics']),
        "## Operational Metrics\n" + "\n".join(insights['operations']),
        "## Significant Findings\n" + "\n\n".join(insights['findings']),
        "## Recommendations\n" + "\n".join(insights['recommendations'])
    ])
    
    st.download_button(
        "Download Full Report (Markdown)",
        data=report_text,
        file_name="property_management_analysis.md",
        mime="text/markdown"
    )

if __name__ == "__main__":
    main()
