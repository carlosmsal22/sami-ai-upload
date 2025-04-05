import streamlit as st
import pandas as pd
from utils.gpt_helpers import summarize_gpt_slide_text
from io import StringIO

st.set_page_config(page_title="📊 Cross-Tabs Analyzer – Phase 2", layout="wide")
st.title("📊 Cross-Tabs Analyzer – Phase 2")

# Sidebar UI
with st.sidebar:
    st.header("📥 Upload Cross-Tab File")
    uploaded_file = st.file_uploader("Upload Excel file", type=["xlsx"])

    st.markdown("---")
    st.header("📈 Group Comparison Setup")
    group_col = st.text_input("Group Column (e.g., Gender, Age Group)")
    metric_col = st.text_input("Metric Column (e.g., Satisfaction, Awareness)")

    st.markdown("---")
    st.header("📊 Frequency Distribution Setup")
    freq_col = st.text_input("Column to Show Frequencies")

# Upload and persist file
if uploaded_file:
    try:
        df = pd.read_excel(uploaded_file)
        st.session_state["phase2_df"] = df
        st.success("✅ File uploaded successfully.")
    except Exception as e:
        st.error(f"❌ Failed to read Excel: {str(e)}")
else:
    if "phase2_df" in st.session_state:
        df = st.session_state["phase2_df"]
    else:
        df = None

# Show the data
if df is not None:
    st.subheader("📋 Raw Cross-Tabulated Data")
    st.dataframe(df, use_container_width=True)

    # --- Group Comparison ---
    if group_col and metric_col and group_col in df.columns and metric_col in df.columns:
        st.markdown("### 📈 Group Summary Table")
        group_summary = df.groupby(group_col)[metric_col].agg(["count", "mean", "median", "std"]).reset_index()
        st.dataframe(group_summary)

        # Export CSV
        csv = group_summary.to_csv(index=False).encode("utf-8")
        st.download_button("⬇️ Download Group Summary CSV", data=csv, file_name="group_comparison.csv", mime="text/csv")

        # GPT Summary
        with st.spinner("🧠 Analyzing with GPT..."):
            try:
                gpt_prompt = f"""
You are a senior data analyst. Provide an executive summary comparing {metric_col} across {group_col} groups.

Data:
{group_summary.to_markdown(index=False)}
"""
                gpt_summary = summarize_gpt_slide_text(gpt_prompt)
                st.markdown("### 🧠 Executive Summary")
                st.markdown(gpt_summary)
            except Exception as e:
                st.error(f"❌ GPT analysis failed: {str(e)}")

    # --- Frequency Distribution ---
    if freq_col and freq_col in df.columns:
        st.markdown(f"### 📊 Frequency Distribution – {freq_col}")
        freq_table = df[freq_col].value_counts().reset_index()
        freq_table.columns = [freq_col, "Frequency"]
        st.dataframe(freq_table)

        # Export CSV
        freq_csv = freq_table.to_csv(index=False).encode("utf-8")
        st.download_button("⬇️ Download Frequency Table CSV", data=freq_csv, file_name="frequency_table.csv", mime="text/csv")
else:
    st.info("📂 Upload a valid Excel file to begin.")
