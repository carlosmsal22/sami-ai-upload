mport streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.decomposition import PCA
from sklearn.cluster import KMeans
from sklearn.feature_extraction.text import TfidfVectorizer
import os
from openai import OpenAI

st.set_page_config(page_title="SAMI Analyzer", layout="wide")
st.title("📊 SAMI AI – Advanced Analytical Tool")

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

uploaded_file = st.file_uploader("Upload your Excel or CSV file", type=["xlsx", "csv"])
user_prompt = st.text_area("Ask a question about your data:", placeholder="e.g. What are the top trends by region?")

show_corr = st.checkbox("🔗 Correlation Matrix")
show_pca = st.checkbox("🔬 PCA (2D Projection)")
show_cluster = st.checkbox("🧭 KMeans Clustering")
show_tfidf = st.checkbox("📝 TF-IDF on Text Columns")

def describe_columns(df):
    report = []
    for col in df.columns:
        col_type = df[col].dtype
        missing = df[col].isnull().mean()
        unique = df[col].nunique()
        if col_type == 'object':
            top_values = df[col].value_counts().head(3).to_dict()
            summary = f"Text | Unique: {unique} | Top: {top_values} | Missing: {missing:.1%}"
        elif np.issubdtype(col_type, np.number):
            desc = df[col].describe()
            summary = f"Numeric | Mean: {desc['mean']:.2f} | Std: {desc['std']:.2f} | Min: {desc['min']:.2f} | Max: {desc['max']:.2f} | Missing: {missing:.1%}"
        else:
            summary = f"{col_type} | Unique: {unique} | Missing: {missing:.1%}"
        report.append(f"- {col}: {summary}")
    return "\n".join(report)

def generate_visuals(df):
    st.subheader("📊 Auto-Generated Visualizations")
    numeric_cols = df.select_dtypes(include=np.number).columns
    categorical_cols = df.select_dtypes(include='object').columns

    for col in numeric_cols:
        fig, ax = plt.subplots()
        df[col].dropna().hist(ax=ax, bins=20)
        ax.set_title(f"Histogram of {col}")
        st.pyplot(fig)

    for col in categorical_cols:
        if df[col].nunique() <= 20:
            fig, ax = plt.subplots()
            df[col].value_counts().plot(kind="bar", ax=ax)
            ax.set_title(f"Bar Plot of {col}")
            st.pyplot(fig)

    if show_corr and len(numeric_cols) >= 2:
        st.subheader("🔗 Correlation Matrix")
        corr = df[numeric_cols].corr()
        fig, ax = plt.subplots(figsize=(8, 5))
        sns.heatmap(corr, annot=True, fmt=".2f", cmap="coolwarm", ax=ax)
        st.pyplot(fig)

    if show_pca and len(numeric_cols) >= 2:
        st.subheader("🔬 PCA Projection (First 2 Components)")
        pca = PCA(n_components=2)
        reduced = pca.fit_transform(df[numeric_cols].dropna())
        fig, ax = plt.subplots()
        ax.scatter(reduced[:, 0], reduced[:, 1])
        ax.set_xlabel("PC1")
        ax.set_ylabel("PC2")
        st.pyplot(fig)

    if show_cluster and len(numeric_cols) >= 2:
        st.subheader("🧭 KMeans Clustering (k=3)")
        km = KMeans(n_clusters=3, random_state=42)
        clusters = km.fit_predict(df[numeric_cols].dropna())
        df['Cluster'] = clusters
        fig, ax = plt.subplots()
        sns.scatterplot(x=df[numeric_cols].iloc[:, 0], y=df[numeric_cols].iloc[:, 1], hue=clusters, palette="viridis", ax=ax)
        st.pyplot(fig)

    if show_tfidf:
        text_cols = df.select_dtypes(include='object').columns
        for col in text_cols:
            st.subheader(f"📝 TF-IDF Terms: {col}")
            text_data = df[col].dropna().astype(str)
            if len(text_data) > 0:
                vectorizer = TfidfVectorizer(max_features=10, stop_words='english')
                tfidf = vectorizer.fit_transform(text_data)
                terms = vectorizer.get_feature_names_out()
                scores = tfidf.sum(axis=0).A1
                top_terms = pd.Series(scores, index=terms).sort_values(ascending=False)
                st.bar_chart(top_terms)

if uploaded_file and st.button("Analyze"):
    try:
        df = pd.read_csv(uploaded_file) if uploaded_file.name.endswith(".csv") else pd.read_excel(uploaded_file)
        st.success(f"Loaded {df.shape[0]} rows × {df.shape[1]} columns")
        st.dataframe(df.head())

        st.subheader("📑 Column Summary")
        column_summary = describe_columns(df)
        st.text(column_summary)

        generate_visuals(df)

        system_prompt = (
            f"You are SAMI AI, a senior data analyst. Below is an overview of a dataset with {df.shape[0]} rows and {df.shape[1]} columns.\n"
            f"Column breakdown:\n{column_summary}\n"
            f"Please analyze the dataset using best practices for exploratory data analysis (EDA) "
            f"and answer the user’s question or provide general insights."
        )

        with st.spinner("GPT is analyzing your dataset..."):
            response = client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_prompt or "Please summarize the dataset and highlight key insights."}
                ]
            )
            st.subheader("💬 GPT Insight")
            st.markdown(response.choices[0].message.content)

    except Exception as e:
        st.error(f"Error: {e}")
