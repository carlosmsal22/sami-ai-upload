import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import os

from utils.parsers import parse_crosstab_file
from utils.gpt_helpers import summarize_crosstab
from utils.visualizers import plot_group_bars

st.set_page_config(page_title="📊 CrossTabs Analyzer", layout="wide")
st.title("📊 Cross-Tabs Analyzer + GPT Summary")

uploaded_file = st.file_uploader("Upload your cross-tab Excel file", type=["xlsx", "xls"])

if uploaded_file:
    try:
        st.info("Parsing file and detecting headers...")
        df, row_headers, col_headers = parse_crosstab_file(uploaded_file)
        st.success(f"Parsed successfully with {len(df)} rows.")

        st.subheader("🔍 Data Preview")
        st.dataframe(df.head(20))

        st.subheader("📊 Group Comparison Chart")
        fig = plot_group_bars(df)
        st.pyplot(fig)

        st.subheader("🧠 GPT Insights Summary")
        if st.button("🔍 Generate Insight Summary"):
            with st.spinner("Sending data to GPT..."):
                summary = summarize_crosstab(df)
                st.markdown(summary)
    except Exception as e:
        st.error(f"❌ Error parsing file: {str(e)}")
