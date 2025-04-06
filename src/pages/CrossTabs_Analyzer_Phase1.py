import streamlit as st
import pandas as pd
import numpy as np
from io import BytesIO

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
        
        # Clean and convert numeric data
        def convert_to_numeric(val):
            if isinstance(val, str):
                val = re.sub(r'[^\d.]', '', val)
                try:
                    return float(val) if val else np.nan
                except:
                    return val
            return val

        # Clean multi-index columns
        df.columns = [
            ' | '.join(filter(None, (str(c).strip() for c in col)))
            for col in df.columns.values
        ]

        # Convert numeric columns
        for col in df.columns:
            df[col] = df[col].apply(convert_to_numeric)
            if pd.api.types.is_numeric_dtype(df[col]):
                df[col] = pd.to_numeric(df[col], errors='coerce')
        
        return df.dropna(how='all').dropna(axis=1, how='all')
    
    except Exception as e:
        st.error(f"Parsing failed: {str(e)}")
        return None

class WinCrossAnalysis:
    @staticmethod
    def clean_data(df):
        """Remove non-data rows and extract numeric data"""
        if df is None:
            return None
            
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
        
        # Convert percentage strings
        for col in clean_df.columns:
            if clean_df[col].dtype == object:
                clean_df[col] = clean_df[col].apply(
                    lambda x: float(re.sub(r'[^\d.]', '', str(x))) 
                    if re.search(r'\d', str(x)) else np.nan
                )
        
        return clean_df

    @staticmethod
    def generate_insights(df):
        """Enhanced insight generation for WinCross data"""
        if df is None or len(df) == 0:
            return []
            
        clean_df = WinCrossAnalysis.clean_data(df)
        insights = []
        
        # Find all numeric columns
        numeric_cols = clean_df.select_dtypes(include=np.number).columns
        
        if len(numeric_cols) == 0:
            return ["No numeric data found for analysis"]
        
        # Analyze each numeric column
        for col in numeric_cols[:10]:  # Limit to first 10 columns
            col_parts = col.split(' | ')
            question = col_parts[0] if len(col_parts) > 0 else "Data"
            response = col_parts[1] if len(col_parts) > 1 else "Value"
            
            col_data = clean_df[col].dropna()
            if len(col_data) > 0:
                insights.append(
                    f"📈 {question} - {response}: "
                    f"Avg={col_data.mean():.1f}, "
                    f"Min={col_data.min():.1f}, "
                    f"Max={col_data.max():.1f}"
                )
        
        # Add summary stats
        if insights:
            insights.insert(0, "🔍 Key Findings from WinCross Data:")
        
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

if uploaded_file and st.session_state.df is None:
    with st.spinner("Processing WinCross file..."):
        df = parse_wincross(uploaded_file)
        if df is not None and len(df) > MIN_DATA_ROWS:
            st.session_state.df = df
            st.session_state.clean_df = WinCrossAnalysis.clean_data(df)
            st.success("✅ File loaded successfully!")
            st.session_state.enable_insights = True
        else:
            st.error("Failed to load valid data from file")

# Analysis Tabs
if st.session_state.df is not None:
    tab1, tab2, tab3 = st.tabs(["Data Overview", "Advanced Analysis", "Export"])
    
    with tab1:
        st.subheader("Data Structure")
        st.write(f"Rows: {len(st.session_state.df)} | Columns: {len(st.session_state.df.columns)}")
        st.write("Numeric Columns:", len(st.session_state.clean_df.select_dtypes(include=np.number).columns))
        st.dataframe(st.session_state.df.head(3))
    
    with tab2:
        st.subheader("Advanced Analysis")
        if st.button("Generate Insights", disabled=not st.session_state.enable_insights):
            insights = WinCrossAnalysis.generate_insights(st.session_state.df)
            if not insights:
                st.warning("No numeric data found for analysis")
            else:
                for insight in insights:
                    st.success(insect)
    
    with tab3:
        st.subheader("Export Results")
        if st.session_state.clean_df is not None:
            csv = st.session_state.clean_df.to_csv(index=False)
            st.download_button(
                "Download CSV",
                csv,
                "wincross_data.csv",
                "text/csv"
            )

# Debug
with st.expander("Technical Details"):
    if st.session_state.df is not None:
        st.write("Sample Numeric Columns:", 
               st.session_state.clean_df.select_dtypes(include=np.number).columns.tolist()[:5])
