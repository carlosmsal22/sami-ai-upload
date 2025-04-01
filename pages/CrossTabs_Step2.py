import streamlit as st
import pandas as pd
from utils.gpt_helpers import summarize_comparisons

st.set_page_config(page_title="CrossTabs Step 2 – Enhanced GPT Comparison", layout="wide")

st.title("📊 Cross-Tabs Analyzer – Step 2: Enhanced GPT Comparison")

uploaded_file = st.file_uploader("Upload your cross-tab file", type=["xlsx"])

if uploaded_file:
    try:
        df = pd.read_excel(uploaded_file, header=None)
        st.success("✅ File uploaded and parsed!")
        st.dataframe(df.head(10))

        if st.button("🤖 Generate Smart GPT Insights"):
            st.subheader("🧠 GPT Enhanced Comparison Summary")
            with st.spinner("Generating enhanced GPT summary..."):
                try:
                    summary = summarize_comparisons(df)
                    st.markdown(summary)
                except Exception as e:
                    st.error(f"Error generating GPT summary: {str(e)}")

    except Exception as e:
        st.error(f"❌ Error reading file: {str(e)}")
