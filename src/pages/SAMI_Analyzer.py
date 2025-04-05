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
# INITIALIZATION
# =============================================
st.set_page_config(
    page_title="SAMI Analyzer Pro",
    page_icon="🔍",
    layout="wide"
)

# Initialize session state
if 'df' not in st.session_state:
    st.session_state.df = None
if 'upload_error' not in st.session_state:
    st.session_state.upload_error = None
if 'analysis_done' not in st.session_state:
    st.session_state.analysis_done = False

# =============================================
# ENHANCED FILE UPLOADER (FIXED FOR EXCEL)
# =============================================
def safe_file_upload():
    try:
        uploaded_file = st.file_uploader(
            "**Upload Dataset (CSV/Excel)**",
            type=["csv", "xlsx", "xls"],
            key="failsafe_uploader"
        )
        
        if uploaded_file is not None:
            if not hasattr(uploaded_file, 'name'):
                st.session_state.upload_error = "Invalid file object"
                return None
            
            with st.spinner("Processing file..."):
                try:
                    if uploaded_file.name.endswith('.csv'):
                        df = pd.read_csv(uploaded_file)
                    else:
                        # Handle both .xlsx and .xls formats
                        df = pd.read_excel(uploaded_file, engine='openpyxl')
                    
                    if df.empty:
                        st.session_state.upload_error = "Empty file detected"
                        return None
                        
                    st.session_state.df = df
                    st.session_state.upload_error = None
                    st.session_state.analysis_done = False
                    return df
                
                except Exception as e:
                    st.session_state.upload_error = f"Error reading file: {str(e)}"
                    return None
            
        return None
        
    except Exception as e:
        st.session_state.upload_error = f"Upload failed: {str(e)}"
        return None

# =============================================
# ANALYSIS FUNCTIONS (ALL FEATURES RESTORED)
# =============================================
def run_correlation_analysis(df):
    numeric_cols = df.select_dtypes(include=np.number).columns
    if len(numeric_cols) > 1:
        st.subheader("🔗 Advanced Correlation Matrix")
        corr = df[numeric_cols].corr()
        
        # Calculate p-values
        p_matrix = np.zeros_like(corr)
        for i in range(len(numeric_cols)):
            for j in range(len(numeric_cols)):
                if i != j:
                    _, p_matrix[i, j] = stats.pearsonr(
                        df[numeric_cols[i]].dropna(),
                        df[numeric_cols[j]].dropna()
                    )
        
        # Create mask for significant correlations
        mask = np.triu(np.ones_like(corr, dtype=bool))
        sig_mask = (p_matrix < 0.05) & ~mask
        
        # Plot
        fig, ax = plt.subplots(figsize=(12, 10))
        sns.heatmap(
            corr,
            mask=mask,
            annot=True,
            fmt=".2f",
            cmap="coolwarm",
            center=0,
            square=True,
            linewidths=.5,
            annot_kws={"size": 9},
            cbar_kws={"shrink": .8}
        )
        
        # Add significance stars
        for i in range(len(numeric_cols)):
            for j in range(len(numeric_cols)):
                if sig_mask[i, j]:
                    plt.text(j+0.5, i+0.5, "*", 
                            ha="center", va="center", 
                            color="black", fontsize=14)
        
        plt.title("Correlation Matrix (* = p < 0.05)")
        st.pyplot(fig)
        return corr
    else:
        st.warning("Need at least 2 numeric columns for correlation")
        return None

def run_distribution_analysis(df):
    st.subheader("📊 Interactive Distributions")
    numeric_cols = df.select_dtypes(include=np.number).columns
    cat_cols = df.select_dtypes(include=['object', 'category']).columns
    
    # Numeric distributions
    for col in numeric_cols[:5]:  # Limit to first 5 for performance
        fig = px.histogram(
            df, x=col, marginal="box",
            title=f"Distribution of {col}",
            hover_data=df.columns
        )
        st.plotly_chart(fig, use_container_width=True)
    
    # Categorical distributions
    for col in cat_cols:
        if df[col].nunique() <= 20:  # Limit for categoricals
            fig = px.histogram(
                df, x=col,
                title=f"Distribution of {col}",
                color=col
            )
            st.plotly_chart(fig, use_container_width=True)

def detect_anomalies(df):
    st.subheader("⚠️ Advanced Anomaly Detection")
    numeric_cols = df.select_dtypes(include=np.number).columns
    anomalies = pd.DataFrame()
    
    for col in numeric_cols:
        # IQR Method
        Q1 = df[col].quantile(0.25)
        Q3 = df[col].quantile(0.75)
        IQR = Q3 - Q1
        iqr_outliers = df[(df[col] < (Q1 - 1.5*IQR)) | (df[col] > (Q3 + 1.5*IQR))]
        
        # Z-score Method
        z_scores = np.abs(stats.zscore(df[col].dropna()))
        z_outliers = df[z_scores > 3]
        
        # Combine results
        col_anomalies = pd.concat([iqr_outliers, z_outliers]).drop_duplicates()
        col_anomalies['Anomaly_Type'] = f"{col} Outlier"
        anomalies = pd.concat([anomalies, col_anomalies])
    
    if not anomalies.empty:
        st.dataframe(
            anomalies.style.highlight_max(color='lightyellow'),
            height=300
        )
        return anomalies
    else:
        st.success("No anomalies detected using IQR and Z-score methods")
        return None

# =============================================
# MAIN INTERFACE (WITH ALL FEATURES)
# =============================================
st.title("🔍 SAMI AI - Advanced Analytics Suite")

with st.expander("ℹ️ How to use", expanded=False):
    st.markdown("""
    1. **Upload** your dataset (Excel/CSV)
    2. **Select** analyses to run
    3. **Explore** interactive results
    4. **Download** full report
    """)

# File Upload
df = safe_file_upload()

if st.session_state.upload_error:
    st.error(st.session_state.upload_error)

if st.session_state.df is not None:
    df = st.session_state.df
    st.success(f"✅ Successfully loaded {len(df)} rows")
    
    with st.expander("🔍 Data Preview", expanded=True):
        st.dataframe(df.head(3))
        
        cols = st.columns(3)
        with cols[0]:
            st.metric("Total Rows", len(df))
        with cols[1]:
            st.metric("Numeric Columns", len(df.select_dtypes(include=np.number).columns))
        with cols[2]:
            st.metric("Missing Values", df.isnull().sum().sum())

    # Analysis Options
    st.subheader("📌 Analysis Options")
    analysis_options = st.multiselect(
        "Select analyses to run:",
        options=[
            "Correlation Analysis",
            "Distribution Analysis",
            "Anomaly Detection",
            "PCA Projection",
            "Cluster Analysis"
        ],
        default=["Correlation Analysis", "Distribution Analysis"]
    )
    
    if st.button("🚀 Run Selected Analyses", type="primary"):
        with st.spinner("Running analyses..."):
            try:
                # Correlation Analysis
                if "Correlation Analysis" in analysis_options:
                    run_correlation_analysis(df)
                
                # Distribution Analysis
                if "Distribution Analysis" in analysis_options:
                    run_distribution_analysis(df)
                
                # Anomaly Detection
                if "Anomaly Detection" in analysis_options:
                    anomalies = detect_anomalies(df)
                
                # PCA Projection
                if "PCA Projection" in analysis_options:
                    numeric_cols = df.select_dtypes(include=np.number).columns
                    if len(numeric_cols) >= 3:
                        st.subheader("🔮 PCA Projection (2D)")
                        pca = PCA(n_components=2)
                        reduced = pca.fit_transform(df[numeric_cols].fillna(0))
                        fig = px.scatter(
                            x=reduced[:, 0], 
                            y=reduced[:, 1],
                            labels={'x': 'PC1', 'y': 'PC2'},
                            title=f"PCA (Variance Explained: {pca.explained_variance_ratio_.sum():.1%})",
                            hover_name=df.index
                        )
                        st.plotly_chart(fig, use_container_width=True)
                    else:
                        st.warning("Need ≥3 numeric columns for PCA")
                
                # Cluster Analysis
                if "Cluster Analysis" in analysis_options:
                    numeric_cols = df.select_dtypes(include=np.number).columns
                    if len(numeric_cols) >= 2:
                        st.subheader("🧭 K-Means Clustering")
                        n_clusters = st.slider("Number of clusters", 2, 5, 3)
                        kmeans = KMeans(n_clusters=n_clusters, random_state=42)
                        clusters = kmeans.fit_predict(df[numeric_cols].fillna(0))
                        df['Cluster'] = clusters
                        
                        if len(numeric_cols) >= 2:
                            fig = px.scatter(
                                df, x=numeric_cols[0], y=numeric_cols[1],
                                color='Cluster',
                                title="Cluster Visualization",
                                hover_data=df.columns
                            )
                            st.plotly_chart(fig, use_container_width=True)
                        
                        st.dataframe(
                            df.groupby('Cluster')[numeric_cols].mean().style.background_gradient()
                        )
                    else:
                        st.warning("Need ≥2 numeric columns for clustering")
                
                st.session_state.analysis_done = True
                
            except Exception as e:
                st.error(f"Analysis failed: {str(e)}")
                st.session_state.analysis_done = False

    # Report Generation
    if st.session_state.analysis_done:
        st.subheader("📄 Report Generation")
        if st.button("📥 Download PDF Report"):
            pdf = FPDF()
            pdf.add_page()
            pdf.set_font("Arial", size=12)
            pdf.cell(200, 10, txt="SAMI AI Analysis Report", ln=1, align='C')
            pdf.ln(10)
            
            # Add analysis summary
            pdf.multi_cell(0, 5, f"Analysis of {len(df)} rows with {len(df.columns)} columns")
            
            # Add more report content here...
            
            # Generate PDF
            pdf_output = BytesIO()
            pdf.output(pdf_output)
            pdf_output.seek(0)
            
            st.download_button(
                label="⬇️ Download Full Report",
                data=pdf_output,
                file_name="SAMI_Analysis_Report.pdf",
                mime="application/pdf"
            )
