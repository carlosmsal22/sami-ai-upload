import streamlit as st
import pandas as pd
import numpy as np
import sys
from pathlib import Path
from io import BytesIO
import matplotlib.pyplot as plt

# ==============================================
# WinCross-Specific Configuration
# ==============================================
WINCROSS_HEADER_ROWS = 3  # Typical WinCross header depth
MIN_DATA_ROWS = 5  # Minimum rows to consider valid data

# ==============================================
# Session State Initialization
# ==============================================
if 'df' not in st.session_state:
    st.session_state.update({
        'enable_insights': False,
        'enable_enhanced_stats': False,
        'df': None,
        'original_columns': None
    })

# ==============================================
# Enhanced WinCross Parser
# ==============================================
def parse_wincross(file):
    """Specialized parser for WinCross crosstab format"""
    try:
        # First pass to detect header structure
        temp_df = pd.read_excel(file, header=None, nrows=20)
        
        # Find the first non-empty row for headers
        header_start = 0
        for i, row in temp_df.iterrows():
            if row.notna().any():
                header_start = i
                break
        
        # Read with dynamic header rows
        df = pd.read_excel(
            file,
            header=list(range(header_start, header_start + WINCROSS_HEADER_ROWS)),
            skiprows=range(header_start)  # Skip empty rows above headers
        )
        
        # Clean multi-index columns
        df.columns = [
            ' | '.join(filter(None, map(str, col))).strip()
            for col in df.columns.values
        ]
        
        # Remove completely empty rows
        df = df.dropna(how='all')
        
        # Remove completely empty columns
        df = df.dropna(axis=1, how='all')
        
        # Convert percentage strings to numeric
        for col in df.columns:
            if df[col].dtype == object:
                df[col] = df[col].replace(r'[%\$,]', '', regex=True)
                try:
                    df[col] = pd.to_numeric(df[col])
                except:
                    pass
        
        return df
    
    except Exception as e:
        st.error(f"Failed to parse WinCross file: {str(e)}")
        return None

# ==============================================
# WinCross Analysis Engine
# ==============================================
class WinCrossAnalysis:
    @staticmethod
    def split_column_name(full_name):
        """Extract components from WinCross column names"""
        parts = full_name.split(' | ')
        return {
            'question': parts[0] if len(parts) > 0 else '',
            'response': parts[1] if len(parts) > 1 else '',
            'statistic': parts[2] if len(parts) > 2 else ''
        }

    @staticmethod
    def descriptive_stats(df):
        """WinCross-optimized stats"""
        stats = {}
        for col in df.columns:
            if pd.api.types.is_numeric_dtype(df[col]):
                stats[col] = {
                    'mean': df[col].mean(),
                    'median': df[col].median(),
                    'min': df[col].min(),
                    'max': df[col].max()
                }
        return stats

    @staticmethod
    def generate_insights(df):
        """WinCross-specific insights"""
        insights = []
        numeric_cols = df.select_dtypes(include=np.number).columns
        
        for col in numeric_cols:
            col_parts = WinCrossAnalysis.split_column_name(col)
            if 'sig' in col_parts['statistic'].lower():
                sig_values = df[col].dropna()
                if len(sig_values) > 0:
                    max_sig = sig_values.max()
                    if max_sig < 0.05:
                        insights.append(
                            f"🔴 Significant finding in {col_parts['question']} "
                            f"(p < {max_sig:.3f})"
                        )
        
        # Add basic stats for numeric columns
        for col in numeric_cols[:5]:  # Limit to top 5 for brevity
            col_parts = WinCrossAnalysis.split_column_name(col)
            insights.append(
                f"📊 {col_parts['question']} ({col_parts['response']}): "
                f"Avg = {df[col].mean():.2f}"
            )
        
        return insights

# ==============================================
# Streamlit UI Setup
# ==============================================
st.set_page_config(page_title="WinCross Analyzer", layout="wide")
st.title("📊 WinCross Crosstab Analyzer")

# ==============================================
# File Upload Section
# ==============================================
uploaded_file = st.file_uploader(
    "Upload WinCross Crosstab (Excel)", 
    type=["xlsx", "xls"],
    help="Upload standard WinCross export files"
)

if uploaded_file:
    with st.spinner("Parsing WinCross file..."):
        df = parse_wincross(uploaded_file)
        if df is not None and len(df) > MIN_DATA_ROWS:
            st.session_state.df = df
            st.success(f"✅ Loaded {len(df)} rows with {len(df.columns)} columns")
            
            with st.expander("🔍 Data Preview"):
                st.dataframe(df.head(3))
                st.write("Column examples:", df.columns.tolist()[:5])

# ==============================================
# Analysis Tabs
# ==============================================
tabs = st.tabs([
    "📋 Data Overview", 
    "📊 Basic Analysis", 
    "🧪 Statistical Tests",
    "💡 Insights",
    "📤 Export"
])

if st.session_state.df is not None:
    df = st.session_state.df
    
    # Tab 1: Data Overview
    with tabs[0]:
        st.subheader("Data Structure")
        st.write(f"Total rows: {len(df)} | Columns: {len(df.columns)}")
        
        col1, col2 = st.columns(2)
        with col1:
            st.metric("Numeric Columns", 
                     len(df.select_dtypes(include=np.number).columns))
        with col2:
            st.metric("Text Columns",
                     len(df.select_dtypes(include='object').columns))
        
        selected_col = st.selectbox("Inspect Column", df.columns)
        st.write(df[selected_col].describe())

    # Tab 2: Basic Analysis
    with tabs[1]:
        st.subheader("Basic Analysis")
        analysis_type = st.radio(
            "Analysis Type",
            ["Descriptive Stats", "Frequency Tables"],
            horizontal=True
        )
        
        if analysis_type == "Descriptive Stats":
            stats = WinCrossAnalysis.descriptive_stats(df)
            st.json(stats)
        else:
            selected_col = st.selectbox("Select Column", df.columns)
            st.dataframe(df[selected_col].value_counts().head(20))

    # Tab 3: Statistical Tests
    with tabs[2]:
        st.subheader("Statistical Testing")
        st.info("WinCross-specific tests coming soon!")
        # Placeholder for future statistical tests

    # Tab 4: Insights
    with tabs[3]:
        st.subheader("Automated Insights")
        if st.button("Generate Insights"):
            insights = WinCrossAnalysis.generate_insights(df)
            for insight in insights:
                st.success(insight)

    # Tab 5: Export
    with tabs[4]:
        st.subheader("Export Results")
        export_format = st.selectbox("Format", ["CSV", "Excel"])
        
        if export_format == "CSV":
            st.download_button(
                "Download CSV",
                df.to_csv(index=False),
                "wincross_analysis.csv",
                "text/csv"
            )
        else:
            output = BytesIO()
            with pd.ExcelWriter(output, engine='openpyxl') as writer:
                df.to_excel(writer, index=False)
            st.download_button(
                "Download Excel",
                output.getvalue(),
                "wincross_analysis.xlsx",
                "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
            )

else:
    st.warning("Please upload a WinCross crosstab file to begin analysis")

# ==============================================
# Debug Section
# ==============================================
with st.expander("Debug Information"):
    st.write("Session State:", st.session_state)
    if st.session_state.df is not None:
        st.write("Data Types:", st.session_state.df.dtypes.value_counts())
