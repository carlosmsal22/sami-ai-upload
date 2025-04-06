import streamlit as st
import pandas as pd
import sys
from pathlib import Path
from io import BytesIO
import matplotlib.pyplot as plt

# ==============================================
# Session State Initialization
# ==============================================
if 'enable_insights' not in st.session_state:
    st.session_state.update({
        'enable_insights': False,
        'enable_enhanced_stats': False,
        'df': None
    })

# Add the src directory to Python path
sys.path.append(str(Path(__file__).parent.parent))

# Import from utils
from utils.stats_helpers import run_group_comparison, run_z_chi_tests, get_descriptive_stats

st.set_page_config(page_title="🚀 Enhanced CrossTabs Analyzer", layout="wide")
st.title("🚀 Enhanced CrossTabs Analyzer")

# ==============================================
# Enhanced File Uploader (400 Error Fix)
# ==============================================
def safe_file_upload():
    """Handles file uploads with proper error handling"""
    try:
        uploaded_file = st.file_uploader(
            "Upload a cross-tabulated file (Excel format)", 
            type=["xlsx", "xls"],
            key="file_uploader_v2",  # New key to avoid conflicts
            accept_multiple_files=False
        )
        
        if uploaded_file is not None:
            if uploaded_file.size == 0:
                st.error("❌ Uploaded file is empty")
                return None
            
            # Verify file content
            try:
                file_contents = uploaded_file.getvalue()
                if len(file_contents) < 100:  # Minimum reasonable file size
                    st.error("❌ File appears to be too small or corrupted")
                    return None
                    
                return uploaded_file
            except Exception as e:
                st.error(f"❌ File verification failed: {str(e)}")
                return None
        return None
    except Exception as e:
        st.error(f"❌ Upload failed: {str(e)}")
        return None

# ==============================================
# Plugin System
# ==============================================
class AnalysisPlugins:
    @staticmethod
    def descriptive_stats(df):
        stats = {
            'basic': df.describe(include='all'),
            'missing': df.isna().sum().to_frame('Missing Values'),
            'dtypes': df.dtypes.to_frame('Data Type'),
            'unique': df.nunique().to_frame('Unique Values')
        }
        return stats
    
    @staticmethod
    def insight_generator(df):
        insights = []
        cat_cols = df.select_dtypes(include=['object', 'category']).columns
        for col in cat_cols:
            if df[col].nunique() < 20:
                top_val = df[col].mode()[0]
                freq = df[col].value_counts(normalize=True).iloc[0]
                insights.append(f"🏆 **{col}**: Most frequent value is '{top_val}' ({freq:.1%})")
        
        num_cols = df.select_dtypes(include=['number']).columns
        for col in num_cols:
            if df[col].nunique() > 5:
                insights.append(f"📊 **{col}**: Range {df[col].min():.2f}-{df[col].max():.2f} (avg={df[col].mean():.2f})")
        return insights
    
    @staticmethod
    def enhanced_export(df, format='csv'):
        if isinstance(df.columns, pd.MultiIndex):
            export_df = df.copy()
            export_df.columns = ['_'.join(filter(None, map(str, col))).strip() 
                             for col in export_df.columns.values]
        else:
            export_df = df
            
        if format == 'csv':
            return export_df.to_csv(index=False)
        elif format == 'excel':
            output = BytesIO()
            with pd.ExcelWriter(output, engine='openpyxl') as writer:
                export_df.to_excel(writer, index=False)
                if st.session_state.enable_insights:
                    insights = AnalysisPlugins.insight_generator(df)
                    pd.DataFrame(insights, columns=["Insights"]).to_excel(
                        writer, sheet_name='Insights', index=False
                    )
            return output.getvalue()

# ==============================================
# UI Components
# ==============================================
st.markdown("---")

with st.sidebar.expander("⚙️ Advanced Features"):
    st.checkbox("Enable Auto-Insights", key="enable_insights")
    st.checkbox("Enhanced Statistics", key="enable_enhanced_stats")

# Using the safe file uploader
uploaded_file = safe_file_upload()

if uploaded_file:
    try:
        df = pd.read_excel(uploaded_file, header=[0, 1, 2])
        st.session_state["df"] = df
        st.success("✅ File loaded successfully!")
        
        with st.expander("🔍 Debug: Show Column Structure"):
            st.write("Columns:", df.columns.tolist())
            st.write("Shape:", df.shape)
            st.write("Data Sample:", df.head(3))
            
    except Exception as e:
        st.error(f"""
        ❌ Error reading file: {str(e)}
        \n**Troubleshooting Tips:**
        1. Check for merged cells in headers
        2. Ensure consistent column structure
        3. Try saving as .xlsx (not .xls)
        """)

if st.button("🔄 Reset Data"):
    st.session_state["df"] = None
    st.rerun()

# ==============================================
# Main Analysis Tabs
# ==============================================
tabs = st.tabs([
    "📘 Frequency Tables", 
    "🔍 Group Comparisons", 
    "🧪 Z / Chi-Square Tests", 
    "📏 Descriptive Stats",
    "💡 Auto Insights", 
    "📤 Export Tools"
])

if st.session_state["df"] is not None:
    df = st.session_state["df"]
    
    # [Previous tab implementations remain exactly the same]
    # ... (include all your existing tab code here)

else:
    st.warning("⚠️ Please upload a file to begin analysis")

with st.expander("🐛 Debug: Session State"):
    st.write(st.session_state)
