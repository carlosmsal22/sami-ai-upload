import streamlit as st
import pandas as pd
import openai
import io
import base64
import matplotlib.pyplot as plt
import seaborn as sns

from utils.gpt_helpers import summarize_crosstabs
from utils.parsers import parse_crosstab_file

st.set_page_config(page_title="📊 Cross-Tabs Analyzer + GPT Insight Summarizer", layout="wide")
st.title("📊 Cross-Tabs Analyzer + GPT Insight Summarizer")

uploaded_file = st.file_uploader("Upload a cross-tabulated Excel or CSV file", type=["xlsx", "xls", "csv"])

if uploaded_file:
    # Parse the file structure
    with st.spinner("Parsing file and detecting headers..."):
        try:
            df, questions, groups = parse_crosstab_file(uploaded_file)
            st.success("✅ File parsed successfully")
        except Exception as e:
            st.error(f"❌ Error parsing file: {e}")
            st.stop()

    st.subheader("🧾 Preview of Parsed Cross-Tab Table")
    st.dataframe(df.head(50), use_container_width=True)

    st.markdown("---")
    st.subheader("📈 Visualize Group Comparisons")
    selected_question = st.selectbox("Select a question to visualize", questions)

    if selected_question:
        fig, ax = plt.subplots()
        sub_df = df[df['Question'] == selected_question].copy()
        sub_df.set_index("Group", inplace=True)
        sub_df.T.plot(kind="bar", ax=ax)
        ax.set_title(f"{selected_question} – Group Comparison")
        ax.set_ylabel("% Respondents")
        ax.legend(title="Groups")
        st.pyplot(fig)

    st.markdown("---")
    st.subheader("🧠 GPT Insight Summary")
    if st.button("Generate GPT Summary"):
    st.subheader("🧠 GPT Insights Summary")

    try:
        with st.spinner("Sending to GPT..."):
            insights = summarize_crosstabs(df)
            for line in insights:
                st.markdown(f"• {line}")
    except Exception as e:
        st.error(f"GPT summarization failed: {e}")
