
import streamlit as st
import pandas as pd
from utils.gpt_helpers import summarize_comparisons

st.set_page_config(page_title="CrossTabs Step 2", layout="wide")
st.title("📊 Cross-Tabs Analyzer – Step 2: Enhanced GPT Comparison")

uploaded_file = st.file_uploader("Upload your cross-tab file", type=[".xlsx"])
if uploaded_file:
    try:
        df = pd.read_excel(uploaded_file)
        st.success("✅ File uploaded and parsed!")
        st.dataframe(df.head(30))
        
        if st.button("🔍 Generate Smart GPT Insights"):
            with st.spinner("Analyzing group differences..."):
                insights = summarize_comparisons(df)
                st.markdown("### 🧠 GPT Enhanced Comparison Summary")
                st.markdown(insights)
    except Exception as e:
        st.error(f"❌ Error parsing file: {e}")
