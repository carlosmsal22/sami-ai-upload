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
if 'openai_error' not in st.session_state:
    st.session_state.openai_error = None

# Initialize OpenAI client with error handling
try:
    client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
except Exception as e:
    st.session_state.openai_error = f"OpenAI initialization failed: {str(e)}"
    client = None

# =============================================
# ENHANCED FILE UPLOADER (FIXED FOR EXCEL)
# =============================================
def safe_file_upload():
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
            
            with st.spinner("Processing file..."):
                try:
                    if uploaded_file.name.endswith('.csv'):
                        df = pd.read_csv(uploaded_file)
                    else:
                        # Handle Excel with explicit engine
                        df = pd.read_excel(uploaded_file, engine='openpyxl')
                    
                    if df.empty:
                        st.session_state.upload_error = "Empty file detected"
                        return None
                        
                    st.session_state.df = df
                    st.session_state.upload_error = None
                    return df
                
                except Exception as e:
                    st.session_state.upload_error = f"Error reading file: {str(e)}"
                    return None
            
        return None
        
    except Exception as e:
        st.session_state.upload_error = f"Upload failed: {str(e)}"
        return None

# =============================================
# ANALYSIS FUNCTIONS (WITH ERROR HANDLING)
# =============================================
def run_correlation_analysis(df):
    try:
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
            return corr
        else:
            st.warning("Need at least 2 numeric columns for correlation")
            return None
    except Exception as e:
        st.error(f"Correlation analysis failed: {str(e)}")
        return None

def generate_ai_insights(df, prompt=""):
    if client is None:
        st.error("OpenAI client not initialized")
        return None
    
    try:
        # Create data summary for AI
        data_summary = f"""
        Dataset Shape: {df.shape}
        Columns: {df.columns.tolist()}
        Numeric Columns: {df.select_dtypes(include=np.number).columns.tolist()}
        Sample Statistics:
        {df.describe().to_markdown()}
        """
        
        with st.spinner("Generating AI insights..."):
            response = client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[
                    {
                        "role": "system",
                        "content": "You are a data analyst. Provide clear insights about this data:"
                    },
                    {
                        "role": "user",
                        "content": f"{data_summary}\n\nUser question: {prompt or 'Identify key patterns'}"
                    }
                ],
                temperature=0.7,
                max_tokens=1000
            )
            return response.choices[0].message.content
    except Exception as e:
        st.session_state.openai_error = f"OpenAI API error: {str(e)}"
        return None

# =============================================
# MAIN INTERFACE
# =============================================
st.title("🔍 SAMI AI - Advanced Analytics Suite")

# File Upload
df = safe_file_upload()

# Display errors if any
if st.session_state.upload_error:
    st.error(st.session_state.upload_error)
if st.session_state.openai_error:
    st.error(st.session_state.openai_error)

if st.session_state.df is not None:
    df = st.session_state.df
    st.success(f"✅ Successfully loaded {len(df)} rows")
    
    with st.expander("🔍 Data Preview", expanded=True):
        st.dataframe(df.head(3))
        
        # Basic stats
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
            "AI Insights"
        ],
        default=["Correlation Analysis"]
    )
    
    user_prompt = st.text_area("Ask a question about your data:")
    
    if st.button("🚀 Run Selected Analyses", type="primary"):
        with st.spinner("Running analyses..."):
            # Correlation Analysis
            if "Correlation Analysis" in analysis_options:
                run_correlation_analysis(df)
            
            # Distribution Analysis
            if "Distribution Analysis" in analysis_options:
                st.subheader("📊 Distributions")
                numeric_cols = df.select_dtypes(include=np.number).columns
                for col in numeric_cols[:3]:  # Show first 3 for demo
                    fig, ax = plt.subplots()
                    df[col].hist(ax=ax, bins=20)
                    ax.set_title(f"Distribution of {col}")
                    st.pyplot(fig)
            
            # AI Insights
            if "AI Insights" in analysis_options:
                st.subheader("💡 AI Insights")
                insights = generate_ai_insights(df, user_prompt)
                if insights:
                    st.markdown(insights)
                elif st.session_state.openai_error:
                    st.error(st.session_state.openai_error)
