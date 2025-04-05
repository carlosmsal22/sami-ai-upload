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
# INITIAL SETUP
# =============================================
st.set_page_config(
    page_title="SAMI Analyzer Pro",
    page_icon="🔍",
    layout="wide"
)

# Custom CSS for enhanced UI
st.markdown("""
<style>
    [data-testid="stFileUploader"] {
        border: 2px dashed #4e8cff;
        border-radius: 8px;
        padding: 20px;
    }
    .st-b7 {
        background-color: #f0f2f6 !important;
    }
    [data-testid="stExpander"] details summary p {
        font-weight: 600 !important;
        font-size: 1.1rem !important;
    }
    .st-cb { background-color: #4e8cff; }
</style>
""", unsafe_allow_html=True)

# Initialize OpenAI client
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# =============================================
# SIDEBAR CONTROLS
# =============================================
with st.sidebar:
    st.title("⚙️ Analysis Settings")
    
    # Analysis Mode Selection
    analysis_mode = st.radio(
        "**Analysis Mode**",
        ["Basic EDA", "Advanced Insights", "Predictive Modeling"],
        help="""Basic: Descriptive statistics and visualizations
        Advanced: Statistical tests and correlations
        Predictive: Machine learning models"""
    )
    
    # File Upload (optional - can move to main area)
    uploaded_file = st.file_uploader(
        "Upload Dataset",
        type=["csv", "xlsx"],
        help="Supports CSV and Excel files"
    )
    
    # Advanced Options
    with st.expander("Advanced Options"):
        confidence_level = st.slider(
            "Confidence Level",
            0.80, 0.99, 0.95
        )
        max_categories = st.number_input(
            "Max Categories",
            5, 50, 15
        )

# =============================================
# MAIN INTERFACE
# =============================================
st.title("🔍 SAMI AI - Advanced Analytics Suite")
st.caption("Upload your dataset and discover actionable insights")

# Help Section
with st.expander("ℹ️ How to use this tool", expanded=False):
    st.markdown("""
    **5-Step Workflow:**
    1. **Upload** your dataset (Excel/CSV)
    2. **Ask a question** about your data
    3. **Select analyses** using checkboxes
    4. **Explore** interactive visualizations
    5. **Download** full PDF report
    
    💡 **Try these prompts:**
    - "What are the key trends by region?"
    - "Show me unexpected relationships"
    - "Which factors impact [metric] most?"
    - "Identify potential data quality issues"
    """)

# File Uploader
uploaded_file = st.file_uploader(
    "**Upload your dataset**",
    type=["xlsx", "csv"],
    help="Supports Excel and CSV files up to 200MB"
)

# Analysis Selection
st.markdown("**🔍 Select Analyses:**")
col1, col2, col3 = st.columns(3)
with col1:
    show_corr = st.checkbox("🔗 Correlation Matrix", True)
    show_dist = st.checkbox("📊 Distributions", True)
with col2:
    show_pca = st.checkbox("🔮 PCA Projection")
    show_cluster = st.checkbox("🧭 Clustering")
with col3:
    show_tfidf = st.checkbox("📝 Text Analysis")
    show_anomaly = st.checkbox("⚠️ Anomaly Detection", True)

# User Question
user_prompt = st.text_area(
    "**Ask a question about your data:**",
    placeholder="E.g.: What are the key drivers of customer satisfaction?",
    height=100
)

# =============================================
# ANALYSIS FUNCTIONS
# =============================================
@st.cache_data
def load_data(uploaded_file):
    """Load data with caching"""
    if uploaded_file.name.endswith('.csv'):
        return pd.read_csv(uploaded_file)
    return pd.read_excel(uploaded_file)

def detect_anomalies(df):
    """Enhanced outlier detection"""
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
        
        # Combine results
        col_anomalies = pd.concat([iqr_outliers, z_outliers]).drop_duplicates()
        col_anomalies['Anomaly_Type'] = f"{col} Outlier"
        anomalies = pd.concat([anomalies, col_anomalies])
    
    return anomalies.drop_duplicates()

def generate_visuals(df):
    """Enhanced visualization suite"""
    # Interactive Distribution Plots
    if show_dist:
        st.subheader("📊 Feature Distributions")
        num_cols = df.select_dtypes(include=np.number).columns
        for col in num_cols[:5]:  # Limit to first 5 for performance
            fig = px.histogram(
                df, x=col, marginal="box",
                title=f"Distribution of {col}",
                hover_data=df.columns
            )
            st.plotly_chart(fig, use_container_width=True)
    
    # Correlation Analysis
    if show_corr and len(df.select_dtypes(include=np.number).columns) >= 2:
        st.subheader("🔗 Correlation Matrix")
        corr = df.select_dtypes(include=np.number).corr()
        fig = px.imshow(
            corr,
            text_auto=".2f",
            color_continuous_scale='RdBu',
            range_color=[-1, 1],
            aspect="auto"
        )
        st.plotly_chart(fig, use_container_width=True)
    
    # PCA Visualization
    if show_pca and len(df.select_dtypes(include=np.number).columns) >= 3:
        st.subheader("🔮 PCA Projection")
        pca = PCA(n_components=2)
        reduced = pca.fit_transform(df.select_dtypes(include=np.number).dropna())
        fig = px.scatter(
            x=reduced[:, 0], y=reduced[:, 1],
            labels={'x': 'PC1', 'y': 'PC2'},
            title="2D PCA Projection"
        )
        st.plotly_chart(fig, use_container_width=True)

# =============================================
# MAIN EXECUTION
# =============================================
if st.button("🚀 Run Analysis", type="primary") and uploaded_file:
    with st.spinner("Analyzing your data..."):
        try:
            # Load Data
            df = load_data(uploaded_file)
            st.session_state.df = df
            
            # Data Quality Report
            with st.expander("🔍 Data Quality Report", expanded=True):
                cols = st.columns(3)
                with cols[0]:
                    st.metric("Total Rows", df.shape[0])
                with cols[1]:
                    st.metric("Total Columns", df.shape[1])
                with cols[2]:
                    st.metric("Missing Values", df.isnull().sum().sum())
                
                # Column Summary
                st.dataframe(
                    pd.DataFrame({
                        'Data Type': df.dtypes,
                        'Missing %': (df.isnull().mean()*100).round(1),
                        'Unique Values': df.nunique()
                    }),
                    use_container_width=True
                )
            
            # Generate Visualizations
            generate_visuals(df)
            
            # Anomaly Detection
            if show_anomaly:
                anomalies = detect_anomalies(df)
                if not anomalies.empty:
                    st.warning(f"⚠️ Detected {len(anomalies)} potential anomalies")
                    with st.expander("View Anomalies"):
                        st.dataframe(anomalies)
            
            # GPT Insights (corrected version)
            with st.spinner("Generating AI insights..."):
                try:
                    # Try using to_markdown() if tabulate is available
                    try:
                        stats_summary = df.describe().to_markdown()
                    except ImportError:
                        # Fallback to to_string() if tabulate not available
                        stats_summary = df.describe().to_string()
                    
                    data_summary = f"""
                    Dataset Shape: {df.shape}
                    Numeric Columns: {df.select_dtypes(include=np.number).columns.tolist()}
                    Sample Statistics:
                    {stats_summary}
                    """
                    
                    response = client.chat.completions.create(
                        model="gpt-4-turbo",
                        messages=[
                            {
                                "role": "system",
                                "content": "You're a senior data analyst. Provide: 1) Key patterns 2) Business implications 3) Recommended actions"
                            },
                            {
                                "role": "user",
                                "content": f"Analyze this data:\n{data_summary}\n\nUser Question: {user_prompt or 'Provide comprehensive analysis'}"
                            }
                        ],
                        temperature=0.7
                    )
                    
                    insights = response.choices[0].message.content
                    st.subheader("💡 AI-Generated Insights")
                    st.markdown(insights)
                    
                except Exception as e:
                    st.error(f"AI analysis failed: {str(e)}")
            
            # PDF Report Generation
            pdf = FPDF()
            pdf.add_page()
            pdf.set_font("Arial", size=12)
            
            # Add report content
            pdf.cell(200, 10, txt="SAMI AI Analysis Report", ln=True, align='C')
            pdf.multi_cell(0, 5, insights)
            
            # Save to buffer
            pdf_output = BytesIO()
            pdf.output(pdf_output)
            pdf_output.seek(0)
            
            # Download Button
            st.download_button(
                "📥 Download Full Report (PDF)",
                data=pdf_output,
                file_name=f"SAMI_Report_{datetime.now().strftime('%Y%m%d')}.pdf",
                mime="application/pdf"
            )
            
        except Exception as e:
            st.error(f"Analysis failed: {str(e)}")
