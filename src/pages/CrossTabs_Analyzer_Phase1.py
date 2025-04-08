# =============== IMPORTS ===============
import streamlit as st
import pandas as pd
import numpy as np
from io import BytesIO
import matplotlib.pyplot as plt
import altair as alt

# =============== DATA PROCESSING ===============
def convert_to_numeric(df):
    """Automatically detect and convert numeric columns"""
    for col in df.columns:
        # Skip if already numeric
        if pd.api.types.is_numeric_dtype(df[col]):
            continue
            
        # Try converting to numeric
        try:
            df[col] = pd.to_numeric(df[col], errors='raise')
            st.sidebar.success(f"Converted {col} to numeric")
        except:
            # If conversion fails, keep as-is
            pass
    return df

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
                
                # Auto-convert compatible columns
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
            
            chart = alt.Chart(df).mark_circle().encode(
                x=x_col,
                y=y_col,
                tooltip=list(df.columns[:3])
            )
            st.altair_chart(chart, use_container_width=True)
        else:
            st.warning("Need at least 2 numeric columns for analytics")
            
            # Show conversion suggestions
            st.info("Potential columns to convert to numeric:")
            convert_candidates = []
            for col in df.columns:
                if pd.api.types.is_string_dtype(df[col]):
                    sample = df[col].head(1).values[0]
                    if str(sample).replace('.','',1).isdigit():
                        convert_candidates.append(col)
            
            if convert_candidates:
                for col in convert_candidates:
                    st.write(f"- {col}")
                if st.button("Auto-convert suggested columns"):
                    df[convert_candidates] = df[convert_candidates].apply(pd.to_numeric, errors='coerce')
                    st.session_state.df = df
                    st.rerun()
            else:
                st.write("No obvious numeric columns found in text data")
    
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
                        f"Avg={stats.get('mean', 0):.2f}, "
                        f"Range={stats.get('min', 0):.2f}-{stats.get('max', 0):.2f}"
                    )
                else:
                    mode = df[col].mode()
                    top_val = mode[0] if not mode.empty else "N/A"
                    freq = df[col].value_counts(normalize=True).iloc[0] if len(df[col]) > 0 else 0
                    insights.append(f"🏷 **{col}**: Most common = '{top_val}' ({freq:.1%})")
            except:
                insights.append(f"❌ Could not analyze column: {col}")
        
        for insight in insights[:15]:
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
