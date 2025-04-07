# =============== IMPORTS ===============
import streamlit as st
import pandas as pd
import numpy as np
from io import BytesIO
import sys
from pathlib import Path
import os
import matplotlib.pyplot as plt
import altair as alt

# =============== PATH CONFIG ===============
def get_base_path():
    if 'RENDER' in os.environ:
        return Path('/opt/render/project/src')
    return Path(__file__).parent.parent

sys.path.append(str(get_base_path()))

# =============== DATA VALIDATION ===============
def validate_data(df):
    """Ensure data meets minimum requirements"""
    if df.empty:
        st.error("Uploaded file is empty")
        return False
    
    # Convert possible numeric columns
    for col in df.columns:
        try:
            df[col] = pd.to_numeric(df[col], errors='ignore')
        except:
            pass
    
    return True

# =============== STREAMLIT APP ===============
st.set_page_config(
    page_title="CrossTabs Analyzer",
    layout="wide",
    page_icon="📊"
)

def main():
    st.title("📊 CrossTab Analyzer")
    
    # Initialize session state
    if 'df' not in st.session_state:
        st.session_state.df = None
    
    # File upload with enhanced validation
    uploaded_file = st.file_uploader("Upload Excel/CSV", type=["xlsx", "csv"])
    if uploaded_file:
        try:
            # Read file with size validation
            if uploaded_file.size > 10 * 1024 * 1024:  # 10MB limit
                st.error("File too large (max 10MB)")
            else:
                if uploaded_file.name.endswith('.csv'):
                    df = pd.read_csv(uploaded_file)
                else:
                    df = pd.read_excel(
                        uploaded_file,
                        engine='openpyxl',
                        header=[0, 1, 2]
                    )
                    # Flatten multi-index columns
                    df.columns = ['_'.join(filter(None, map(str, col))).strip() 
                                 for col in df.columns.values]
                
                if validate_data(df):
                    st.session_state.df = df
                    st.success("✅ File loaded successfully!")
        except Exception as e:
            st.error(f"Error loading file: {str(e)}")
            st.session_state.df = None
    
    if st.session_state.df is None:
        return st.warning("Please upload a valid data file")
    
    df = st.session_state.df
    
    # Main tabs - now with proper error boundaries
    tab_names = ["🧪 Stats", "📈 Analytics", "💡 Insights", "📤 Export"]
    tabs = st.tabs(tab_names)
    
    try:
        # =============== STATS TAB ===============
        with tabs[0]:
            st.subheader("Statistical Analysis")
            stats = df.describe(include='all')
            st.dataframe(stats)
            
            num_cols = df.select_dtypes(include=np.number).columns.tolist()
            if num_cols:
                col = st.selectbox("Select column", num_cols, key='stats_col')
                fig, ax = plt.subplots()
                df[col].plot(kind='hist', ax=ax)
                st.pyplot(fig)
        
        # =============== ANALYTICS TAB ===============
        with tabs[1]:
            st.subheader("Data Analytics")
            num_cols = df.select_dtypes(include=np.number).columns.tolist()
            
            if len(num_cols) >= 2:
                col1, col2 = st.columns(2)
                with col1:
                    x_col = st.selectbox("X-axis", num_cols, key='x_axis')
                with col2:
                    y_col = st.selectbox("Y-axis", num_cols, key='y_axis')
                
                chart = alt.Chart(df).mark_circle().encode(
                    x=x_col,
                    y=y_col,
                    tooltip=list(df.columns[:3])
                )
                st.altair_chart(chart, use_container_width=True)
            else:
                st.warning("Need 2+ numeric columns for analytics")
        
        # =============== INSIGHTS TAB ===============
        with tabs[2]:
            st.subheader("Data Insights")
            
            insights = []
            for col in df.columns:
                try:
                    if pd.api.types.is_numeric_dtype(df[col]):
                        stats = df[col].describe()
                        insights.append(
                            f"📌 **{col}**: "
                            f"Avg={stats.get('mean', 0):.2f}, "
                            f"Range={stats.get('min', 0):.2f}-{stats.get('max', 0):.2f}"
                        )
                    else:
                        mode = df[col].mode()
                        top_val = mode[0] if not mode.empty else "N/A"
                        freq = df[col].value_counts(normalize=True).iloc[0] if len(df[col]) > 0 else 0
                        insights.append(f"🏷 **{col}**: Most common = '{top_val}' ({freq:.1%})")
                except:
                    pass
            
            for insight in insights[:15]:
                st.info(insight)
        
        # =============== EXPORT TAB ===============
        with tabs[3]:
            st.subheader("Export Data")
            export_format = st.radio(
                "Format",
                ["CSV", "Excel", "JSON"],
                horizontal=True
            )
            
            if export_format == "CSV":
                csv = df.to_csv(index=False)
                st.download_button(
                    "Download CSV",
                    data=csv,
                    file_name="data_export.csv",
                    mime="text/csv"
                )
            elif export_format == "Excel":
                output = BytesIO()
                with pd.ExcelWriter(output, engine='openpyxl') as writer:
                    df.to_excel(writer, index=False)
                st.download_button(
                    "Download Excel",
                    data=output.getvalue(),
                    file_name="data_export.xlsx",
                    mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
                )
            elif export_format == "JSON":
                st.download_button(
                    "Download JSON",
                    data=df.to_json(orient='records'),
                    file_name="data_export.json",
                    mime="application/json"
                )
    
    except Exception as e:
        st.error(f"An error occurred: {str(e)}")
        st.stop()

if __name__ == "__main__":
    main()
