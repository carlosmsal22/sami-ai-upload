import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import statsmodels.api as sm
from openai import OpenAI
import os

st.set_page_config(page_title="Conjoint Analysis", layout="wide")

st.title("📦 CBC Conjoint Module")

st.markdown("Estimate part-worth utilities from choice-based conjoint (CBC) data and simulate preferences.")

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

uploaded_file = st.file_uploader("Upload CBC Choice Task Data (Excel or CSV)", type=["xlsx", "csv"])

# Example structure:
# respondent_id | task | alternative | choice | brand | price | featureX ...

if uploaded_file:
    df = pd.read_excel(uploaded_file) if uploaded_file.name.endswith(".xlsx") else pd.read_csv(uploaded_file)
    st.success(f"Loaded {df.shape[0]} rows with {df.shape[1]} columns.")
    st.dataframe(df.head())

    id_col = st.selectbox("Respondent ID column", df.columns)
    task_col = st.selectbox("Task column", df.columns)
    alt_col = st.selectbox("Alternative column", df.columns)
    choice_col = st.selectbox("Choice column (1 = chosen, 0 = not chosen)", df.columns)
    attributes = st.multiselect("Attributes to include in the model", [col for col in df.columns if col not in [id_col, task_col, alt_col, choice_col]])

    if st.button("Estimate Part-Worth Utilities"):
        df_encoded = pd.get_dummies(df[attributes], drop_first=True)
        X = df_encoded
        y = df[choice_col]

        model = sm.Logit(y, X).fit(disp=False)
        utilities = model.params

        st.subheader("📊 Estimated Part-Worth Utilities")
        st.dataframe(utilities)

        fig, ax = plt.subplots(figsize=(10, 5))
        utilities.sort_values().plot(kind="barh", ax=ax)
        st.pyplot(fig)

        # GPT interpretation
                # GPT interpretation
        system_prompt = f"You are a research analyst. Based on these part-worth utilities from a CBC model:\n{utilities.to_string()}"

        try:
            with st.spinner("GPT analyzing the results..."):
                response = client.chat.completions.create(
                    model="gpt-3.5-turbo",
                    messages=[
                        {"role": "system", "content": system_prompt},
                        {"role": "user", "content": "Please summarize the key findings and attribute importance."}
                    ]
                )
                st.markdown(response.choices[0].message.content)

        try:
            with st.spinner("GPT analyzing the results..."):
                response = client.chat.completions.create(
                    model="gpt-3.5-turbo",
                    messages=[
                        {"role": "system", "content": system_prompt},
                        {"role": "user", "content": "Please summarize the key findings and attribute importance."}
                    ]
                )
                st.markdown(response.choices[0].message.content)
        except Exception as e:
            st.error(f"GPT error: {e}")
