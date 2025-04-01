
import streamlit as st
import pandas as pd
import plotly.express as px
from utils.gpt_helpers import summarize_comparisons

st.set_page_config(page_title="📊 CrossTabs Step 2: Visualize & Compare", layout="wide")
st.title("📊 CrossTabs Analyzer – Step 2: Compare Groups")

uploaded_file = st.file_uploader("Upload Cross-Tabulated Excel File", type=["xlsx"])
if uploaded_file:
    try:
        df = pd.read_excel(uploaded_file, header=[0, 1])
        df.columns = [' '.join(col).strip() for col in df.columns.values]
        st.dataframe(df.head())

        col1 = st.selectbox("Group 1 Column", df.columns)
        col2 = st.selectbox("Group 2 Column", df.columns)
        if col1 != col2:
            fig = px.bar(df, x=col1, y=col2, barmode="group", title=f"Group Comparison: {col1} vs {col2}")
            st.plotly_chart(fig)

        st.subheader("🧠 GPT Insight Generator")
        if st.button("Summarize Key Differences"):
            summary = summarize_comparisons(df[[col1, col2]].dropna())
            st.markdown(summary)

    except Exception as e:
        st.error(f"❌ Error: {e}")
