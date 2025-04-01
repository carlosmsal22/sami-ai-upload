
import streamlit as st
import pandas as pd
from utils.gpt_helpers import generate_gpt_summary

st.set_page_config(page_title="CrossTabs Analyzer + GPT Summary")

st.title("📊 CrossTabs Analyzer + GPT Summary")

uploaded_file = st.file_uploader("Upload Cross-Tabulated Excel File", type=["xlsx", "xls"])
if uploaded_file:
    df = pd.read_excel(uploaded_file, header=[0, 1, 2])
    st.success("✅ File uploaded and parsed!")
    st.dataframe(df.head(10))

    st.subheader("🧠 GPT Insights Summary")
    if st.button("Generate Deeper Summary"):
        summary = generate_gpt_summary(df)
        st.markdown(summary)
