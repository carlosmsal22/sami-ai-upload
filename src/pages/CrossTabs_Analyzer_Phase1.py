import streamlit as st
import pandas as pd
import sys
from pathlib import Path

# Add the src directory to Python path (works in GitHub Codespaces and Render)
sys.path.append(str(Path(__file__).parent.parent))

# Now import from utils directly
from utils.stats_helpers import run_group_comparison, run_z_chi_tests, get_descriptive_stats

st.set_page_config(page_title="CrossTabs Analyzer – Phase 1", layout="wide")
st.title("📊 CrossTabs Analyzer – Phase 1")

st.markdown("---")
tabs = st.tabs(["📘 Frequency Tables", "🔍 Group Comparisons", "🧪 Z / Chi-Square Tests", "📏 Descriptive Stats", "📤 Export Tools"])

# Initialize session state if not present
if "df" not in st.session_state:
    st.session_state["df"] = None

# File uploader with error handling
uploaded_file = st.file_uploader(
    "Upload a cross-tabulated file (Excel format)", 
    type=["xlsx", "xls"],
    key="file_uploader"
)

if uploaded_file:
    try:
        df = pd.read_excel(uploaded_file, header=[0, 1, 2])
        st.session_state["df"] = df
        st.success("✅ File loaded successfully!")
        
        # Debug: Show raw columns
        with st.expander("🔍 Debug: Show Column Structure"):
            st.write("Columns:", df.columns.tolist())
            st.write("Data Sample:", df.head(3))
            
    except Exception as e:
        st.error(f"❌ Error reading file: {str(e)}")
        st.session_state["df"] = None

# Reset button
if st.button("🔄 Reset Data"):
    st.session_state["df"] = None
    st.rerun()

# Main analysis tabs (only show if data exists)
if st.session_state["df"] is not None:
    df = st.session_state["df"]
    
    with tabs[0]:
        st.subheader("📘 Frequency Table")
        st.dataframe(df, use_container_width=True)
        
        # Add value counts for each column
        with st.expander("🔢 Value Counts"):
            for col in df.columns:
                st.write(f"**{col}**")
                st.dataframe(df[col].value_counts(dropna=False))

    with tabs[1]:
        st.subheader("🔍 Compare Groups")
        columns = df.columns.tolist()
        
        col1, col2 = st.columns(2)
        with col1:
            group1 = st.selectbox("Select Group 1", columns, key="group1")
        with col2:
            group2 = st.selectbox("Select Group 2", columns, key="group2")
            
        if st.button("Run Comparison"):
            try:
                result = run_group_comparison(df, group1, group2)
                st.dataframe(result)
            except Exception as e:
                st.error(f"Comparison failed: {str(e)}")

    with tabs[2]:
        st.subheader("🧪 Z-Test / Chi-Square")
        if st.button("Run Statistical Tests"):
            try:
                result = run_z_chi_tests(df)
                st.dataframe(result)
            except Exception as e:
                st.error(f"Tests failed: {str(e)}")

    with tabs[3]:
        st.subheader("📏 Descriptive Stats")
        if st.button("Generate Summary Statistics"):
            try:
                result = get_descriptive_stats(df)
                st.dataframe(result)
            except Exception as e:
                st.error(f"Stats generation failed: {str(e)}")

    with tabs[4]:
        st.subheader("📤 Export Tools")
        
        st.download_button(
            label="Download CSV",
            data=df.to_csv(index=False),
            file_name="crosstabs_data.csv",
            mime="text/csv"
        )
        
        st.download_button(
            label="Download Excel",
            data=df.to_excel(index=False),
            file_name="crosstabs_data.xlsx",
            mime="application/vnd.ms-excel"
        )
else:
    st.warning("⚠️ Please upload a file to begin analysis")

# Debug session state
with st.expander("🐛 Debug: Session State"):
    st.write(st.session_state)
