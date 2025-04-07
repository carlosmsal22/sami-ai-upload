# =============== IMPORTS ===============
import streamlit as st
import pandas as pd
import sys
from pathlib import Path
from io import BytesIO
import matplotlib.pyplot as plt

# =============== PATH FIX ===============
# Add src directory to Python path (critical for Render deployment)
sys.path.append(str(Path(__file__).parent.parent))

# =============== UTILS IMPORT ===============
try:
    from utils.stats_helpers import run_group_comparison, run_z_chi_tests, get_descriptive_stats
except ImportError as e:
    st.error(f"""
    ❌ Failed to import utils module: {str(e)}
    Please verify:
    1. The file exists at: src/utils/stats_helpers.py
    2. The file contains all required functions
    3. The project structure is correct
    """)
    st.stop()  # Halt execution if imports fail

# =============== STREAMLIT CONFIG ===============
st.set_page_config(
    page_title="🚀 Enhanced CrossTabs Analyzer", 
    layout="wide",
    page_icon="📊"
)
st.title("🚀 Enhanced CrossTabs Analyzer")

# =============== ANALYSIS PLUGINS ===============
class AnalysisPlugins:
    """Enhanced analysis methods container"""
    
    @staticmethod
    def descriptive_stats(df):
        """Enhanced descriptive statistics with metadata"""
        stats = {
            'basic': get_descriptive_stats(df),  # Using your imported function
            'missing': df.isna().sum().to_frame('Missing Values'),
            'dtypes': df.dtypes.to_frame('Data Type'),
            'unique': df.nunique().to_frame('Unique Values')
        }
        return stats
    
    @staticmethod
    def insight_generator(df):
        """Auto-generated insights from data patterns"""
        insights = []
        
        # Categorical insights
        cat_cols = df.select_dtypes(include=['object', 'category']).columns
        for col in cat_cols:
            if df[col].nunique() < 20:
                top_val = df[col].mode()[0]
                freq = df[col].value_counts(normalize=True).iloc[0]
                insights.append(f"🏆 **{col}**: Most frequent value is '{top_val}' ({freq:.1%})")
        
        # Numerical insights
        num_cols = df.select_dtypes(include=['number']).columns
        for col in num_cols:
            if df[col].nunique() > 5:
                insights.append(f"📊 **{col}**: Range {df[col].min():.2f}-{df[col].max():.2f} (avg={df[col].mean():.2f})")
        
        return insights
    
    @staticmethod
    def enhanced_export(df, format='csv'):
        """Smart export with MultiIndex support"""
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
                if st.session_state.get("enable_insights", False):
                    insights = AnalysisPlugins.insight_generator(df)
                    pd.DataFrame(insights, columns=["Insights"]).to_excel(
                        writer, sheet_name='Insights', index=False
                    )
            return output.getvalue()

# =============== CORE APPLICATION ===============
def main():
    # Session state initialization
    if "df" not in st.session_state:
        st.session_state.update({
            "df": None,
            "enable_insights": False,
            "enable_enhanced_stats": False
        })

    # Sidebar controls
    with st.sidebar:
        st.header("Settings")
        with st.expander("⚙️ Advanced Features"):
            st.session_state.enable_insights = st.checkbox(
                "Enable Auto-Insights", 
                value=st.session_state.enable_insights
            )
            st.session_state.enable_enhanced_stats = st.checkbox(
                "Enhanced Statistics", 
                value=st.session_state.enable_enhanced_stats
            )

        # Debug info
        with st.expander("🐛 Debug Info"):
            st.write("Python path:", sys.path)
            st.write("Current directory:", Path(__file__).parent)
            st.write("Utils path:", str(Path(__file__).parent.parent / "utils" / "stats_helpers.py"))

    # File uploader
    uploaded_file = st.file_uploader(
        "Upload cross-tabulated data (Excel)", 
        type=["xlsx", "xls"]
    )

    if uploaded_file:
        try:
            df = pd.read_excel(uploaded_file, header=[0, 1, 2])
            st.session_state["df"] = df
            st.success("✅ File loaded successfully!")
            
            with st.expander("🔍 Data Preview"):
                st.write("Columns:", df.columns.tolist())
                st.write("Shape:", df.shape)
                st.dataframe(df.head(3))
                
        except Exception as e:
            st.error(f"❌ Error reading file: {str(e)}")
            st.session_state["df"] = None

    if st.button("🔄 Reset Data"):
        st.session_state["df"] = None
        st.rerun()

    # Main tabs
    tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs([
        "📊 Frequency Tables", 
        "🔍 Group Comparisons", 
        "🧪 Statistical Tests", 
        "📈 Descriptive Stats",
        "💡 Auto Insights",
        "📤 Export Data"
    ])

    if st.session_state["df"] is not None:
        df = st.session_state["df"]
        
        # [Rest of your tab implementations...]
        # [Include all your existing tab code here]
        # [Make sure to use the imported functions]
        
if __name__ == "__main__":
    main()
