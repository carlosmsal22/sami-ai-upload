
import streamlit as st
import pandas as pd
import sys
from pathlib import Path
from io import BytesIO
import re
from openai import OpenAI

# Add the src directory to Python path
sys.path.append(str(Path(__file__).parent.parent))

# Import from utils
from utils.stats_helpers import run_group_comparison, run_z_chi_tests, get_descriptive_stats

st.set_page_config(page_title="CrossTabs Analyzer – Phase 1", layout="wide")
st.title("📊 CrossTabs Analyzer – Phase 1")

st.markdown("---")
tabs = st.tabs(["📘 Frequency Tables", "🔍 Group Comparisons", "🧪 Z / Chi-Square Tests", "📏 Descriptive Stats", "📤 Export Tools"])

# Initialize session state
if "df" not in st.session_state:
    st.session_state["df"] = None

# File uploader with enhanced error handling
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

        if st.button("Generate GPT Summary + Excel Export"):
            try:
                # Flatten MultiIndex columns for export
                export_df = df.copy()
                if isinstance(export_df.columns, pd.MultiIndex):
                    export_df.columns = [' '.join([str(c) for c in col if c]).strip() for col in export_df.columns.values]

                st.dataframe(export_df.head())

                # GPT Summary
                client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
                table_text = export_df.head(4).to_string(index=False)
                prompt = f"""You are a senior research analyst. Provide a 2-paragraph summary of differences in the following cross-tab table and key implications:

{table_text}"""
                with st.spinner("GPT generating summary..."):
                    response = client.chat.completions.create(
                        model="gpt-4",
                        messages=[
                            {"role": "system", "content": "You are an expert in cross-tab analysis."},
                            {"role": "user", "content": prompt}
                        ]
                    )
                    summary = response.choices[0].message.content
                    st.markdown("### 🧠 Executive Summary")
                    st.markdown(summary)

                # Excel Export
                excel_buffer = BytesIO()
                with pd.ExcelWriter(excel_buffer, engine='openpyxl') as writer:
                    export_df.to_excel(writer, index=False, sheet_name="Segment Table")
                excel_buffer.seek(0)
                st.download_button("📥 Download Segment Table (Excel)", data=excel_buffer, file_name="Formatted_CrossTab.xlsx")
            except Exception as e:
                st.error(f"Export/GPT summary failed: {str(e)}")

else:
    st.warning("⚠️ Please upload a file to begin analysis")

# Optional debug section
with st.expander("🐛 Debug: Session State"):
    st.write(st.session_state)
