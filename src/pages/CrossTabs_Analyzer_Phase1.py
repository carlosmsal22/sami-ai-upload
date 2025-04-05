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

if "df" not in st.session_state:
    uploaded_file = st.file_uploader("Upload a cross-tabulated file to see frequency distributions.", type=["xlsx", "xls"])
    if uploaded_file:
        df = pd.read_excel(uploaded_file, header=[0, 1, 2])
        st.session_state["df"] = df
else:
    df = st.session_state["df"]

if "df" in st.session_state:
    with tabs[0]:
        st.subheader("📘 Frequency Table")
        st.dataframe(df, use_container_width=True)

    with tabs[1]:
        st.subheader("🔍 Compare Groups")
        columns = df.columns.tolist()
        col1 = st.selectbox("Select Group 1", columns, key="group1")
        col2 = st.selectbox("Select Group 2", columns, key="group2")
        if st.button("Compare Groups"):
            result = run_group_comparison(df, col1, col2)
            st.dataframe(result)

    with tabs[2]:
        st.subheader("🧪 Z-Test / Chi-Square")
        if st.button("Run Z / Chi-Square Tests"):
            result = run_z_chi_tests(df)
            st.dataframe(result)

    with tabs[3]:
        st.subheader("📏 Descriptive Stats")
        if st.button("Generate Summary Stats"):
            result = get_descriptive_stats(df)
            st.dataframe(result)

    with tabs[4]:
        st.subheader("📤 Export")
        csv = df.to_csv(index=False)
        st.download_button("Download CSV", csv, "crosstabs_data.csv", "text/csv")
