import streamlit as st
import pandas as pd
from utils.gpt_helpers import generate_gpt_summary

st.set_page_config(page_title="📊 CrossTabs Analyzer", layout="wide")
st.title("📊 CrossTabs Analyzer + GPT Summary")
st.markdown("Upload a cross-tabulated Excel file to generate group-wise GPT insights.")

uploaded_file = st.file_uploader("Upload Excel CrossTab", type=["xlsx", "xls"])

if uploaded_file:
    try:
        st.info("Reading Excel...")
        df = pd.read_excel(uploaded_file, header=[0, 1])
        st.success("File loaded successfully!")
        st.dataframe(df)

        if st.button("🧠 Generate GPT Insights"):
            st.subheader("🧠 GPT Insights Summary")
            sample = df.head(5).iloc[:, :5].to_string()
            prompt = f"""You are a market research analyst. Interpret this cross-tabulated table and summarize key group differences and insights:\n{sample}"""
            summary = generate_gpt_summary(prompt)
            st.markdown(summary)

            with open("outputs/summary.txt", "w", encoding="utf-8") as f:
                f.write(summary)
            st.success("Summary saved to outputs/summary.txt")
    except Exception as e:
        st.error(f"❌ Error parsing file: {e}")
