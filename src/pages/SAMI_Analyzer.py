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
if 'analysis_done' not in st.session_state:
    st.session_state.analysis_done = False

# Initialize OpenAI client
try:
    client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
except Exception as e:
    st.session_state.openai_error = f"OpenAI initialization failed: {str(e)}"
    client = None

# =============================================
# ENHANCED FILE UPLOADER
# =============================================
def safe_file_upload():
    try:
        uploaded_file = st.file_uploader(
            "**Upload Dataset (CSV/Excel)**",
            type=["csv", "xlsx"],
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
def run_advanced_analysis(df, analysis_types, user_prompt=""):
    results = {}
    
    # 1. Correlation Analysis
    if "Correlation Matrix" in analysis_types:
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
            results['correlation'] = corr
    
    # 2. Distribution Analysis
    if "Distributions" in analysis_types:
        st.subheader("📊 Feature Distributions")
        numeric_cols = df.select_dtypes(include=np.number).columns
        for col in numeric_cols[:5]:  # Show first 5 for demo
            fig = px.histogram(
                df, x=col, marginal="box",
                title=f"Distribution of {col}",
                hover_data=df.columns
            )
            st.plotly_chart(fig, use_container_width=True)
    
    # 3. Anomaly Detection
    if "Anomaly Detection" in analysis_types:
        st.subheader("⚠️ Anomaly Report")
        numeric_cols = df.select_dtypes(include=np.number).columns
        anomalies = pd.DataFrame()
        
        for col in numeric_cols:
            z_scores = np.abs(stats.zscore(df[col].dropna()))
            outliers = df[z_scores > 3]
            if not outliers.empty:
                outliers['Anomaly_Type'] = f"{col} (Z > 3)"
                anomalies = pd.concat([anomalies, outliers])
        
        if not anomalies.empty:
            st.dataframe(anomalies)
        else:
            st.success("No anomalies detected (Z > 3)")
        results['anomalies'] = anomalies
    
    # 4. AI Insights (with tabulate workaround)
    if "AI Insights" in analysis_types and client:
        st.subheader("💡 AI Insights")
        try:
            # Create data summary without .to_markdown()
            data_summary = f"""
            Dataset Shape: {df.shape}
            Columns: {', '.join(df.columns)}
            Numeric Columns: {', '.join(df.select_dtypes(include=np.number).columns)}
            
            Sample Statistics:
            Mean Values:
            {df.select_dtypes(include=np.number).mean().to_string()}
            
            Value Counts:
            {df.select_dtypes(include='object').nunique().to_string()}
            """
            
            with st.spinner("Generating insights..."):
                response = client.chat.completions.create(
                    model="gpt-3.5-turbo",
                    messages=[
                        {
                            "role": "system",
                            "content": "You're a data analyst. Provide: 1) Key patterns 2) Business insights 3) Recommendations"
                        },
                        {
                            "role": "user",
                            "content": f"{data_summary}\n\nUser question: {user_prompt or 'Analyze this data'}"
                        }
                    ],
                    temperature=0.7
                )
                insights = response.choices[0].message.content
                st.markdown(insights)
                results['insights'] = insights
        except Exception as e:
            st.error(f"AI analysis failed: {str(e)}")
    
    return results

# =============================================
# MAIN INTERFACE (WITH SIDEBAR)
# =============================================
st.title("🔍 SAMI AI - Advanced Analytics Suite")

# Sidebar with options
with st.sidebar:
    st.header("Analysis Settings")
    analysis_options = st.multiselect(
        "Select analyses:",
        options=[
            "Correlation Matrix",
            "Distributions",
            "Anomaly Detection",
            "AI Insights"
        ],
        default=["Correlation Matrix", "Distributions"]
    )
    
    if client:
        user_prompt = st.text_area("Ask about your data:")
    else:
        st.warning("OpenAI unavailable - AI Insights disabled")

# File Upload
df = safe_file_upload()

# Display errors
if st.session_state.upload_error:
    st.error(st.session_state.upload_error)
if st.session_state.openai_error:
    st.error(st.session_state.openai_error)

# Run analysis
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

    if st.button("🚀 Run Analysis", type="primary"):
        with st.spinner("Analyzing..."):
            results = run_advanced_analysis(df, analysis_options, user_prompt)
            st.session_state.analysis_done = True
            st.session_state.results = results

    # Report Generation
    if st.session_state.analysis_done and 'results' in st.session_state:
        st.subheader("📄 Report Generation")
        if st.button("📥 Download Summary"):
            pdf = FPDF()
            pdf.add_page()
            pdf.set_font("Arial", size=12)
            pdf.cell(200, 10, txt="SAMI Analysis Report", ln=1, align='C')
            
            # Add analysis results to PDF
            if 'insights' in st.session_state.results:
                pdf.multi_cell(0, 5, st.session_state.results['insights'])
            
            # Save and offer download
            pdf_output = BytesIO()
            pdf.output(pdf_output)
            pdf_output.seek(0)
            
            st.download_button(
                label="Download PDF",
                data=pdf_output,
                file_name="sami_report.pdf",
                mime="application/pdf"
            )
