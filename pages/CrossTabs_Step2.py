import streamlit as st
import pandas as pd
import plotly.express as px
from utils.gpt_helpers import summarize_comparisons

st.set_page_config(page_title="📊 CrossTabs Analyzer – Step 2", layout="wide")
st.title("📊 CrossTabs Analyzer – Step 2: Insights from Group Differences")

uploaded_file = st.file_uploader("📤 Upload Cleaned Cross-Tab Excel File", type=["xlsx"])

if uploaded_file:
    try:
        df = pd.read_excel(uploaded_file)

        st.subheader("📈 Group Comparison Chart")

        group_cols = [col for col in df.columns if df[col].dtype in [float, int]]
        question_col = df.columns[0]

        if group_cols and question_col:
            melted_df = df.melt(id_vars=question_col, value_vars=group_cols,
                                var_name="Group", value_name="Score")

            fig = px.bar(melted_df, x=question_col, y="Score", color="Group", barmode="group",
                         title="Group Differences Across Questions")
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.warning("No numeric group columns found.")

        # GPT Summary Logic
        st.subheader("🧠 GPT Insights Summary")
        if st.button("📢 Generate Executive Summary"):
            with st.spinner("Analyzing differences using GPT..."):
                summary = summarize_comparisons(df)
                st.markdown(summary)

    except Exception as e:
        st.error(f"❌ Error: {e}")
