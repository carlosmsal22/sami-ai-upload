import streamlit as st
import pandas as pd
from utils.gpt_helpers import generate_gpt_summary
import os

st.set_page_config(page_title="📊 Cross-Tabs Analyzer", layout="wide")
st.title("📊 Cross-Tabs Reader + GPT Insight Summarizer")

uploaded_file = st.file_uploader("Upload a cross-tabulated Excel file", type=["xlsx"])

def preprocess_excel(file):
    df = pd.read_excel(file, sheet_name=0)
    df.fillna("", inplace=True)
    return df

if uploaded_file:
    st.success("✅ File uploaded successfully!")
    df = preprocess_excel(uploaded_file)
    st.dataframe(df, use_container_width=True)

    if st.button("🧠 Generate GPT Summary"):
        st.info("Sending data to GPT...")
        gpt_prompt = f"""You are a market insights strategist. Analyze the following cross-tabulated data and extract meaningful group-level insights.
Focus on trends, differences, and opportunities.

Data:
{df.head(30).to_markdown(index=False)}"""

        try:
            summary = generate_gpt_summary(gpt_prompt)
            st.subheader("🧠 GPT Insights Summary")
            st.markdown(summary)

            # Save to text file
            os.makedirs("outputs", exist_ok=True)
            with open("outputs/summary.txt", "w", encoding="utf-8") as f:
                f.write(summary)

        except Exception as e:
            st.error(f"❌ GPT generation failed: {e}")
