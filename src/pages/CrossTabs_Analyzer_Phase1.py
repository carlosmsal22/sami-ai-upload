import streamlit as st
import pandas as pd
import sys
from pathlib import Path
import os

# ========== CLOUD PATH FIX ==========
# Special handling for Render's file system
def get_base_path():
    """Get absolute path to base directory"""
    if 'RENDER' in os.environ:
        return Path('/opt/render/project/src')
    return Path(__file__).parent.parent

sys.path.append(str(get_base_path()))

# ========== IMPORTS WITH CLOUD FALLBACK ==========
try:
    from utils.stats_helpers import run_group_comparison, run_z_chi_tests, get_descriptive_stats
    st.session_state.utils_loaded = True
except ImportError as e:
    st.error(f"""
    ❌ Cloud Import Error: {str(e)}
    Please verify:
    1. utils/stats_helpers.py exists in your repo
    2. All functions are properly defined
    3. Render service has rebuilt after changes
    """)
    st.stop()

# ========== STREAMLIT CONFIG ==========
st.set_page_config(
    page_title="Cloud CrossTabs Analyzer",
    layout="wide",
    menu_items={
        'Get Help': 'https://your-docs-link.com',
        'Report a bug': "https://your-support-link.com"
    }
)

# ========== CLOUD-OPTIMIZED TAB RENDERING ==========
def render_tabs(df):
    """Cloud-optimized tab rendering"""
    tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs([
        "📊 Frequency", "🔍 Groups", "🧪 Stats",
        "📈 Analytics", "💡 Insights", "📤 Export"
    ])
    
    with tab1:
        st.subheader("Frequency Tables")
        st.dataframe(df)
        
    with tab2:
        st.subheader("Group Comparisons")
        col1, col2 = st.columns(2)
        with col1:
            group1 = st.selectbox("Group 1", df.columns)
        with col2:
            group2 = st.selectbox("Group 2", df.columns)
        if st.button("Compare"):
            st.dataframe(run_group_comparison(df, group1, group2))
    
    # Add other tabs following same pattern...

# ========== CLOUD FILE HANDLER ==========
def handle_upload():
    """Special handling for cloud file uploads"""
    uploaded_file = st.file_uploader("Upload Excel", type=["xlsx", "xls"])
    if uploaded_file:
        try:
            # Read with explicit engine for cloud compatibility
            return pd.read_excel(
                uploaded_file,
                header=[0, 1, 2],
                engine='openpyxl'
            )
        except Exception as e:
            st.error(f"Cloud upload error: {str(e)}")
            return None

# ========== MAIN APP ==========
def main():
    st.title("📊 Cloud CrossTabs Analyzer")
    
    if 'df' not in st.session_state:
        st.session_state.df = None
    
    # Cloud-optimized file handling
    new_df = handle_upload()
    if new_df is not None:
        st.session_state.df = new_df
    
    if st.session_state.df is not None:
        render_tabs(st.session_state.df)
    else:
        st.warning("Please upload data file to begin analysis")

if __name__ == "__main__":
    main()
