import streamlit as st
import pandas as pd
from utils.gpt_helpers import summarize_gpt_slide_text
import os

st.set_page_config(page_title="CrossTabs Analyzer", layout="wide")
st.title("📊 CrossTabs Analyzer + GPT Summary")

uploaded_file = st.file_uploader("Upload Cross-Tabulated Excel File", type=["xlsx", "xls"])
if uploaded_file:
    df = pd.read_excel(uploaded_file, header=[0, 1, 2])
    df.columns = [' '.join(col).strip() for col in df.columns.values]
    st.success("✅ File uploaded and parsed!")
    st.dataframe(df.head(10), use_container_width=True)

    if st.button("🧠 Generate Deeper Summary"):
        with st.spinner("Generating insights..."):
            try:
                summary = summarize_gpt_slide_text(df.head(30))
                st.subheader("🧠 GPT Insights Summary")
                st.markdown(summary)
            except Exception as e:
                st.error(f"GPT Error: {e}")
