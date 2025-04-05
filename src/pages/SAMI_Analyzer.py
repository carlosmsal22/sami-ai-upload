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
import plotly.express as px  # New for interactive plots

# Configuration
st.set_page_config(page_title="SAMI Analyzer Pro", layout="wide", page_icon="🔍")
st.title("🔍 SAMI AI – Advanced Insights Engine with Automated Reporting")

# Initialize client
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# =============================================
# NEW: Enhanced UI Components
# =============================================
with st.sidebar:
    st.header("Analysis Configuration")
    analysis_mode = st.radio(
        "Mode:",
        ["Exploratory", "Diagnostic", "Predictive"],
        help="Exploratory: Basic stats\nDiagnostic: Deep insights\nPredictive: ML modeling"
    )
    
    advanced_options = st.expander("Advanced Options")
    with advanced_options:
        confidence_level = st.slider("Confidence Level", 0.8, 0.99, 0.95)
        max_categories = st.number_input("Max Categories for Plots", 10, 50, 20)
        random_state = st.number_input("Random Seed", 1, 1000, 42)

# =============================================
# Enhanced Data Processing Functions
# =============================================
def detect_anomalies(df):
    """Automatically detect outliers using IQR and Z-score methods"""
    numeric_cols = df.select_dtypes(include=np.number).columns
    anomalies = pd.DataFrame()
    
    for col in numeric_cols:
        # IQR Method
        Q1 = df[col].quantile(0.25)
        Q3 = df[col].quantile(0.75)
        IQR = Q3 - Q1
        iqr_outliers = df[(df[col] < (Q1 - 1.5*IQR)) | (df[col] > (Q3 + 1.5*IQR))]
        
        # Z-score Method
        z_scores = stats.zscore(df[col].dropna())
        z_outliers = df[(abs(z_scores) > 3)]
        
        # Combine
        col_anomalies = pd.concat([iqr_outliers, z_outliers]).drop_duplicates()
        col_anomalies['Anomaly_Type'] = f"{col} Outlier"
        anomalies = pd.concat([anomalies, col_anomalies])
    
    return anomalies.drop_duplicates()

def feature_importance_analysis(df, target_col=None):
    """Calculate feature importance using Random Forest"""
    numeric_cols = df.select_dtypes(include=np.number).columns
    
    if target_col and target_col in numeric_cols:
        # Supervised importance
        X = df[numeric_cols].drop(columns=[target_col]).fillna(0)
        y = df[target_col]
        
        model = RandomForestRegressor(random_state=random_state)
        model.fit(X, y)
        importance = pd.DataFrame({
            'Feature': X.columns,
            'Importance': model.feature_importances_
        }).sort_values('Importance', ascending=False)
        
        return importance, "supervised"
    else:
        # Unsupervised importance (variance)
        importance = pd.DataFrame({
            'Feature': numeric_cols,
            'Importance': df[numeric_cols].var().values
        }).sort_values('Importance', ascending=False)
        
        return importance, "unsupervised"

# =============================================
# SUPERCHARGED Visualization Functions
# =============================================
def enhanced_correlation_analysis(df):
    """Interactive correlation matrix with statistical significance"""
    numeric_cols = df.select_dtypes(include=np.number).columns
    
    # Calculate correlation and p-values
    corr_matrix = pd.DataFrame(index=numeric_cols, columns=numeric_cols)
    p_matrix = pd.DataFrame(index=numeric_cols, columns=numeric_cols)
    
    for i in numeric_cols:
        for j in numeric_cols:
            corr, p_value = stats.pearsonr(df[i].dropna(), df[j].dropna())
            corr_matrix.loc[i,j] = corr
            p_matrix.loc[i,j] = p_value
    
    # Create mask for significant correlations
    mask = np.triu(np.ones_like(corr_matrix, dtype=bool))
    sig_mask = (p_matrix < (1-confidence_level)) & ~mask
    
    # Plot
    plt.figure(figsize=(12,8))
    sns.heatmap(
        corr_matrix.astype(float), 
        mask=mask,
        annot=True, 
        fmt=".2f", 
        cmap="coolwarm",
        center=0,
        annot_kws={"size":9},
        cbar_kws={"shrink":0.8}
    )
    
    # Highlight significant correlations
    for i in range(len(numeric_cols)):
        for j in range(len(numeric_cols)):
            if sig_mask.iloc[i,j]:
                plt.text(j+0.5, i+0.5, "*", 
                        ha="center", va="center", 
                        color="black", fontsize=14)
    
    plt.title(f"Correlation Matrix (∗ = p < {1-confidence_level:.2f})")
    st.pyplot(plt.gcf())
    plt.clf()
    
    return corr_matrix, p_matrix

def interactive_distribution_plots(df):
    """Plotly interactive distribution visualizations"""
    numeric_cols = df.select_dtypes(include=np.number).columns
    
    for col in numeric_cols:
        fig = px.histogram(
            df, 
            x=col,
            nbins=50,
            marginal="box",
            title=f"Distribution of {col}",
            hover_data=df.columns
        )
        st.plotly_chart(fig, use_container_width=True)

# =============================================
# MAIN ANALYSIS PIPELINE
# =============================================
uploaded_file = st.file_uploader("Upload your dataset", type=["xlsx", "csv", "parquet"])
user_prompt = st.text_area("What insights would you like to discover?", 
                          placeholder="E.g.: What are the key drivers of customer satisfaction?")

if uploaded_file and st.button("🚀 Analyze Data", type="primary"):
    with st.spinner("Crunching numbers..."):
        try:
            # Load data
            df = pd.read_csv(uploaded_file) if uploaded_file.name.endswith(".csv") else pd.read_excel(uploaded_file)
            st.success(f"✅ Loaded {df.shape[0]:,} rows × {df.shape[1]:,} columns")
            
            # Data Quality Report
            with st.expander("🔍 Data Quality Report", expanded=True):
                missing_data = df.isnull().sum().rename("Missing Values")
                data_types = df.dtypes.rename("Data Type")
                uniqueness = df.nunique().rename("Unique Values")
                quality_report = pd.concat([data_types, missing_data, uniqueness], axis=1)
                st.dataframe(quality_report.style.background_gradient(cmap="Reds", subset=["Missing Values"]))
            
            # Automated Anomaly Detection
            anomalies = detect_anomalies(df)
            if not anomalies.empty:
                st.warning(f"⚠️ Detected {len(anomalies)} potential anomalies")
                with st.expander("View Anomalies"):
                    st.dataframe(anomalies)
            
            # Enhanced Correlation Analysis
            if len(df.select_dtypes(include=np.number).columns) >= 2:
                st.subheader("🔗 Advanced Correlation Analysis")
                corr_matrix, p_matrix = enhanced_correlation_analysis(df)
            
            # Interactive Distributions
            st.subheader("📊 Interactive Distributions")
            interactive_distribution_plots(df)
            
            # Feature Importance
            numeric_cols = df.select_dtypes(include=np.number).columns
            if len(numeric_cols) > 1:
                st.subheader("🏆 Feature Importance")
                target = st.selectbox("Select target variable (optional)", [None] + list(numeric_cols))
                importance, imp_type = feature_importance_analysis(df, target)
                
                fig, ax = plt.subplots(figsize=(10,6))
                sns.barplot(
                    data=importance.head(10),
                    x="Importance",
                    y="Feature",
                    palette="viridis",
                    ax=ax
                )
                ax.set_title(f"Top 10 {'Predictive' if imp_type == 'supervised' else 'Variance-Based'} Features")
                st.pyplot(fig)
            
            # GPT-4 Turbo Insight Generation
            with st.spinner("🧠 Generating strategic insights..."):
                # Prepare data summary for GPT
                data_summary = f"""
                Dataset Shape: {df.shape}
                Columns: {', '.join(df.columns)}
                Numeric Columns: {', '.join(df.select_dtypes(include=np.number).columns)}
                Categorical Columns: {', '.join(df.select_dtypes(include='object').columns)}
                
                Sample Data:
                {df.head(3).to_markdown()}
                
                Key Statistics:
                {df.describe().to_markdown()}
                """
                
                response = client.chat.completions.create(
                    model="gpt-4-turbo",
                    messages=[
                        {
                            "role": "system", 
                            "content": """You are SAMI AI, an advanced analytics assistant. Analyze this dataset and provide:
                            1. Key patterns and relationships
                            2. Business implications
                            3. Recommended next steps
                            4. Potential pitfalls"""
                        },
                        {
                            "role": "user",
                            "content": f"Data Summary:\n{data_summary}\n\nUser Question: {user_prompt or 'Provide comprehensive analysis'}"
                        }
                    ],
                    temperature=0.7,
                    max_tokens=2000
                )
                
                insights = response.choices[0].message.content
                
                st.subheader("💡 Strategic Insights")
                st.markdown(insights)
                
                # PDF Report Generation
                pdf = FPDF()
                pdf.add_page()
                pdf.set_font("Arial", size=12)
                pdf.cell(200, 10, txt="SAMI AI Analysis Report", ln=True, align='C')
                pdf.ln(10)
                
                # Add content to PDF
                pdf.multi_cell(0, 5, insights)
                
                # Save to buffer
                pdf_output = BytesIO()
                pdf.output(pdf_output)
                pdf_output.seek(0)
                
                st.download_button(
                    "📥 Download Full Report",
                    data=pdf_output,
                    file_name=f"SAMI_Report_{datetime.now().strftime('%Y%m%d_%H%M')}.pdf",
                    mime="application/pdf"
                )
                
        except Exception as e:
            st.error(f"Analysis failed: {str(e)}")
