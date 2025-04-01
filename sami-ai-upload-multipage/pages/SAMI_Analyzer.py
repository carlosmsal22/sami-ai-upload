import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import os
from openai import OpenAI
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.decomposition import PCA
import seaborn as sns

st.set_page_config(page_title="SAMI Analyzer", layout="wide")
st.title("📊 SAMI AI – Advanced Analytical Tool")

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

uploaded_file = st.file_uploader("Upload your Excel or CSV file", type=["xlsx", "csv"])
user_prompt = st.text_area("Ask a question about your data:")

def parse_file(file):
    if file.name.endswith(".csv"):
        return pd.read_csv(file)
    elif file.name.endswith(".xlsx"):
        return pd.read_excel(file)
    else:
        return None

def summarize_data(df):
    st.subheader("📈 Summary Statistics")
    summary = df.describe(include='all').transpose()
    st.dataframe(summary)
    return summary.to_string()

def show_correlation(df):
    st.subheader("📊 Correlation Matrix")
    corr = df.select_dtypes(include='number').corr()
    st.dataframe(corr.round(2))
    fig, ax = plt.subplots()
    sns.heatmap(corr, annot=True, cmap="coolwarm", fmt=".2f", ax=ax)
    st.pyplot(fig)
    return corr.to_string()

def show_pca(df):
    st.subheader("🔎 PCA Visualization")
    numeric_cols = df.select_dtypes(include='number').dropna()
    if numeric_cols.shape[1] < 2:
        st.info("Need at least 2 numeric columns for PCA.")
        return ""
    from sklearn.preprocessing import StandardScaler
    scaled = StandardScaler().fit_transform(numeric_cols)
    pca = PCA(n_components=2)
    pcs = pca.fit_transform(scaled)
    explained_var = pca.explained_variance_ratio_
    fig, ax = plt.subplots()
    ax.scatter(pcs[:,0], pcs[:,1], alpha=0.6)
    ax.set_xlabel("PC1")
    ax.set_ylabel("PC2")
    st.pyplot(fig)
    return f"PCA Explained Variance: PC1={explained_var[0]:.2%}, PC2={explained_var[1]:.2%}"

def show_tfidf(df):
    st.subheader("🧠 TF-IDF")
    text_cols = df.select_dtypes(include='object').columns
    if len(text_cols) == 0:
        st.info("No text columns found.")
        return
    col = st.selectbox("Select text column", text_cols)
    vec = TfidfVectorizer(max_features=15)
    tfidf_matrix = vec.fit_transform(df[col].fillna("").astype(str))
    tfidf_df = pd.DataFrame(tfidf_matrix.toarray(), columns=vec.get_feature_names_out())
    st.dataframe(tfidf_df)

if uploaded_file and st.button("Analyze"):
    df = parse_file(uploaded_file)
    st.success("File uploaded and parsed.")
    show_tfidf(df)
    summary = summarize_data(df)
    corr = show_correlation(df)
    pca = show_pca(df)

    system_prompt = f"You are SAMI AI, an analytics assistant. Summary:\n{summary}\nCorrelation:\n{corr}\n{pca}"
    try:
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt}
            ]
        )
        st.subheader("💬 GPT Insight")
        st.markdown(response.choices[0].message.content)
    except Exception as e:
        st.error(f"API Error: {e}")
