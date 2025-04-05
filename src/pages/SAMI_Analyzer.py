import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.decomposition import PCA
from sklearn.cluster import KMeans
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.ensemble import RandomForestRegressor
from scipy import stats
import os
from openai import OpenAI
from io import BytesIO
from datetime import datetime
from fpdf import FPDF
import plotly.express as px

# =============================================
# INITIALIZATION (CRITICAL FOR UPLOADS)
# =============================================
st.set_page_config(
    page_title="SAMI Analyzer Pro",
    page_icon="🔍",
    layout="wide"
)

# Initialize all session state variables FIRST
if 'df' not in st.session_state:
    st.session_state.df = None
if 'upload_error' not in st.session_state:
    st.session_state.upload_error = None

# =============================================
# FAILSAFE FILE UPLOADER
# =============================================
def safe_file_upload():
    """Guaranteed-working file upload handler"""
    try:
        uploaded_file = st.file_uploader(
            "**Upload Dataset (CSV/Excel)**",
            type=["csv", "xlsx"],
            key="failsafe_uploader"
        )
        
        if uploaded_file is not None:
            # Validate file object
            if not hasattr(uploaded_file, 'name'):
                st.session_state.upload_error = "Invalid file object"
                return None
            
            # Read based on file type
            with st.spinner("Processing file..."):
                if uploaded_file.name.endswith('.csv'):
                    df = pd.read_csv(uploaded_file)
                else:
                    df = pd.read_excel(uploaded_file, engine='openpyxl')
            
            # Basic validation
            if df.empty:
                st.session_state.upload_error = "Empty file detected"
                return None
                
            st.session_state.df = df
            st.session_state.upload_error = None
            return df
            
        return None
        
    except Exception as e:
        st.session_state.upload_error = str(e)
        return None

# =============================================
# MAIN INTERFACE
# =============================================
st.title("🔍 SAMI AI - Advanced Analytics Suite")

# --- File Upload Section ---
df = safe_file_upload()

if st.session_state.upload_error:
    st.error(f"Upload error: {st.session_state.upload_error}")

if st.session_state.df is not None:
    df = st.session_state.df
    st.success(f"✅ Successfully loaded {len(df)} rows")
    st.dataframe(df.head(3))
    
    # --- Analysis Options ---
    st.subheader("🔍 Analysis Options")
    col1, col2 = st.columns(2)
    with col1:
        show_corr = st.checkbox("Correlation Matrix", True)
        show_dist = st.checkbox("Distributions", True)
    with col2:
        show_anomaly = st.checkbox("Anomaly Detection", True)
        show_pca = st.checkbox("PCA Projection")
    
    # --- Run Analysis ---
    if st.button("🚀 Run Analysis", type="primary"):
        with st.spinner("Analyzing data..."):
            try:
                # 1. Basic Stats
                st.subheader("📊 Descriptive Statistics")
                st.dataframe(df.describe())
                
                # 2. Correlation Matrix
                if show_corr:
                    numeric_cols = df.select_dtypes(include=np.number).columns
                    if len(numeric_cols) > 1:
                        st.subheader("🔗 Correlation Matrix")
                        corr = df[numeric_cols].corr()
                        fig, ax = plt.subplots(figsize=(10, 8))
                        sns.heatmap(
                            corr, 
                            annot=True, 
                            fmt=".2f", 
                            cmap="coolwarm",
                            center=0,
                            annot_kws={"size": 9}
                        )
                        st.pyplot(fig)
                    else:
                        st.warning("Need at least 2 numeric columns for correlation")
                
                # 3. Distributions
                if show_dist:
                    st.subheader("📈 Feature Distributions")
                    numeric_cols = df.select_dtypes(include=np.number).columns
                    for col in numeric_cols[:3]:  # Limit to 3 for demo
                        fig, ax = plt.subplots()
                        df[col].hist(ax=ax, bins=20)
                        ax.set_title(f"Distribution of {col}")
                        st.pyplot(fig)
                
                # 4. Anomaly Detection
                if show_anomaly:
                    st.subheader("⚠️ Anomaly Report")
                    numeric_cols = df.select_dtypes(include=np.number).columns
                    anomalies = pd.DataFrame()
                    
                    for col in numeric_cols:
                        # Z-score method
                        z_scores = np.abs(stats.zscore(df[col].dropna()))
                        outliers = df[z_scores > 3]
                        if not outliers.empty:
                            outliers['Anomaly_Type'] = f"{col} (Z > 3)"
                            anomalies = pd.concat([anomalies, outliers])
                    
                    if not anomalies.empty:
                        st.dataframe(anomalies)
                    else:
                        st.success("No anomalies detected (Z > 3)")
                
                # 5. PCA
                if show_pca:
                    numeric_cols = df.select_dtypes(include=np.number).columns
                    if len(numeric_cols) >= 3:
                        st.subheader("🔮 PCA Projection (2D)")
                        pca = PCA(n_components=2)
                        reduced = pca.fit_transform(df[numeric_cols].fillna(0))
                        fig = px.scatter(
                            x=reduced[:, 0], 
                            y=reduced[:, 1],
                            labels={'x': 'PC1', 'y': 'PC2'},
                            title=f"PCA (Explained Variance: {pca.explained_variance_ratio_.sum():.1%})"
                        )
                        st.plotly_chart(fig)
                    else:
                        st.warning("Need ≥3 numeric columns for PCA")
                        
            except Exception as e:
                st.error(f"Analysis error: {str(e)}")

# =============================================
# DEPENDENCY NOTES (Must include in requirements.txt)
# =============================================
"""
streamlit>=1.28.0
pandas>=2.0.0
numpy>=1.24.0
scikit-learn>=1.0.0
scipy>=1.0.0
matplotlib>=3.7.0
seaborn>=0.12.0
openpyxl>=3.0.0  # Critical for Excel support
plotly>=5.0.0
fpdf2>=1.7.2
openai>=1.0.0
"""
