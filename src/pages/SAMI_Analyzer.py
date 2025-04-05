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
# INITIAL SETUP (CRITICAL FIXES)
# =============================================
st.set_page_config(
    page_title="SAMI Analyzer Pro",
    page_icon="🔍",
    layout="wide"
)

# Initialize session state FIRST
if 'df' not in st.session_state:
    st.session_state.df = None
if 'uploaded_file' not in st.session_state:
    st.session_state.uploaded_file = None

# =============================================
# GUARANTEED FILE UPLOADER
# =============================================
def load_data(uploaded_file):
    """Failsafe data loader"""
    try:
        if uploaded_file.name.endswith('.csv'):
            return pd.read_csv(uploaded_file)
        else:
            return pd.read_excel(uploaded_file, engine='openpyxl')
    except Exception as e:
        st.error(f"Failed to read file: {str(e)}")
        st.stop()

# =============================================
# MAIN INTERFACE (WITH UPLOAD FIXES)
# =============================================
st.title("🔍 SAMI AI - Advanced Analytics Suite")

# --- File Uploader with Fixes ---
uploaded_file = st.file_uploader(
    "**Upload your dataset (CSV/Excel)**",
    type=["csv", "xlsx"],
    key="guaranteed_uploader"
)

if uploaded_file:
    try:
        # Validate file
        if not uploaded_file.name:
            st.error("Invalid file - please re-upload")
            st.stop()
        
        # Store in session state
        st.session_state.uploaded_file = uploaded_file
        
        # Load with progress
        with st.spinner("Loading data..."):
            df = load_data(uploaded_file)
            st.session_state.df = df
            
        st.success(f"✅ Successfully loaded {len(df)} rows")
        st.dataframe(df.head(3))
        
    except Exception as e:
        st.error(f"Upload failed: {str(e)}")
        st.stop()

# --- Only show analysis options AFTER successful upload ---
if st.session_state.df is not None:
    df = st.session_state.df
    
    # Analysis Options
    st.subheader("🔍 Analysis Options")
    show_corr = st.checkbox("Correlation Matrix", True)
    show_dist = st.checkbox("Distributions", True)
    show_anomaly = st.checkbox("Anomaly Detection", True)
    
    # --- Analysis Execution ---
    if st.button("🚀 Run Analysis", type="primary"):
        with st.spinner("Analyzing..."):
            try:
                # 1. Basic Stats
                st.subheader("📊 Basic Statistics")
                st.dataframe(df.describe())
                
                # 2. Correlation Matrix (if enabled)
                if show_corr and df.select_dtypes(include=np.number).shape[1] > 1:
                    st.subheader("🔗 Correlation Matrix")
                    corr = df.select_dtypes(include=np.number).corr()
                    fig, ax = plt.subplots(figsize=(10, 8))
                    sns.heatmap(corr, annot=True, fmt=".2f", cmap="coolwarm", ax=ax)
                    st.pyplot(fig)
                
                # 3. Anomaly Detection (if enabled)
                if show_anomaly:
                    st.subheader("⚠️ Anomaly Report")
                    numeric_cols = df.select_dtypes(include=np.number).columns
                    if len(numeric_cols) > 0:
                        anomalies = pd.DataFrame()
                        for col in numeric_cols:
                            z_scores = stats.zscore(df[col].dropna())
                            outliers = df[(abs(z_scores) > 3)]
                            if not outliers.empty:
                                outliers['Anomaly_Type'] = f"{col} outlier (Z > 3)"
                                anomalies = pd.concat([anomalies, outliers])
                        
                        if not anomalies.empty:
                            st.dataframe(anomalies)
                        else:
                            st.success("No anomalies detected")
                    else:
                        st.warning("No numeric columns for anomaly detection")
                
                # 4. Distribution Plots (if enabled)
                if show_dist:
                    st.subheader("📈 Distributions")
                    numeric_cols = df.select_dtypes(include=np.number).columns
                    for col in numeric_cols[:3]:  # Show first 3 for demo
                        fig, ax = plt.subplots()
                        df[col].hist(ax=ax)
                        ax.set_title(f"Distribution of {col}")
                        st.pyplot(fig)
                
            except Exception as e:
                st.error(f"Analysis failed: {str(e)}")

# =============================================
# REQUIREMENTS.TXT (Must include these)
# =============================================
"""
streamlit>=1.28.0
pandas>=2.0.0
numpy>=1.24.0
scikit-learn>=1.0.0
scipy>=1.0.0
matplotlib>=3.7.0
seaborn>=0.12.0
openpyxl>=3.0.0  # Critical for Excel files
plotly>=5.0.0
fpdf2>=1.7.2
openai>=1.0.0
"""
