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
        'numeric_cols': [],
        'conversion_issues': []
    })

def clean_column_name(name):
    """Clean WinCross column names for visualization compatibility"""
    # Remove problematic characters and spaces
    name = re.sub(r'[^a-zA-Z0-9_]', '_', str(name))
    # Remove leading/trailing underscores
    name = name.strip('_')
    # Ensure it doesn't start with number
    if name and name[0].isdigit():
        name = f'col_{name}'
    return name

def parse_wincross(file):
    """Advanced WinCross parser with robust numeric conversion"""
    try:
        # First pass to detect header structure
        raw_df = pd.read_excel(file, header=None, nrows=20)
        header_start = next(i for i, row in raw_df.iterrows() if row.notna().any())
        
        # Read with proper headers
        df = pd.read_excel(
            file,
            header=list(range(header_start, header_start + 3)),
            skiprows=list(range(header_start))
        )
        
        # Clean column names for visualization compatibility
        df.columns = [
            clean_column_name('_'.join(filter(None, (str(c).strip() for c in col))))
            for col in df.columns.values
        ]
        
        return df.dropna(how='all').dropna(axis=1, how='all')
    except Exception as e:
        st.error(f"File parsing error: {str(e)}")
        return None

def convert_to_numeric(series):
    """Convert a series to numeric, handling WinCross formats"""
    conversion_issues = []
    
    def converter(x):
        if pd.isna(x):
            return np.nan
        try:
            # Handle percentages (25% → 0.25)
            if isinstance(x, str) and '%' in x:
                return float(re.sub(r'[^\d.]', '', x)) / 100
            # Handle comma numbers (1,000 → 1000)
            if isinstance(x, str) and ',' in x:
                return float(re.sub(r'[^\d.]', '', x))
            return float(x)
        except Exception as e:
            conversion_issues.append(f"Couldn't convert {x}: {str(e)}")
            return np.nan
    
    numeric_series = series.apply(converter)
    return numeric_series, conversion_issues

def analyze_data(df):
    """Identify and convert numeric columns"""
    if df is None:
        return None, [], []
    
    numeric_cols = []
    all_conversion_issues = []
    clean_df = df.copy()
    
    for col in clean_df.columns:
        # Skip obvious non-numeric columns
        if (clean_df[col].dtype == object and 
            not any(char.isdigit() for char in clean_df[col].astype(str).str.cat())):
            continue
            
        numeric_series, issues = convert_to_numeric(clean_df[col])
        if numeric_series.notna().any():  # If we got any numeric values
            clean_df[col] = numeric_series
            numeric_cols.append(col)
        all_conversion_issues.extend(issues)
    
    return clean_df, numeric_cols, all_conversion_issues

# Streamlit UI
st.set_page_config(page_title="WinCross Analyzer Pro", layout="wide")
st.title("🔍 WinCross Data Analyzer")

# File Upload
uploaded_file = st.file_uploader(
    "Upload WinCross Crosstab", 
    type=["xlsx", "xls"],
    help="Upload standard WinCross export files"
)

if uploaded_file and st.session_state.df is None:
    with st.spinner("Analyzing WinCross file..."):
        df = parse_wincross(uploaded_file)
        if df is not None:
            clean_df, numeric_cols, issues = analyze_data(df)
            st.session_state.df = df
            st.session_state.clean_df = clean_df
            st.session_state.numeric_cols = numeric_cols
            st.session_state.conversion_issues = issues
            
            if numeric_cols:
                st.success(f"✅ Found {len(numeric_cols)} numeric columns")
            else:
                st.warning("⚠️ No numeric columns detected")

# Analysis Tabs
if st.session_state.df is not None:
    tab1, tab2, tab3 = st.tabs(["Data Overview", "Numeric Analysis", "Debug"])
    
    with tab1:
        st.subheader("Raw Data Structure")
        st.write(f"Total Rows: {len(st.session_state.df)}")
        st.write(f"Total Columns: {len(st.session_state.df.columns)}")
        st.dataframe(st.session_state.df.head(3))
    
    with tab2:
        st.subheader("Numeric Data Analysis")
        
        if not st.session_state.numeric_cols:
            st.error("No numeric columns found in the data")
            st.markdown("""
            **Common Reasons:**
            - Numbers stored as text (e.g., '25%', '1,000')
            - Non-standard numeric formats
            - Data contains mostly text responses
            
            **Try:**
            1. Check your WinCross export settings
            2. Export as plain numbers without formatting
            3. Verify your data contains numeric values
            """)
        else:
            selected_col = st.selectbox(
                "Select numeric column to analyze", 
                st.session_state.numeric_cols
            )
            
            col_data = st.session_state.clean_df[selected_col].dropna()
            if len(col_data) > 0:
                col1, col2, col3 = st.columns(3)
                with col1:
                    st.metric("Average", f"{col_data.mean():.2f}")
                with col2:
                    st.metric("Minimum", f"{col_data.min():.2f}")
                with col3:
                    st.metric("Maximum", f"{col_data.max():.2f}")
                
                # Create a simple bar chart with clean data
                try:
                    chart_df = pd.DataFrame({
                        'value': col_data,
                        'index': range(len(col_data))
                    })
                    st.bar_chart(chart_df.set_index('index')['value'])
                except Exception as e:
                    st.warning(f"Could not display chart: {str(e)}")
            else:
                st.warning("Selected column contains no valid numeric data")
    
    with tab3:
        st.subheader("Diagnostic Information")
        st.write("All Columns:", st.session_state.df.columns.tolist())
        st.write("Numeric Columns:", st.session_state.numeric_cols)
        st.write("Conversion Issues:", st.session_state.conversion_issues)
        st.write("Sample Values:", st.session_state.df.iloc[:, :5].head(3).to_dict())

else:
    st.info("Please upload a WinCross crosstab file to begin analysis")
