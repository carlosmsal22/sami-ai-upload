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

# =============== DATA LOADER ===============
def load_data(uploaded_file):
    try:
        if uploaded_file.name.endswith('.csv'):
            df = pd.read_csv(uploaded_file)
        else:
            df = pd.read_excel(
                uploaded_file,
                engine='openpyxl',
                header=[0, 1, 2],
                dtype=str  # Prevent Arrow errors
            )
            # Clean multi-index columns
            df.columns = ['_'.join(filter(None, map(str, col))).strip() 
                         for col in df.columns.values]
        return df
    except Exception as e:
        st.error(f"🚨 Data loading error: {str(e)}")
        return None

# =============== STREAMLIT APP ===============
st.set_page_config(
    page_title="CrossTabs Analyzer",
    layout="wide",
    page_icon="📊"
)

def main():
    st.title("📊 CrossTab Analyzer")
    
    # File upload
    uploaded_file = st.file_uploader("Upload Excel/CSV", type=["xlsx", "csv"])
    if uploaded_file:
        with st.spinner("Processing file..."):
            st.session_state.df = load_data(uploaded_file)
    
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
        if st.button("Run Descriptive Stats"):
            try:
                stats = df.describe(include='all')
                st.dataframe(stats)
                
                # Add distribution plot
                num_cols = df.select_dtypes(include=np.number).columns
                if len(num_cols) > 0:
                    col = st.selectbox("Select numeric column", num_cols)
                    fig, ax = plt.subplots()
                    df[col].plot(kind='hist', ax=ax)
                    st.pyplot(fig)
            except Exception as e:
                st.error(f"Stats error: {str(e)}")
    
    # =============== ANALYTICS TAB ===============
    with tab2:
        st.subheader("Data Analytics")
        num_cols = df.select_dtypes(include=np.number).columns
        
        if len(num_cols) >= 2:
            x_col = st.selectbox("X-axis column", num_cols)
            y_col = st.selectbox("Y-axis column", num_cols)
            
            chart = alt.Chart(df).mark_circle().encode(
                x=x_col,
                y=y_col,
                tooltip=list(df.columns[:3])
            )
            st.altair_chart(chart, use_container_width=True)
        else:
            st.warning("Need at least 2 numeric columns for analytics")
    
    # =============== INSIGHTS TAB ===============
    with tab3:
        st.subheader("Data Insights")
        
        # Auto insights
        insights = []
        for col in df.columns:
            if pd.api.types.is_numeric_dtype(df[col]):
                stats = df[col].describe()
                insights.append(f"📌 **{col}**: Avg={stats['mean']:.2f}, Range={stats['min']:.2f}-{stats['max']:.2f}")
            else:
                top_val = df[col].mode()[0]
                freq = df[col].value_counts(normalize=True).iloc[0]
                insights.append(f"🏷 **{col}**: Most common = '{top_val}' ({freq:.1%})")
        
        for insight in insights[:10]:  # Limit to 10 insights
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
