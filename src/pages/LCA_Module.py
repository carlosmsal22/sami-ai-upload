import streamlit as st
import pandas as pd
import numpy as np
import os
from sklearn.mixture import GaussianMixture
import matplotlib.pyplot as plt
from openai import OpenAI

st.set_page_config(page_title="Latent Class Analysis", layout="wide")
st.title("🧬 Latent Class Analysis (LCA) Module")

st.markdown("Upload survey data to segment respondents into latent classes based on behavioral patterns.")

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

uploaded_file = st.file_uploader("Upload CSV or Excel file", type=["csv", "xlsx"])

if uploaded_file:
    df = pd.read_excel(uploaded_file) if uploaded_file.name.endswith("xlsx") else pd.read_csv(uploaded_file)
    st.success(f"Loaded {df.shape[0]} rows and {df.shape[1]} columns.")
    st.dataframe(df.head())

    input_cols = st.multiselect("Select numeric columns to use for segmentation", df.select_dtypes(include=np.number).columns)

    if input_cols and st.button("Run LCA Segmentation"):
        X = df[input_cols].dropna()

        n_classes = st.slider("Number of latent classes", 2, 6, 3)
        model = GaussianMixture(n_components=n_classes, random_state=42)
        labels = model.fit_predict(X)
        df["Segment"] = labels

        st.subheader("📊 Segment Summary")
        st.write(df["Segment"].value_counts())

        fig, ax = plt.subplots()
        df["Segment"].value_counts().sort_index().plot(kind="bar", ax=ax)
        ax.set_title("Segment Sizes")
        ax.set_xlabel("Segment")
        ax.set_ylabel("Count")
        st.pyplot(fig)

        means = df.groupby("Segment")[input_cols].mean()
        st.subheader("📈 Segment Profiles")
        st.dataframe(means)

        prompt = f"You are an insights analyst. Here are average profiles for each segment:\n{means.to_string()}"
        try:
            with st.spinner("GPT interpreting segment profiles..."):
                response = client.chat.completions.create(
                    model="gpt-3.5-turbo",
                    messages=[
                        {"role": "system", "content": prompt},
                        {"role": "user", "content": "Please summarize each segment and provide high-level interpretations."}
                    ]
                )
                st.subheader("💬 GPT Insight")
                st.markdown(response.choices[0].message.content)
        except Exception as e:
            st.error(f"GPT error: {e}")
