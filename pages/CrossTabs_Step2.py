
import streamlit as st
import pandas as pd
from utils.gpt_helpers import summarize_gpt_slide_text

st.set_page_config(page_title="CrossTabs Analyzer – Step 2", layout="wide")
st.title("📊 CrossTabs Analyzer – Step 2: Compare Groups")

uploaded_file = st.file_uploader("Upload Cross-Tabulated Excel File", type=["xlsx", "xls"])
if uploaded_file:
    df = pd.read_excel(uploaded_file, header=[0, 1, 2])
    st.success("✅ File uploaded and parsed!")
    st.dataframe(df.head(5))

    clean_columns = [' | '.join([str(part) for part in col if 'Unnamed' not in str(part)]) for col in df.columns]
    st.write("⬇️ Choose two groups (columns) to compare:")

    col1 = st.selectbox("Group 1 Column", clean_columns, key="group1")
    col2 = st.selectbox("Group 2 Column", clean_columns, key="group2")

    if st.button("Summarize Key Differences"):
        try:
            if col1 != col2:
                sub_df = df[[col1, col2]].dropna()
                sub_df.columns = ["Group 1", "Group 2"]
                summary = summarize_gpt_slide_text(sub_df)
                st.markdown(summary)
            else:
                st.error("Please select two different columns to compare.")
        except Exception as e:
            st.error(f"Error: {e}")
