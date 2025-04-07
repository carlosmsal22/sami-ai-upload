# MUST BE FIRST - Streamlit page config
st.set_page_config(page_title="🚀 Enhanced CrossTabs Analyzer", layout="wide")

# ==============================================
# DEBUG IMPORTS
# ==============================================
import streamlit as st
import pandas as pd
import sys
from pathlib import Path
from io import BytesIO
import matplotlib.pyplot as plt

# Debug header
st.sidebar.subheader("🐛 Debug Console")

# Show Python path and file structure
with st.sidebar.expander("System Info"):
    st.write("Python version:", sys.version)
    st.write("Python path:", sys.path)
    st.write("Current file:", Path(__file__).resolve())

# ==============================================
# DEBUGGABLE IMPORT SYSTEM
# ==============================================
try:
    # Try absolute import first
    from src.utils.stats_helpers import run_group_comparison, run_z_chi_tests, get_descriptive_stats
    st.sidebar.success("✅ Utils imported via absolute path")
except ImportError as e:
    st.sidebar.warning("⚠️ Absolute import failed. Trying fallbacks...")
    
    try:
        # Fallback 1: Relative import
        from ..utils.stats_helpers import run_group_comparison, run_z_chi_tests, get_descriptive_stats
        st.sidebar.success("✅ Utils imported via relative path")
    except (ImportError, ValueError) as e:
        st.sidebar.warning(f"⚠️ Relative import failed: {str(e)}")
        
        try:
            # Fallback 2: Path manipulation
            sys.path.append(str(Path(__file__).parent.parent.parent))
            from src.utils.stats_helpers import run_group_comparison, run_z_chi_tests, get_descriptive_stats
            st.sidebar.success("✅ Utils imported via path manipulation")
        except ImportError as e:
            st.sidebar.error(f"❌ All import methods failed: {str(e)}")
            st.sidebar.info("Using placeholder functions instead")
            
            # Placeholder implementations
            def run_group_comparison(df, group1, group2):
                """Placeholder group comparison"""
                return pd.DataFrame({
                    "Metric": ["Mean", "Count"],
                    group1: [df[group1].mean(), len(df[group1])],
                    group2: [df[group2].mean(), len(df[group2])]
                })
            
            def run_z_chi_tests(df):
                """Placeholder statistical tests"""
                return pd.DataFrame({
                    "Test": ["Z-test", "Chi-square"],
                    "Value": [0.0, 0.0],
                    "p-value": [1.0, 1.0]
                })
            
            def get_descriptive_stats(df):
                """Placeholder descriptive stats"""
                return df.describe()

# ==============================================
# MAIN APPLICATION (ORIGINAL CODE)
# ==============================================
st.title("🚀 Enhanced CrossTabs Analyzer")

# Debug module status
with st.expander("🔧 Module Status", expanded=True):
    col1, col2 = st.columns(2)
    with col1:
        st.write("**Available Functions:**")
        st.code("""
        - run_group_comparison
        - run_z_chi_tests
        - get_descriptive_stats
        """)
    with col2:
        st.write("**System Checks:**")
        st.write(f"Pandas: {pd.__version__}")
        st.write(f"Streamlit: {st.__version__}")
        st.write("Utils imported:", "run_group_comparison" in globals())

# Rest of your original code continues here...
class AnalysisPlugins:
    # ... [keep all your existing class code] ...

# Core Application Setup
st.markdown("---")

if "df" not in st.session_state:
    st.session_state.update({
        "df": None,
        "enable_insights": False,
        "enable_enhanced_stats": False
    })

# ... [keep all your existing application code] ...
