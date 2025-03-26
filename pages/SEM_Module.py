import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from semopy import Model, Optimizer
from openai import OpenAI
import os

st.set_page_config(page_title="Structural Equation Modeling", layout="wide")
st.title("🧩 Structural Equation Modeling (SEM)")

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

st.markdown("Upload data and provide a SEM model definition to estimate latent and observed relationships.")

uploaded_file = st.file_uploader("Upload CSV or Excel file", type=["csv", "xlsx"])
model_spec = st.text_area("Paste your SEM model specification (lavaan-style syntax)", height=200)

if uploaded_file and model_spec:
    df = pd.read_excel(uploaded_file) if uploaded_file.name.endswith("xlsx") else pd.read_csv(uploaded_file)
    st.success(f"Loaded {df.shape[0]} rows and {df.shape[1]} columns.")
    st.dataframe(df.head())

    if st.button("Run SEM Model"):
        try:
            model = Model(model_spec)
            opt = Optimizer(model)
            opt.optimize(df)

            st.subheader("✅ Model Fit Statistics")
            st.write(model.inspect("gfi"))

            st.subheader("📊 Parameter Estimates")
            estimates = model.inspect()
            st.dataframe(estimates)

            fig, ax = plt.subplots(figsize=(6, 4))
            ax.hist(df.dropna().isnull().sum(), bins=10)
            ax.set_title("Missing Data Distribution")
            st.pyplot(fig)

            prompt = f"SEM results:\n{estimates.to_string()}"
            response = client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": "You are a SEM analyst interpreting structural equation model output."},
                    {"role": "user", "content": prompt}
                ]
            )
            st.subheader("💬 GPT Insight")
            st.markdown(response.choices[0].message.content)

        except Exception as e:
            st.error(f"SEM model error: {e}")
