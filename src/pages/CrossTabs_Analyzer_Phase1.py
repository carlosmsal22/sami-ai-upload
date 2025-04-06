import streamlit as st
import pandas as pd
import sys
from pathlib import Path
from io import BytesIO
import matplotlib.pyplot as plt  # For visualization (original feature)

# Add the src directory to Python path
sys.path.append(str(Path(__file__).parent.parent))

# Import from utils (original imports)
from utils.stats_helpers import run_group_comparison, run_z_chi_tests, get_descriptive_stats

st.set_page_config(page_title="CrossTabs Analyzer", layout="wide")
st.title("📊 CrossTabs Analyzer")

st.markdown("---")
# Restore original tabs
tabs = st.tabs(["📘 Frequency Tables", "🔍 Group Comparisons", "🧪 Z / Chi-Square Tests", "📏 Descriptive Stats", "📤 Export Tools"])

# Initialize session state (original version)
if "df" not in st.session_state:
    st.session_state["df"] = None

# Original file uploader with error handling
uploaded_file = st.file_uploader(
    "Upload a cross-tabulated file (Excel format)", 
    type=["xlsx", "xls"],
    key="file_uploader"
)

if uploaded_file:
    try:
        # Original file loading logic
        df = pd.read_excel(uploaded_file, header=[0, 1, 2])
        st.session_state["df"] = df
        st.success("✅ File loaded successfully!")
        
        with st.expander("🔍 Debug: Show Column Structure"):
            st.write("Columns:", df.columns.tolist())
            st.write("Shape:", df.shape)
            st.write("Data Sample:", df.head(3))
            
    except Exception as e:
        st.error(f"❌ Error reading file: {str(e)}")
        st.session_state["df"] = None

# Original reset button
if st.button("🔄 Reset Data"):
    st.session_state["df"] = None
    st.rerun()

# Main analysis tabs (original functionality)
if st.session_state["df"] is not None:
    df = st.session_state["df"]
    
    # 1. Frequency Tables (original)
    with tabs[0]:
        st.subheader("📘 Frequency Table")
        st.dataframe(df, use_container_width=True)
        
        with st.expander("🔢 Value Counts"):
            for col in df.columns:
                st.write(f"**{col}**")
                st.dataframe(df[col].value_counts(dropna=False))

    # 2. Group Comparisons (original)
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

    # 3. Statistical Tests (original)
    with tabs[2]:
        st.subheader("🧪 Z-Test / Chi-Square")
        if st.button("Run Statistical Tests"):
            try:
                result = run_z_chi_tests(df)
                st.dataframe(result)
            except Exception as e:
                st.error(f"Tests failed: {str(e)}")

    # 4. Descriptive Stats (original)
    with tabs[3]:
        st.subheader("📏 Descriptive Stats")
        if st.button("Generate Summary Statistics"):
            try:
                result = get_descriptive_stats(df)
                st.dataframe(result)
            except Exception as e:
                st.error(f"Stats generation failed: {str(e)}")

    # 5. Export Tools (original with fix)
    with tabs[4]:
        st.subheader("📤 Export Tools")
        
        try:
            # CSV Export
            st.download_button(
                label="Download CSV",
                data=df.to_csv(index=False),
                file_name="crosstabs_data.csv",
                mime="text/csv"
            )
            
            # Excel Export
            excel_buffer = BytesIO()
            with pd.ExcelWriter(excel_buffer, engine='openpyxl') as writer:
                df.to_excel(writer, index=False)
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

# Debug section (original)
with st.expander("🐛 Debug: Session State"):
    st.write(st.session_state)
