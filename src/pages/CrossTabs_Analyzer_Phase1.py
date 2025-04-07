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

# =============== DATA PROCESSING HELPERS ===============
def convert_to_numeric(df):
    """Automatically convert convertible columns to numeric"""
    for col in df.columns:
        try:
            df[col] = pd.to_numeric(df[col], errors='ignore')
        except:
            pass
    return df

def safe_mode(series):
    """Handle empty/missing data when calculating mode"""
    try:
        mode = series.mode()
        return mode[0] if not mode.empty else "N/A"
    except:
        return "N/A"

# =============== STREAMLIT APP ===============
st.set_page_config(
    page_title="CrossTabs Analyzer",
    layout="wide",
    page_icon="📊"
)

def main():
    st.title("📊 CrossTab Analyzer")
    
    # File upload with automatic type conversion
    uploaded_file = st.file_uploader("Upload Excel/CSV", type=["xlsx", "csv"])
    if uploaded_file:
        with st.spinner("Processing file..."):
            try:
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
                
                # Convert compatible columns to numeric
                df = convert_to_numeric(df)
                st.session_state.df = df
                st.success("✅ File loaded successfully!")
            except Exception as e:
                st.error(f"🚨 Error loading file: {str(e)}")
                st.session_state.df = None
    
    if 'df' not in st.session_state or st.session_state.df is None:
        return st.warning("Please upload a file to begin")
    
    df = st.session_state.df
    
    # Main tabs
    tab1, tab2, tab3, tab4 = st.tabs([
        "🧪 Stats", 
        "📈 Analytics", 
        "💡 Insights", 
        "📤 Export"
    ])
    
    # =============== STATS TAB ===============
    with tab1:
        st.subheader("Statistical Analysis")
        stats = df.describe(include='all')
        st.dataframe(stats)
        
        # Show distribution for numeric columns
        num_cols = df.select_dtypes(include=np.number).columns.tolist()
        if num_cols:
            col = st.selectbox("Select column for distribution", num_cols, key='dist_col')
            fig, ax = plt.subplots()
            df[col].plot(kind='hist', ax=ax)
            st.pyplot(fig)
        else:
            st.warning("No numeric columns found for visualization")
    
    # =============== ANALYTICS TAB ===============
    with tab2:
        st.subheader("Data Analytics")
        num_cols = df.select_dtypes(include=np.number).columns.tolist()
        
        if len(num_cols) >= 2:
            col1, col2 = st.columns(2)
            with col1:
                x_col = st.selectbox("X-axis column", num_cols, key='x_axis')
            with col2:
                y_col = st.selectbox("Y-axis column", num_cols, key='y_axis')
            
            try:
                chart = alt.Chart(df).mark_circle().encode(
                    x=x_col,
                    y=y_col,
                    tooltip=list(df.columns[:3])
                )
                st.altair_chart(chart, use_container_width=True)
            except Exception as e:
                st.error(f"Chart error: {str(e)}")
        else:
            st.warning("""
            Need at least 2 numeric columns for analytics. 
            Try converting text columns to numbers in your source file.
            """)
            
            # Show convertible columns
            st.info("Potential columns to convert to numeric:")
            for col in df.columns:
                if pd.api.types.is_string_dtype(df[col]):
                    sample = df[col].head(1).values[0]
                    if str(sample).replace('.','',1).isdigit():
                        st.write(f"- {col} (sample value: {sample})")
    
    # =============== INSIGHTS TAB ===============
    with tab3:
        st.subheader("Data Insights")
        
        insights = []
        for col in df.columns:
            try:
                if pd.api.types.is_numeric_dtype(df[col]):
                    stats = df[col].describe()
                    insights.append(
                        f"📌 **{col}**: "
                        f"Avg={stats.get('mean', 'N/A'):.2f}, "
                        f"Range={stats.get('min', 'N/A'):.2f}-{stats.get('max', 'N/A'):.2f}"
                    )
                else:
                    top_val = safe_mode(df[col])
                    freq = df[col].value_counts(normalize=True).iloc[0] if not df[col].empty else 0
                    insights.append(
                        f"🏷 **{col}**: "
                        f"Most common = '{top_val}' ({freq:.1%})"
                    )
            except Exception as e:
                insights.append(f"❌ Could not analyze column: {col} ({str(e)})")
        
        for insight in insights[:15]:  # Limit to 15 insights
            st.info(insight)
    
    # =============== EXPORT TAB ===============
    with tab4:
        st.subheader("Export Data")
        export_format = st.radio(
            "Select format",
            ["CSV", "Excel", "JSON"],
            horizontal=True
        )
        
        if export_format == "CSV":
            st.download_button(
                "Download CSV",
                data=df.to_csv(index=False),
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

if __name__ == "__main__":
    main()
