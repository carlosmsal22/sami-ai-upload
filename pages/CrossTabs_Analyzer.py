
import streamlit as st
import pandas as pd
from utils.gpt_helpers import summarize_gpt_slide_text

st.set_page_config(page_title="📊 CrossTabs Analyzer", layout="wide")
st.title("📊 CrossTabs Analyzer + GPT Summary")

uploaded_file = st.file_uploader("Upload Cross-Tabulated Excel File", type=["xlsx", "xls"])
if uploaded_file:
    try:
        df = pd.read_excel(uploaded_file, header=[0, 1])
        df.columns = [' '.join(col).strip() for col in df.columns.values]
        st.dataframe(df.head(30))

        st.subheader("🧠 GPT Insights Summary")
        with st.spinner("Analyzing table with GPT..."):
            summary = summarize_gpt_slide_text(df.head(30))
            st.markdown(summary)
    except Exception as e:
        st.error(f"❌ Error parsing file: {e}")
