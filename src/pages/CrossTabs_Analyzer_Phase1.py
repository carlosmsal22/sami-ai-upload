# =============== IMPORTS ===============
import streamlit as st
import pandas as pd
import numpy as np
from io import BytesIO
import sys
from pathlib import Path
import os

# =============== CLOUD PATH CONFIG ===============
def get_base_path():
    """Smart path detection for Render/local"""
    if 'RENDER' in os.environ:
        return Path('/opt/render/project/src')
    return Path(__file__).parent.parent

sys.path.append(str(get_base_path()))

# =============== TYPE FIXER ===============
def fix_column_types(df):
    """Convert mixed-type columns to string to avoid Arrow errors"""
    for col in df.columns:
        if df[col].dtype == object:
            df[col] = df[col].astype(str)
    return df

# =============== FILE LOADER ===============
def load_data(uploaded_file):
    """Robust Excel/CSV loader with type handling"""
    try:
        if uploaded_file.name.endswith('.csv'):
            df = pd.read_csv(uploaded_file)
        else:
            df = pd.read_excel(
                uploaded_file,
                engine='openpyxl',
                header=[0, 1, 2],  # Supports multi-index
                dtype=str  # Force string initially
            )
            # Convert numeric columns back where possible
            for level in range(df.columns.nlevels):
                df.columns = df.columns.set_levels(
                    df.columns.levels[level].astype(str), 
                    level=level
                )
        return fix_column_types(df)
    except Exception as e:
        st.error(f"🚨 Data loading error: {str(e)}")
        return None

# =============== STREAMLIT APP ===============
st.set_page_config(
    page_title="CrossTabs Analyzer",
    layout="wide",
    page_icon="📊"
)

def main():
    st.title("📊 CrossTab Analyzer (Render-Optimized)")

    # File upload with type handling
    uploaded_file = st.file_uploader("Upload Excel/CSV", type=["xlsx", "csv"])
    if uploaded_file:
        with st.spinner("Processing file..."):
            st.session_state.df = load_data(uploaded_file)
    
    if 'df' not in st.session_state or st.session_state.df is None:
        return st.warning("Please upload a file to begin")

    df = st.session_state.df
    
    # Main tabs
    tab1, tab2, tab3 = st.tabs(["📈 Data View", "🔍 Analysis", "📤 Export"])
    
    with tab1:
        st.subheader("Data Preview")
        st.dataframe(df.head(10))
        
    with tab2:
        st.subheader("Statistical Analysis")
        if st.button("Run Basic Stats"):
            st.dataframe(df.describe(include='all'))
    
    with tab3:
        st.subheader("Export Options")
        export_format = st.selectbox("Format", ["CSV", "Excel", "JSON"])
        
        if export_format == "CSV":
            st.download_button(
                "Download CSV",
                data=df.to_csv(index=False),
                file_name="data_export.csv"
            )
        elif export_format == "Excel":
            output = BytesIO()
            with pd.ExcelWriter(output, engine='openpyxl') as writer:
                df.to_excel(writer, index=False)
            st.download_button(
                "Download Excel",
                data=output.getvalue(),
                file_name="data_export.xlsx"
            )

if __name__ == "__main__":
    main()
