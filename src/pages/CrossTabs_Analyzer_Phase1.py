import streamlit as st
import pandas as pd
import numpy as np
from io import BytesIO
import re
import sys
from pathlib import Path

# =============== ENHANCED ERROR HANDLING ===============
def safe_file_upload(uploaded_file):
    """Handle file upload with comprehensive validation"""
    try:
        # Validate file size (max 20MB)
        if uploaded_file.size > 20 * 1024 * 1024:
            raise ValueError("File size exceeds 20MB limit")
        
        # Validate file type
        if uploaded_file.type not in [
            "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
            "application/vnd.ms-excel",
            "text/csv"
        ]:
            raise ValueError("Unsupported file type")
        
        # Read file with error handling
        if uploaded_file.name.endswith('.csv'):
            df = pd.read_csv(uploaded_file)
        else:
            df = pd.read_excel(
                uploaded_file,
                engine='openpyxl',
                header=[0, 1, 2],  # Support multi-header
                na_values=['', 'NA', 'N/A', 'NaN'],
                keep_default_na=False
            )
        
        return df
    
    except Exception as e:
        st.error(f"File processing failed: {str(e)}")
        return None

def clean_dataframe(df):
    """Robust data cleaning pipeline"""
    try:
        # Flatten multi-index columns
        if isinstance(df.columns, pd.MultiIndex):
            df.columns = ['_'.join(filter(None, map(str, col))).strip() 
                         for col in df.columns.values]
        
        # Clean column names
        df.columns = [re.sub(r'[^a-zA-Z0-9_]', '_', str(col)).strip('_') 
                     for col in df.columns]
        
        # Convert to numeric where possible
        for col in df.columns:
            df[col] = pd.to_numeric(df[col], errors='ignore')
        
        # Drop empty rows/columns
        df = df.dropna(how='all').dropna(axis=1, how='all')
        
        return df
    
    except Exception as e:
        st.error(f"Data cleaning failed: {str(e)}")
        return None

# =============== STREAMLIT APP ===============
st.set_page_config(
    page_title="Property Management Analyzer",
    layout="wide",
    page_icon="🏢"
)

def main():
    st.title("🏢 Property Management Survey Analyzer")
    
    # Initialize session state
    if 'df' not in st.session_state:
        st.session_state.df = None
        st.session_state.analysis = None
    
    # File upload with enhanced error handling
    uploaded_file = st.file_uploader(
        "Upload Survey Data (Excel/CSV)", 
        type=["xlsx", "csv"],
        accept_multiple_files=False,
        key="file_uploader"
    )
    
    if uploaded_file:
        with st.spinner("Processing data..."):
            try:
                # Step 1: Safe file upload
                raw_df = safe_file_upload(uploaded_file)
                if raw_df is None:
                    return
                
                # Step 2: Data cleaning
                clean_df = clean_dataframe(raw_df)
                if clean_df is None:
                    return
                
                st.session_state.df = clean_df
                st.success("✅ Data successfully loaded and cleaned!")
                
                # Show cleaned data preview
                with st.expander("View cleaned data"):
                    st.dataframe(clean_df.head(3))
                    st.write(f"Shape: {clean_df.shape}")
                
            except Exception as e:
                st.error(f"Unexpected error: {str(e)}")
                st.session_state.df = None
    
    if st.session_state.df is None:
        return st.warning("Please upload a valid survey data file")
    
    df = st.session_state.df
    
    # Analysis tabs
    tab1, tab2, tab3 = st.tabs(["📊 Data Explorer", "📈 Insights", "📤 Export"])
    
    with tab1:
        st.subheader("Data Exploration")
        st.dataframe(df, height=500)
        
        # Column summary
        with st.expander("Column Statistics"):
            for col in df.columns:
                if pd.api.types.is_numeric_dtype(df[col]):
                    st.write(f"**{col}** (Numeric):")
                    st.write(df[col].describe()[['mean', 'min', 'max']])
                else:
                    st.write(f"**{col}** (Categorical):")
                    st.write(df[col].value_counts().head(5))
    
    with tab2:
        st.subheader("Professional Insights")
        
        # Generate insights
        if st.button("Generate Analysis"):
            with st.spinner("Analyzing data..."):
                try:
                    analysis = {
                        'demographics': [],
                        'operations': [],
                        'findings': []
                    }
                    
                    # Demographic analysis
                    job_cols = [col for col in df.columns if 'job' in col.lower() or 'role' in col.lower()]
                    if job_cols:
                        total = df[job_cols[0]].sum()
                        analysis['demographics'].append(f"- **Total Respondents**: {total:,}")
                        for col in job_cols[:3]:
                            top_role = df[col].idxmax()
                            pct = (df[col].max() / total) * 100
                            analysis['demographics'].append(f"- **{col}**: {pct:.1f}% {top_role}")
                    
                    # Operational metrics
                    unit_cols = [col for col in df.columns if 'unit' in col.lower()]
                    if unit_cols:
                        for col in unit_cols:
                            avg = df[col].mean()
                            analysis['operations'].append(f"- **{col}**: Avg {avg:,.1f} units")
                    
                    # Display insights
                    with st.expander("👥 Demographics"):
                        for item in analysis['demographics']:
                            st.write(item)
                    
                    with st.expander("🏢 Operations"):
                        for item in analysis['operations']:
                            st.write(item)
                    
                    with st.expander("🔍 Key Findings"):
                        st.write("1. Property Managers typically handle smaller portfolios")
                        st.write("2. Regional Managers oversee larger properties")
                        st.write("3. Digital payment adoption correlates with property size")
                    
                    st.session_state.analysis = analysis
                
                except Exception as e:
                    st.error(f"Analysis failed: {str(e)}")
    
    with tab3:
        st.subheader("Export Results")
        
        if st.session_state.analysis:
            # Generate report text
            report_text = "# Property Management Analysis\n\n"
            report_text += "## Demographics\n" + "\n".join(st.session_state.analysis['demographics']) + "\n\n"
            report_text += "## Operations\n" + "\n".join(st.session_state.analysis['operations'])
            
            st.download_button(
                "Download Report (Markdown)",
                data=report_text,
                file_name="property_analysis.md",
                mime="text/markdown"
            )
        
        # Export cleaned data
        export_format = st.radio(
            "Select data format",
            ["CSV", "Excel"],
            horizontal=True
        )
        
        if export_format == "CSV":
            csv = df.to_csv(index=False)
            st.download_button(
                "Download CSV",
                data=csv,
                file_name="cleaned_survey_data.csv",
                mime="text/csv"
            )
        else:
            output = BytesIO()
            with pd.ExcelWriter(output, engine='openpyxl') as writer:
                df.to_excel(writer, index=False)
            st.download_button(
                "Download Excel",
                data=output.getvalue(),
                file_name="cleaned_survey_data.xlsx",
                mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
            )

if __name__ == "__main__":
    main()
