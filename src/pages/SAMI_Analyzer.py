import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.decomposition import PCA
from sklearn.cluster import KMeans
from sklearn.ensemble import RandomForestRegressor
from scipy import stats
import os
from openai import OpenAI
from io import BytesIO
from datetime import datetime
from fpdf import FPDF
import plotly.express as px

# === CONFIG ===
st.set_page_config(page_title="SAMI Analyzer Pro", page_icon="🔍", layout="wide")
st.title("🔍 SAMI AI - Advanced Analytics Suite")
st.caption("Upload your dataset and discover actionable insights")

# === STYLING ===
st.markdown("""
<style>
[data-testid="stFileUploader"] {
    border: 2px dashed #4e8cff;
    border-radius: 8px;
    padding: 20px;
}
[data-testid="stExpander"] details summary p {
    font-weight: 600 !important;
}
</style>
""", unsafe_allow_html=True)

# === SESSION ===
if 'df' not in st.session_state:
    st.session_state.df = None
if 'openai_error' not in st.session_state:
    st.session_state.openai_error = None

# === INIT OPENAI ===
try:
    client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
except Exception as e:
    st.session_state.openai_error = f"OpenAI init error: {str(e)}"
    client = None

# === SIDEBAR ===
with st.sidebar:
    st.title("⚙️ Analysis Settings")
    analysis_mode = st.radio("**Analysis Mode**", ["Basic EDA", "Advanced Insights", "Predictive Modeling"])
    with st.expander("Advanced Options"):
        confidence_level = st.slider("Confidence Level", 0.8, 0.99, 0.95)
        max_categories = st.number_input("Max Categories", 5, 100, 20)

# === FILE UPLOAD ===
uploaded_file = st.file_uploader("📁 Upload your dataset", type=["csv", "xlsx"])
user_prompt = st.text_area("💬 Ask a question about your data:", placeholder="E.g. What are the key drivers of satisfaction?")

col1, col2, col3 = st.columns(3)
with col1:
    show_corr = st.checkbox("🔗 Correlation Matrix", True)
    show_dist = st.checkbox("📊 Distributions", True)
with col2:
    show_pca = st.checkbox("🔮 PCA Projection")
    show_cluster = st.checkbox("🧭 Clustering")
with col3:
    show_tfidf = st.checkbox("📝 Text Analysis (Coming Soon)", False)
    show_anomaly = st.checkbox("⚠️ Anomaly Detection", True)

# === HELP ===
with st.expander("ℹ️ How to use this tool", expanded=False):
    st.markdown("""
**Steps:**
1. Upload your dataset
2. Select analysis options
3. Click "Run Analysis"
4. Explore results
5. Download insights

**Try prompts like:**
- What drives NPS by region?
- What are unexpected patterns?
- How do clusters differ demographically?
""")

# === HELPERS ===
@st.cache_data
def load_data(file):
    try:
        return pd.read_csv(file) if file.name.endswith(".csv") else pd.read_excel(file)
    except Exception as e:
        st.error(f"❌ File error: {e}")
        return None

def detect_anomalies(df):
    numeric_cols = df.select_dtypes(include=np.number).columns
    outliers = pd.DataFrame()
    for col in numeric_cols:
        Q1 = df[col].quantile(0.25)
        Q3 = df[col].quantile(0.75)
        IQR = Q3 - Q1
        mask = (df[col] < Q1 - 1.5 * IQR) | (df[col] > Q3 + 1.5 * IQR)
        z_scores = np.abs(stats.zscore(df[col].dropna()))
        z_outliers = df.loc[(z_scores > 3).values]
        iqr_outliers = df[mask]
        outliers = pd.concat([outliers, iqr_outliers, z_outliers])
    return outliers.drop_duplicates()

def generate_visuals(df):
    if show_dist:
        st.subheader("📊 Feature Distributions")
        for col in df.select_dtypes(include=np.number).columns[:5]:
            fig = px.histogram(df, x=col, marginal="box", title=col)
            st.plotly_chart(fig, use_container_width=True)

    if show_corr:
        st.subheader("🔗 Correlation Matrix")
        corr = df.select_dtypes(include=np.number).corr()
        fig = px.imshow(corr, text_auto=".2f", color_continuous_scale="RdBu", range_color=[-1, 1])
        st.plotly_chart(fig, use_container_width=True)

    if show_pca and len(df.select_dtypes(include=np.number).columns) >= 3:
        st.subheader("🔮 PCA Projection")
        pca = PCA(n_components=2)
        proj = pca.fit_transform(df.select_dtypes(include=np.number).dropna())
        fig = px.scatter(x=proj[:, 0], y=proj[:, 1], title="2D PCA Projection", labels={'x': "PC1", 'y': "PC2"})
        st.plotly_chart(fig, use_container_width=True)

# === MAIN ANALYSIS ===
def run_analysis(df):
    with st.expander("📋 Data Overview", expanded=True):
        c1, c2, c3 = st.columns(3)
        c1.metric("Rows", df.shape[0])
        c2.metric("Columns", df.shape[1])
        c3.metric("Missing %", f"{df.isnull().mean().mean()*100:.1f}%")
        st.dataframe(df.head(3))

    generate_visuals(df)

    if show_anomaly:
        anomalies = detect_anomalies(df)
        if not anomalies.empty:
            st.warning(f"⚠️ {len(anomalies)} anomalies detected")
            with st.expander("View Anomalies"):
                st.dataframe(anomalies)

    if client:
        try:
            try:
                desc = df.describe().to_markdown()
            except:
                desc = df.describe().to_string()

            summary = f"""
Data shape: {df.shape}
Columns: {list(df.columns)}
Stats:
{desc}
"""

            with st.spinner("🧠 Generating AI insights..."):
                response = client.chat.completions.create(
                    model="gpt-3.5-turbo",
                    messages=[
                        {"role": "system", "content": "You're a senior data analyst. Focus on: key patterns, implications, next steps."},
                        {"role": "user", "content": f"{user_prompt or 'Analyze this dataset'}:\n{summary}"}
                    ]
                )
                answer = response.choices[0].message.content
                st.subheader("💡 GPT Insights")
                st.markdown(answer)

                pdf = FPDF()
                pdf.add_page()
                pdf.set_font("Arial", size=10)
                pdf.multi_cell(0, 5, answer)
                buffer = BytesIO()
                pdf.output(buffer)
                buffer.seek(0)
                st.download_button("📄 Download PDF", buffer, file_name="SAMI_Insights.pdf", mime="application/pdf")

        except Exception as e:
            st.error(f"GPT error: {e}")
    else:
        st.info("GPT not initialized")

# === EXECUTION ===
if st.button("🚀 Run Analysis") and uploaded_file:
    df = load_data(uploaded_file)
    if df is not None:
        st.session_state.df = df
        run_analysis(df)
elif uploaded_file and st.session_state.df is not None:
    st.info("📌 File already loaded. Click 'Run Analysis' again to reprocess.")

