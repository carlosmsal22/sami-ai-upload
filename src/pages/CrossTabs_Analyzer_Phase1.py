import streamlit as st
import pandas as pd
import sys
from pathlib import Path
from io import BytesIO

# Add the src directory to Python path
sys.path.append(str(Path(__file__).parent.parent))

# Import from utils
from utils.stats_helpers import run_group_comparison, run_z_chi_tests, get_descriptive_stats

st.set_page_config(page_title="CrossTabs Analyzer – Phase 1", layout="wide")
st.title("📊 CrossTabs Analyzer – Phase 1")

st.markdown("---")
tabs = st.tabs(["📘 Frequency Tables", "🔍 Group Comparisons", "🧪 Z / Chi-Square Tests", "📏 Descriptive Stats", "📄 Export Tools"])

# Initialize session state
if "df" not in st.session_state:
    st.session_state["df"] = None

# File uploader with enhanced error handling
uploaded_file = st.file_uploader(
    "Upload a cross-tabulated file (Excel format)", 
    type=["xlsx", "xls"],
    key="file_uploader"
)

flatten = st.checkbox("🔄 Flatten MultiIndex Columns (Recommended)", value=True)

if uploaded_file:
    try:
        df = pd.read_excel(uploaded_file, header=[0, 1, 2])
        if flatten and isinstance(df.columns, pd.MultiIndex):
            df.columns = ['_'.join(filter(None, map(str, col))).strip() for col in df.columns.values]
        st.session_state["df"] = df
        st.success("✅ File loaded successfully!")

        with st.expander("🔍 Debug: Show Column Structure"):
            st.write("Columns:", df.columns.tolist())
            st.write("Shape:", df.shape)
            st.write("Data Sample:", df.head(3))

    except Exception as e:
        st.error(f"❌ Error reading file: {str(e)}")
        st.session_state["df"] = None

# Reset button
if st.button("🔄 Reset Data"):
    st.session_state["df"] = None
    st.rerun()

# Main analysis tabs
if st.session_state["df"] is not None:
    df = st.session_state["df"]

    with tabs[0]:
        st.subheader("📘 Frequency Table")
        st.dataframe(df, use_container_width=True)

        with st.expander("🔢 Value Counts"):
            for col in df.columns:
                st.write(f"**{col}**")
                st.dataframe(df[col].value_counts(dropna=False))

    with tabs[1]:
        st.subheader("🔍 Compare Groups")
        columns = df.columns.tolist()

        col1, col2 = st.columns(2)
        with col1:
            group_col = st.selectbox("Select Group Column (Banner)", columns, key="group")
        with col2:
            metric_col = st.selectbox("Select Metric Column", columns, key="metric")

        if st.button("Run Comparison"):
            try:
                result = run_group_comparison(df, group_col, metric_col)
                st.dataframe(result)
                st.download_button("Download Comparison Results", result.to_csv(index=False), "group_comparison.csv", "text/csv")
            except Exception as e:
                st.error(f"Comparison failed: {str(e)}")

    with tabs[2]:
        st.subheader("🧪 Z-Test / Chi-Square")
        if st.button("Run Statistical Tests"):
            try:
                result = run_z_chi_tests(df)
                st.dataframe(result)
                st.download_button("Download Z/Chi Results", result.to_csv(index=False), "z_chi_results.csv", "text/csv")
            except Exception as e:
                st.error(f"Tests failed: {str(e)}")

    with tabs[3]:
        st.subheader("📏 Descriptive Stats")
        numeric_cols = df.select_dtypes(include='number').columns.tolist()

        if not numeric_cols:
            st.warning("⚠️ No numeric columns found.")
        else:
            if st.button("Generate Summary Statistics"):
                try:
                    result = get_descriptive_stats(df[numeric_cols])
                    st.dataframe(result)
                    st.download_button("Download Descriptive Stats", result.to_csv(index=False), "descriptive_stats.csv", "text/csv")
                except Exception as e:
                    st.error(f"Stats generation failed: {str(e)}")

    with tabs[4]:
        st.subheader("📤 Export Tools")

        try:
            st.download_button(
                label="Download Full CSV",
                data=df.to_csv(index=False),
                file_name="crosstabs_data.csv",
                mime="text/csv"
            )

            excel_buffer = BytesIO()
            with pd.ExcelWriter(excel_buffer, engine='openpyxl') as writer:
                export_df = df.copy()
                if isinstance(export_df.columns, pd.MultiIndex):
                    export_df.columns = ['_'.join(filter(None, map(str, col))).strip() 
                                          for col in export_df.columns.values]
                export_df.to_excel(writer, index=False, sheet_name="Data")
            excel_buffer.seek(0)

            st.download_button(
                label="Download Excel",
                data=excel_buffer,
                file_name="crosstabs_data.xlsx",
                mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
            )

        except Exception as e:
            st.error(f"Export failed: {str(e)}")

else:
    st.warning("⚠️ Please upload a file to begin analysis")

# Optional debug section
with st.expander("🐛 Debug: Session State"):
    st.write(st.session_state)
