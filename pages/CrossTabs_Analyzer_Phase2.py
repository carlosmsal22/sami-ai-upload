import streamlit as st
import pandas as pd
from utils.gpt_helpers import summarize_gpt_slide_text

st.set_page_config(page_title="📊 Cross-Tabs Analyzer", layout="wide")

st.title("📊 Cross-Tabs Analyzer")

with st.sidebar:
    st.header("📥 Upload Cross-Tab File")
    uploaded_file = st.file_uploader("Upload Excel file", type=["xlsx"])

    st.markdown("---")
    st.header("📈 Group Comparison")
    group_col = st.text_input("Group Column (e.g., Gender, Age Group)")
    metric_col = st.text_input("Metric Column (e.g., Satisfaction, Awareness)")

    st.markdown("---")
    st.header("📊 Frequency Distributions")
    freq_col = st.text_input("Column to Show Frequencies")

if uploaded_file:
    df = pd.read_excel(uploaded_file)

    st.subheader("📋 Raw Cross-Tabulated Data")
    st.dataframe(df)

    if group_col and metric_col and group_col in df.columns and metric_col in df.columns:
        st.subheader(f"📊 Comparison: {metric_col} by {group_col}")
        group_summary = df.groupby(group_col)[metric_col].agg(["count", "mean", "median", "std"])
        st.dataframe(group_summary)

        gpt_prompt = f"""You are a data analyst. Analyze the comparison of {metric_col} across {group_col} groups below and provide a brief executive summary:

{group_summary.to_markdown()}"""
        gpt_summary = summarize_gpt_slide_text(gpt_prompt)
        st.subheader("🧠 GPT Summary")
        st.markdown(gpt_summary)

    if freq_col and freq_col in df.columns:
        st.subheader(f"📊 Frequency Distribution for {freq_col}")
        freq_table = df[freq_col].value_counts().reset_index()
        freq_table.columns = [freq_col, "Frequency"]
        st.dataframe(freq_table)