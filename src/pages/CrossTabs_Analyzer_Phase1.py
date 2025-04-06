import streamlit as st
import pandas as pd
import numpy as np
import re
from io import BytesIO

# Initialize session state
if 'df' not in st.session_state:
    st.session_state.update({
        'df': None,
        'clean_df': None,
        'numeric_cols': []
    })

# WinCross Configuration
WINCROSS_HEADER_DEPTH = 3
MIN_DATA_ROWS = 5

def parse_wincross(file):
    """Enhanced WinCross parser with numeric conversion"""
    try:
        # Read with no headers to find structure
        raw_df = pd.read_excel(file, header=None)
        
        # Find first non-empty row
        header_start = next(i for i, row in raw_df.iterrows() if row.notna().any())
        
        # Read with proper headers
        df = pd.read_excel(
            file,
            header=list(range(header_start, header_start + WINCROSS_HEADER_DEPTH)),
            skiprows=list(range(header_start))
        )
        
        # Clean multi-index columns
        df.columns = [
            ' | '.join(filter(None, (str(c).strip() for c in col)))
            for col in df.columns.values
        ]
        
        # Convert all potential numeric columns
        for col in df.columns:
            # Handle percentage signs and other non-numeric characters
            df[col] = df[col].apply(
                lambda x: pd.to_numeric(re.sub(r'[^\d.]', '', str(x)), errors='coerce')
                if isinstance(x, str) else x
            )
            
            # Final conversion to numeric
            if pd.api.types.is_numeric_dtype(df[col]):
                df[col] = pd.to_numeric(df[col], errors='coerce')
        
        return df.dropna(how='all').drop  (axis=1, how='all')
    
    except Exception as e:
        st.error(f"Parsing failed: {str(e)}")
        return None

def clean_data(df):
    """Remove non-data rows and identify numeric columns"""
    if df is None:
        return None, []
    
    # Filter out metadata rows
    clean_df = df[
        ~df.apply(
            lambda r: any(
                x in str(r).lower() 
                for x in ['banner', 'footnote', 'base', 'sig-testing', 'total']
            ),
            axis=1
        )
    ].reset_index(drop=True)
    
    # Identify numeric columns
    numeric_cols = [
        col for col in clean_df.columns 
        if pd.api.types.is_numeric_dtype(clean_df[col])
    ]
    
    return clean_df, numeric_cols

# Streamlit UI
st.set_page_config(page_title="WinCross Analyzer Pro", layout="wide")
st.title("📊 WinCross Professional Analyzer")

# File Upload
uploaded_file = st.file_uploader(
    "Upload WinCross File", 
    type=["xlsx", "xls"],
    help="Standard WinCross export files"
)

if uploaded_file and st.session_state.df is None:
    with st.spinner("Processing WinCross file..."):
        df = parse_wincross(uploaded_file)
        if df is not None and len(df) > MIN_DATA_ROWS:
            clean_df, numeric_cols = clean_data(df)
            st.session_state.df = df
            st.session_state.clean_df = clean_df
            st.session_state.numeric_cols = numeric_cols
            st.success(f"✅ File loaded with {len(numeric_cols)} numeric columns")
        else:
            st.error("Failed to load valid data from file")

# Analysis Tabs
if st.session_state.df is not None:
    tab1, tab2 = st.tabs(["Data Overview", "Advanced Analysis"])
    
    with tab1:
        st.subheader("Data Structure")
        st.write(f"Total Rows: {len(st.session_state.df)}")
        st.write(f"Numeric Columns: {len(st.session_state.numeric_cols)}")
        st.write("Sample Numeric Columns:", st.session_state.numeric_cols[:5])
        st.dataframe(st.session_state.df.head(3))
    
    with tab2:
        st.subheader("Statistical Analysis")
        
        if not st.session_state.numeric_cols:
            st.warning("No numeric columns detected - cannot generate insights")
            st.info("""
            Common reasons:
            1. Data contains percentages as text (e.g., '25%')
            2. Numbers have special formatting
            3. File uses non-standard structure
            """)
        else:
            selected_col = st.selectbox(
                "Select numeric column to analyze",
                st.session_state.numeric_cols
            )
            
            col_data = st.session_state.clean_df[selected_col].dropna()
            if len(col_data) > 0:
                st.metric("Average", f"{col_data.mean():.2f}")
                st.metric("Minimum", f"{col_data.min():.2f}")
                st.metric("Maximum", f"{col_data.max():.2f}")
                
                # Basic histogram
                st.bar_chart(col_data.value_counts().sort_index())
            else:
                st.warning("Selected column contains no numeric data")

# Debug
with st.expander("Technical Details"):
    if st.session_state.df is not None:
        st.write("All Columns:", st.session_state.df.columns.tolist())
        st.write("Numeric Columns:", st.session_state.numeric_cols)
        st.write("Data Types:", st.session_state.clean_df.dtypes.value_counts())
