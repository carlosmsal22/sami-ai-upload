import streamlit as st
import pandas as pd
from utils.gpt_helpers import compare_two_groups

st.set_page_config(page_title="CrossTabs Step 2", layout="wide")
st.title("📊 CrossTabs Analyzer – Step 2: Compare Groups")

uploaded_file = st.file_uploader("Upload Cross-Tabulated Excel File", type=["xlsx", "xls"])
if uploaded_file:
    df = pd.read_excel(uploaded_file, header=[0, 1, 2])
    df.columns = [' '.join(col).strip() for col in df.columns.values]
    st.success("✅ File uploaded and parsed!")
    st.dataframe(df.head(10), use_container_width=True)

    st.markdown("🧮 Choose two groups (columns) to compare:")
    group1 = st.selectbox("Group 1 Column", df.columns.tolist())
    group2 = st.selectbox("Group 2 Column", df.columns.tolist())

    if st.button("🧠 Summarize Key Differences"):
        try:
            summary = compare_two_groups(df, group1, group2)
            st.subheader("🧠 GPT Insight Generator")
            st.markdown(summary)
        except Exception as e:
            st.error(f"Error: {e}")
