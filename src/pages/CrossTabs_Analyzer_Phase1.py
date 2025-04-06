iimport streamlit as st
import pandas as pd
import numpy as np
from io import BytesIO
import re

# ==============================================
# WinCross Parser Configuration
# ==============================================
WINCROSS_HEADER_DEPTH = 3  # Number of header rows in WinCross files
MIN_DATA_ROWS = 5  # Minimum valid data rows to consider

# ==============================================
# Enhanced WinCross Parser
# ==============================================
def parse_wincross(file):
    """Specialized parser for WinCross crosstab format"""
    try:
        # Read raw data to find header structure
        raw_df = pd.read_excel(file, header=None)
        
        # Find the first non-empty row (header start)
        header_start = 0
        for i, row in raw_df.iterrows():
            if row.notna().any():
                header_start = i
                break
        
        # Read with proper headers
        df = pd.read_excel(
            file,
            header=list(range(header_start, header_start + WINCROSS_HEADER_DEPTH)),
            skiprows=range(header_start)
        )
        
        # Clean multi-index columns
        df.columns = [
            ' | '.join([str(c).strip() for c in col if str(c).strip() != 'nan'])
            for col in df.columns.values
        ]
        
        # Remove completely empty rows and columns
        df = df.dropna(how='all').dropna(axis=1, how='all')
        
        # Convert percentage/numeric strings
        for col in df.columns:
            if df[col].dtype == object:
                # Clean numeric strings
                df[col] = df[col].apply(
                    lambda x: pd.to_numeric(re.sub(r'[^\d.]+', '', str(x)), errors='ignore')
                    if isinstance(x, str) else x
                )
        
        return df
    
    except Exception as e:
        st.error(f"Failed to parse WinCross file: {str(e)}")
        return None

# ==============================================
# WinCross Analysis Engine
# ==============================================
class WinCrossAnalyzer:
    @staticmethod
    def is_data_row(row):
        """Identify actual data rows (not headers/footnotes)"""
        return not any(x in str(row).lower() for x in ['banner', 'footnote', 'base', 'sig-testing'])

    @staticmethod
    def clean_dataframe(df):
        """Extract just the data rows from WinCross output"""
        # Identify data rows
        mask = df.apply(WinCrossAnalyzer.is_data_row, axis=1)
        return df[mask].reset_index(drop=True)

    @staticmethod
    def extract_question_response(col_name):
        """Parse WinCross column names into components"""
        parts = col_name.split(' | ')
        return {
            'question': parts[0] if len(parts) > 0 else '',
            'response': parts[1] if len(parts) > 1 else '',
            'statistic': parts[2] if len(parts) > 2 else ''
        }

    @staticmethod
    def generate_insights(df):
        """WinCross-specific insights"""
        insights = []
        clean_df = WinCrossAnalyzer.clean_dataframe(df)
        
        # Numeric analysis
        numeric_cols = clean_df.select_dtypes(include=np.number).columns
        for col in numeric_cols[:5]:  # Limit to first 5 for demo
            col_info = WinCrossAnalyzer.extract_question_response(col)
            insights.append(
                f"📊 {col_info['question']} ({col_info['response']}): "
                f"Avg = {clean_df[col].mean():.2f}, "
                f"Range = {clean_df[col].min():.2f}-{clean_df[col].max():.2f}"
            )
        
        return insights

# ==============================================
# Streamlit UI Setup
# ==============================================
st.set_page_config(page_title="WinCross Professional", layout="wide")
st.title("🔍 WinCross Professional Analyzer")

# Initialize session state
if 'df' not in st.session_state:
    st.session_state.df = None
    st.session_state.clean_df = None

# ==============================================
# File Upload Section
# ==============================================
uploaded_file = st.file_uploader(
    "Upload WinCross Crosstab", 
    type=["xlsx", "xls"],
    help="Standard WinCross export files only"
)

if uploaded_file and st.session_state.df is None:
    with st.spinner("Parsing WinCross file..."):
        df = parse_wincross(uploaded_file)
        if df is not None and len(df) > MIN_DATA_ROWS:
            st.session_state.df = df
            st.session_state.clean_df = WinCrossAnalyzer.clean_dataframe(df)
            st.success(f"✅ Successfully parsed {len(df)} rows")

# ==============================================
# Analysis Tabs
# ==============================================
tab1, tab2, tab3 = st.tabs(["Data Overview", "Advanced Analysis", "Export"])

if st.session_state.df is not None:
    df = st.session_state.df
    clean_df = st.session_state.clean_df

    with tab1:
        st.subheader("Data Structure")
        st.write(f"Raw rows: {len(df)} | Clean rows: {len(clean_df)} | Columns: {len(df.columns)}")
        
        col1, col2 = st.columns(2)
        with col1:
            st.metric("Numeric Columns", len(clean_df.select_dtypes(include=np.number).columns))
        with col2:
            st.metric("Text Columns", len(clean_df.select_dtypes(include='object').columns))
        
        selected_col = st.selectbox("Inspect Column", df.columns)
        st.write("Sample values:", df[selected_col].head(10))

    with tab2:
        st.subheader("Advanced Analysis")
        
        if st.button("Generate Insights", key="insights_btn"):
            insights = WinCrossAnalyzer.generate_insights(df)
            for insight in insights:
                st.success(insight)
        
        st.write("Clean Data Preview (first 10 rows):")
        st.dataframe(clean_df.head(10))

    with tab3:
        st.subheader("Export Results")
        export_format = st.radio("Format", ["CSV", "Excel"], horizontal=True)
        
        if export_format == "CSV":
            st.download_button(
                "Download CSV",
                clean_df.to_csv(index=False),
                "wincross_clean_data.csv",
                "text/csv"
            )
        else:
            output = BytesIO()
            with pd.ExcelWriter(output, engine='openpyxl') as writer:
                clean_df.to_excel(writer, index=False, sheet_name="CleanData")
                df.to_excel(writer, index=False, sheet_name="RawData")
            st.download_button(
                "Download Excel",
                output.getvalue(),
                "wincross_analysis.xlsx",
                "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
            )

else:
    st.warning("Please upload a WinCross crosstab file")

# ==============================================
# Debug Section
# ==============================================
with st.expander("Technical Details"):
    st.write("Session State:", {k: v for k, v in st.session_state.items() if k != 'df'})
    if st.session_state.df is not None:
        st.write("Column Examples:", df.columns.tolist()[:5])
        st.write("Data Types:", clean_df.dtypes.value_counts())
