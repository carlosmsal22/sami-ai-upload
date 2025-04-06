import streamlit as st
import pandas as pd
import numpy as np
import re
from io import BytesIO
import sys
from pathlib import Path

# Initialize session state
if 'df' not in st.session_state:
    st.session_state.update({
        'enable_insights': False,
        'enable_enhanced_stats': False,
        'df': None,
        'clean_df': None
    })

# WinCross Configuration
WINCROSS_HEADER_DEPTH = 3
MIN_DATA_ROWS = 5

def parse_wincross(file):
    """Parse WinCross crosstab files"""
    try:
        # Read with no headers to find structure
        raw_df = pd.read_excel(file, header=None)
        
        # Find first non-empty row
        header_start = next(
            (i for i, row in raw_df.iterrows() if row.notna().any()), 
            0
        )
        
        # Read with proper headers
        df = pd.read_excel(
            file,
            header=list(range(header_start, header_start + WINCROSS_HEADER_DEPTH)),
            skiprows=range(header_start)
        )
        
        # Clean multi-index columns
        df.columns = [
            ' | '.join(filter(None, (str(c).strip() for c in col)))
            for col in df.columns.values
        ]
        
        return df.dropna(how='all').dropna(axis=1, how='all')
    
    except Exception as e:
        st.error(f"Parsing failed: {str(e)}")
        return None

class WinCrossAnalysis:
    @staticmethod
    def clean_data(df):
        """Remove non-data rows"""
        return df[
            ~df.apply(
                lambda r: any(
                    x in str(r).lower() 
                    for x in ['banner', 'footnote', 'base', 'sig-testing']
                ),
                axis=1
            )
        ].reset_index(drop=True)

    @staticmethod
    def generate_insights(df):
        """Create automated insights"""
        clean_df = WinCrossAnalysis.clean_data(df)
        insights = []
        
        for col in clean_df.select_dtypes(include=np.number).columns[:5]:
            parts = col.split(' | ')
            label = f"{parts[0]} ({parts[1]})" if len(parts) > 1 else col
            insights.append(
                f"📊 {label}: Mean={clean_df[col].mean():.2f}, "
                f"Range={clean_df[col].min():.2f}-{clean_df[col].max():.2f}"
            )
        
        return insights

# Streamlit UI
st.set_page_config(page_title="WinCross Analyzer", layout="wide")
st.title("📊 WinCross Professional Analyzer")

# File Upload
uploaded_file = st.file_uploader(
    "Upload WinCross File", 
    type=["xlsx", "xls"],
    help="Standard WinCross export files"
)

if uploaded_file and not st.session_state.df:
    with st.spinner("Processing..."):
        df = parse_wincross(uploaded_file)
        if df is not None and len(df) > MIN_DATA_ROWS:
            st.session_state.df = df
            st.session_state.clean_df = WinCrossAnalysis.clean_data(df)
            st.success("File loaded successfully!")

# Analysis Tabs
if st.session_state.df:
    tab1, tab2, tab3 = st.tabs(["Overview", "Analysis", "Export"])
    
    with tab1:
        st.subheader("Data Structure")
        st.write(f"Rows: {len(st.session_state.df)} | Columns: {len(st.session_state.df.columns)}")
        st.dataframe(st.session_state.df.head(3))
    
    with tab2:
        st.subheader("Advanced Analysis")
        if st.button("Generate Insights"):
            insights = WinCrossAnalysis.generate_insights(st.session_state.df)
            for insight in insights:
                st.success(insight)
    
    with tab3:
        st.subheader("Export Results")
        if st.download_button(
            "Download CSV",
            st.session_state.clean_df.to_csv(index=False),
            "wincross_data.csv",
            "text/csv"
        ):
            st.success("Export started!")

else:
    st.warning("Please upload a WinCross crosstab file")

# Debug
with st.expander("Session State"):
    st.write({
        k: v for k, v in st.session_state.items() 
        if not isinstance(v, pd.DataFrame)
    })
