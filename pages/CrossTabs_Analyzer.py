import streamlit as st
import pandas as pd
import openai
from utils.gpt_helpers import summarize_gpt_slide_text

st.set_page_config(page_title="CrossTabs Analyzer", layout="wide")
st.title("📊 CrossTabs Analyzer + GPT Summary")

uploaded_file = st.file_uploader("Upload Cross-Tabulated Excel File", type=["xlsx", "xls"])
if uploaded_file:
    df = pd.read_excel(uploaded_file, header=[0, 1, 2])
    df.columns = [" | ".join([str(i) for i in col if 'Unnamed' not in str(i)]).strip() for col in df.columns.values]
    st.success("✅ File uploaded and parsed!")
    st.dataframe(df.head(10))

    if st.button("🧠 Generate Deeper Summary"):
        try:
            with st.spinner("Analyzing with GPT..."):
                summary = summarize_gpt_slide_text(df)
                st.markdown("### 🧠 GPT Insights Summary")
                st.markdown(summary)
        except Exception as e:
            st.error(f"❌ GPT Error: {e}")
