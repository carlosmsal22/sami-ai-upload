import streamlit as st
import pandas as pd
import sys
from pathlib import Path
from io import BytesIO
import matplotlib.pyplot as plt

# Add the src directory to Python path
sys.path.append(str(Path(__file__).parent.parent))

# Import from utils (original imports)
from utils.stats_helpers import run_group_comparison, run_z_chi_tests, get_descriptive_stats

st.set_page_config(page_title="🚀 Enhanced CrossTabs Analyzer", layout="wide")
st.title("🚀 Enhanced CrossTabs Analyzer")

# ==============================================
# NEW: Plugin System
# ==============================================
class AnalysisPlugins:
    """Container for all enhanced analysis methods"""
    
    @staticmethod
    def descriptive_stats(df):
        """Enhanced descriptive statistics"""
        stats = {
            'basic': df.describe(include='all'),
            'missing': df.isna().sum().to_frame('Missing Values'),
            'dtypes': df.dtypes.to_frame('Data Type'),
            'unique': df.nunique().to_frame('Unique Values')
        }
        return stats
    
    @staticmethod
    def insight_generator(df):
        """Automatically generate insights from data"""
        insights = []
        
        # Categorical insights
        cat_cols = df.select_dtypes(include=['object', 'category']).columns
        for col in cat_cols:
            top_val = df[col].mode()[0]
            freq = df[col].value_counts(normalize=True).iloc[0]
            insights.append(f"🏆 **{col}**: Most frequent value is '{top_val}' ({freq:.1%})")
        
        # Numerical insights
        num_cols = df.select_dtypes(include=['number']).columns
        for col in num_cols:
            if df[col].nunique() > 5:  # Only for proper numericals
                insights.append(f"📊 **{col}**: Range {df[col].min():.2f}-{df[col].max():.2f} (avg={df[col].mean():.2f})")
        
        return insights
    
    @staticmethod
    def enhanced_export(df, format='csv'):
        """Improved export functionality"""
        if format == 'csv':
            return df.to_csv(index=False)
        elif format == 'excel':
            output = BytesIO()
            with pd.ExcelWriter(output, engine='openpyxl') as writer:
                df.to_excel(writer, index=False)
                # Add summary sheet
                pd.DataFrame(AnalysisPlugins.insight_generator(df)).to_excel(
                    writer, sheet_name='Insights', index=False
                )
            return output.getvalue()

# ==============================================
# Original Core Functionality with Upgrades
# ==============================================
st.markdown("---")

# Initialize session state with new fields
if "df" not in st.session_state:
    st.session_state.update({
        "df": None,
        "enable_insights": False,
        "enable_enhanced_stats": False
    })

# NEW: Feature Toggles in Sidebar
with st.sidebar.expander("⚙️ Advanced Features"):
    st.session_state.enable_insights = st.checkbox(
        "Enable Auto-Insights", 
        st.session_state.enable_insights
    )
    st.session_state.enable_enhanced_stats = st.checkbox(
        "Enhanced Statistics", 
        st.session_state.enable_enhanced_stats
    )

# Original file uploader with error handling
uploaded_file = st.file_uploader(
    "Upload a cross-tabulated file (Excel format)", 
    type=["xlsx", "xls"],
    key="file_uploader"
)

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
        st.error(f"❌ Error reading file: {str(e)}")
        st.session_state["df"] = None

# Reset button (original)
if st.button("🔄 Reset Data"):
    st.session_state["df"] = None
    st.rerun()

# ==============================================
# Enhanced Tab System
# ==============================================
tabs = st.tabs([
    "📘 Frequency Tables", 
    "🔍 Group Comparisons", 
    "🧪 Z / Chi-Square Tests", 
    "📏 Descriptive Stats",
    "💡 Auto Insights",  # NEW TAB
    "📤 Export Tools"
])

if st.session_state["df"] is not None:
    df = st.session_state["df"]
    
    # 1. Original Frequency Tables
    with tabs[0]:
        st.subheader("📘 Frequency Table")
        st.dataframe(df, use_container_width=True)
        
        with st.expander("🔢 Value Counts"):
            for col in df.columns:
                st.write(f"**{col}**")
                st.dataframe(df[col].value_counts(dropna=False))

    # 2. Original Group Comparisons
    with tabs[1]:
        st.subheader("🔍 Compare Groups")
        columns = df.columns.tolist()
        
        col1, col2 = st.columns(2)
        with col1:
            group1 = st.selectbox("Select Group 1", columns, key="group1")
        with col2:
            group2 = st.selectbox("Select Group 2", columns, key="group2")
            
        if st.button("Run Comparison"):
            try:
                result = run_group_comparison(df, group1, group2)
                st.dataframe(result)
            except Exception as e:
                st.error(f"Comparison failed: {str(e)}")

    # 3. Original Statistical Tests
    with tabs[2]:
        st.subheader("🧪 Z-Test / Chi-Square")
        if st.button("Run Statistical Tests"):
            try:
                result = run_z_chi_tests(df)
                st.dataframe(result)
            except Exception as e:
                st.error(f"Tests failed: {str(e)}")

    # 4. Enhanced Descriptive Stats
    with tabs[3]:
        st.subheader("📏 Descriptive Stats")
        
        if st.session_state.enable_enhanced_stats:
            try:
                stats = AnalysisPlugins.descriptive_stats(df)
                st.dataframe(stats['basic'])
                
                with st.expander("🔍 Detailed Metadata"):
                    st.dataframe(stats['missing'])
                    st.dataframe(stats['dtypes'])
                    st.dataframe(stats['unique'])
                    
            except Exception as e:
                st.error(f"Enhanced stats failed: {str(e)}")
        else:
            if st.button("Generate Summary Statistics"):
                try:
                    result = get_descriptive_stats(df)
                    st.dataframe(result)
                except Exception as e:
                    st.error(f"Stats generation failed: {str(e)}")

    # 5. NEW: Auto Insights Tab
    with tabs[4]:
        st.subheader("💡 Automated Insights")
        
        if st.session_state.enable_insights:
            try:
                insights = AnalysisPlugins.insight_generator(df)
                for insight in insights:
                    st.success(insight)
                    
                with st.expander("📊 Visualization"):
                    col = st.selectbox("Select column to visualize", df.columns)
                    if pd.api.types.is_numeric_dtype(df[col]):
                        fig, ax = plt.subplots()
                        df[col].plot(kind='hist', ax=ax)
                        st.pyplot(fig)
                    else:
                        fig, ax = plt.subplots()
                        df[col].value_counts().plot(kind='bar', ax=ax)
                        st.pyplot(fig)
                        
            except Exception as e:
                st.error(f"Insight generation failed: {str(e)}")
        else:
            st.warning("Enable 'Auto-Insights' in sidebar to use this feature")

    # 6. Enhanced Export Tools
    with tabs[5]:
        st.subheader("📤 Export Tools")
        
        export_format = st.radio(
            "Select export format",
            ["CSV", "Excel"],
            horizontal=True
        )
        
        if st.session_state.enable_insights:
            include_insights = st.checkbox("Include auto-insights in export", True)
        else:
            include_insights = False
        
        try:
            if export_format == "CSV":
                data = AnalysisPlugins.enhanced_export(df, 'csv')
                st.download_button(
                    label="Download CSV",
                    data=data,
                    file_name="enhanced_export.csv",
                    mime="text/csv"
                )
            else:
                data = AnalysisPlugins.enhanced_export(df, 'excel')
                st.download_button(
                    label="Download Excel",
                    data=data,
                    file_name="enhanced_export.xlsx",
                    mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
                )
        except Exception as e:
            st.error(f"Export failed: {str(e)}")

else:
    st.warning("⚠️ Please upload a file to begin analysis")

# Debug section (original)
with st.expander("🐛 Debug: Session State"):
    st.write(st.session_state)
