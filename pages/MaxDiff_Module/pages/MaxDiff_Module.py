import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import statsmodels.api as sm
import os
from openai import OpenAI

st.set_page_config(page_title="MaxDiff Analysis", layout="wide")
st.title("📊 MaxDiff Analysis Module")

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

st.markdown("Upload your MaxDiff survey response data to estimate relative preference scores.")

uploaded_file = st.file_uploader("Upload Excel or CSV file", type=["xlsx", "csv"])

if uploaded_file:
    df = pd.read_excel(uploaded_file) if uploaded_file.name.endswith("xlsx") else pd.read_csv(uploaded_file)
    st.success(f"Loaded {df.shape[0]} rows and {df.shape[1]} columns.")
    st.dataframe(df.head())

    id_col = st.selectbox("Respondent ID column", df.columns)
    task_col = st.selectbox("Task/Set column", df.columns)
    best_col = st.selectbox("BEST choice column", df.columns)
    worst_col = st.selectbox("WORST choice column", df.columns)
    attribute_col = st.selectbox("Attribute/Item column", df.columns)

    if st.button("Estimate Preference Scores"):
        df["score"] = df.apply(lambda row: 1 if row[attribute_col] == row[best_col] else (-1 if row[attribute_col] == row[worst_col] else 0), axis=1)
        scores = df.groupby(attribute_col)["score"].sum().sort_values(ascending=False)
        st.subheader("📊 Preference Scores (Best-Worst Totals)")
        st.dataframe(scores)

        fig, ax = plt.subplots()
        scores.plot(kind="bar", ax=ax)
        ax.set_ylabel("Preference Score")
        st.pyplot(fig)

        prompt = f"Here are relative preference scores from a MaxDiff study:\n{scores.to_string()}"
        try:
            with st.spinner("GPT interpreting MaxDiff results..."):
                response = client.chat.completions.create(
                    model="gpt-3.5-turbo",
                    messages=[
                        {"role": "system", "content": prompt},
                        {"role": "user", "content": "Please summarize key preferences and insights from this MaxDiff data."}
                    ]
                )
                st.subheader("💬 GPT Insight")
                st.markdown(response.choices[0].message.content)
        except Exception as e:
            st.error(f"GPT error: {e}")
