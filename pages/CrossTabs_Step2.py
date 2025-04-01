import streamlit as st
import pandas as pd
from utils.gpt_helpers import summarize_comparisons

st.set_page_config(page_title="CrossTabs Step2", layout="wide")
st.title("📊 CrossTabs Analyzer – Step 2: Compare Groups")

uploaded_file = st.file_uploader("Upload Cross-Tabulated Excel File", type=["xlsx", "xls"])
if uploaded_file:
    df = pd.read_excel(uploaded_file, header=[0, 1, 2])
    df.columns = [" | ".join([str(i) for i in col if 'Unnamed' not in str(i)]).strip() for col in df.columns.values]
    st.success("✅ File uploaded and parsed!")
    st.dataframe(df.head(5))

    columns = df.columns.tolist()
    col1 = st.selectbox("Group 1 Column", columns)
    col2 = st.selectbox("Group 2 Column", columns)

    if st.button("🧠 Summarize Key Differences"):
        try:
            comparison = summarize_comparisons(df, col1, col2)
            st.markdown("### 🧠 GPT Insight Generator")
            st.markdown(comparison)
        except Exception as e:
            st.error(f"Error: {e}")
