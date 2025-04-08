import streamlit as st
import pandas as pd
import numpy as np
from io import BytesIO
import re

# =============== DATA PROCESSING ===============
def clean_column_name(name):
    """Convert messy column names to readable format"""
    if not isinstance(name, str):
        name = str(name)
    # Remove special characters and extra spaces
    name = re.sub(r'[^a-zA-Z0-9\s]', ' ', name)
    # Convert to title case
    name = name.title().replace('_', ' ')
    # Remove duplicate spaces
    name = ' '.join(name.split())
    return name

def analyze_crosstabs(df):
    """Generate professional analysis from crosstab data"""
    analysis = {
        'overview': "",
        'demographics': [],
        'operations': [],
        'findings': [],
        'recommendations': []
    }
    
    # Extract key metrics
    total_respondents = df.iloc[:, 0].sum()
    
    # Demographic analysis
    demo_cols = [col for col in df.columns if 'job' in col.lower() or 'role' in col.lower()]
    if demo_cols:
        analysis['demographics'].append(f"- **Total Respondents**: {total_respondents:,}")
        for col in demo_cols[:3]:  # Analyze top 3 demographic columns
            clean_col = clean_column_name(col)
            top_category = df[col].idxmax()
            pct = (df[col].max() / total_respondents) * 100
            analysis['demographics'].append(f"- **{clean_col}**: {pct:.1f}% are {top_category}")
    
    # Operational metrics
    metric_cols = [col for col in df.columns if 'unit' in col.lower() or 'manage' in col.lower()]
    if metric_cols:
        for col in metric_cols[:3]:  # Analyze top 3 metric columns
            clean_col = clean_column_name(col)
            avg = df[col].mean()
            analysis['operations'].append(f"- **{clean_col}**: Average {avg:,.2f} units")
    
    # Significant findings
    if len(df.columns) >= 2:
        col1, col2 = df.columns[0], df.columns[1]
        corr = df[col1].corr(df[col2])
        if abs(corr) > 0.3:
            direction = "positively" if corr > 0 else "negatively"
            analysis['findings'].append(
                f"**{clean_column_name(col1)}** and **{clean_column_name(col2)}** "
                f"show {direction} correlated trends (r={corr:.2f})"
            )
    
    # Generate recommendations
    if analysis['findings']:
        analysis['recommendations'].append(
            "**Tailor solutions** by property size based on observed operational differences"
        )
        analysis['recommendations'].append(
            "**Focus adoption** on key metrics showing strong correlations"
        )
    
    return analysis

# =============== STREAMLIT APP ===============
st.set_page_config(
    page_title="Professional Crosstab Analyzer",
    layout="wide",
    page_icon="📊"
)

def main():
    st.title("📊 Professional Crosstab Analysis")
    
    # File upload
    uploaded_file = st.file_uploader("Upload Crosstab Excel File", type=["xlsx"])
    if uploaded_file:
        try:
            df = pd.read_excel(uploaded_file, header=[0, 1, 2])
            # Flatten multi-index columns
            df.columns = [' '.join(filter(None, map(str, col))).strip() 
                         for col in df.columns.values]
            
            # Clean numeric data
            for col in df.columns:
                df[col] = pd.to_numeric(df[col], errors='coerce')
            df = df.dropna(how='all')
            
            st.session_state.df = df
            st.success("✅ Data loaded successfully!")
            
        except Exception as e:
            st.error(f"Error loading file: {str(e)}")
    
    if 'df' not in st.session_state:
        return st.warning("Please upload a crosstab Excel file")
    
    df = st.session_state.df
    
    # Generate professional analysis
    analysis = analyze_crosstabs(df)
    
    # Display report
    st.header("Professional Analysis Report")
    
    with st.expander("📌 Overview", expanded=True):
        st.write("""
        This analysis examines crosstabulated survey data from property management professionals.
        The data reveals key operational patterns and demographic distributions across different
        property types and management roles.
        """)
    
    with st.expander("👥 Respondent Demographics"):
        for item in analysis['demographics']:
            st.write(item)
    
    with st.expander("🏢 Operational Metrics"):
        for item in analysis['operations']:
            st.write(item)
    
    with st.expander("🔍 Significant Findings (p<0.05)"):
        if analysis['findings']:
            for i, finding in enumerate(analysis['findings'], 1):
                st.write(f"{i}. {finding}")
        else:
            st.warning("No significant correlations found in this dataset")
    
    with st.expander("💡 Recommendations"):
        if analysis['recommendations']:
            for i, rec in enumerate(analysis['recommendations'], 1):
                st.write(f"{i}. {rec}")
        else:
            st.info("Upload more detailed data for specific recommendations")
    
    # Data explorer
    st.header("Data Explorer")
    col1, col2 = st.columns(2)
    with col1:
        st.subheader("Raw Data Preview")
        st.dataframe(df.head())
    with col2:
        st.subheader("Column Summary")
        for col in df.columns:
            if pd.api.types.is_numeric_dtype(df[col]):
                st.write(f"**{clean_column_name(col)}**: Mean={df[col].mean():.2f} (Range: {df[col].min():.2f}-{df[col].max():.2f})")
    
    # Export report
    st.header("Export Options")
    report_text = "\n\n".join([
        "## Professional Analysis Report",
        "### Overview\n" + analysis['overview'],
        "### Respondent Demographics\n" + "\n".join(analysis['demographics']),
        "### Operational Metrics\n" + "\n".join(analysis['operations']),
        "### Significant Findings\n" + "\n".join(analysis['findings']),
        "### Recommendations\n" + "\n".join(analysis['recommendations'])
    ])
    
    st.download_button(
        "Download Report (DOCX)",
        data=report_text,
        file_name="crosstab_analysis_report.md",
        mime="text/markdown"
    )

if __name__ == "__main__":
    main()
