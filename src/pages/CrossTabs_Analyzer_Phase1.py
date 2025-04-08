# =============== IMPORTS ===============
import streamlit as st
import pandas as pd
import numpy as np
from io import BytesIO
import matplotlib.pyplot as plt
import altair as alt
import re
from pandas.api.types import is_numeric_dtype

# =============== DATA VALIDATION ===============
def validate_upload(file):
    """Validate file before processing"""
    if file.size > 10 * 1024 * 1024:  # 10MB limit
        raise ValueError("File size exceeds 10MB limit")
    if file.type not in ["application/vnd.ms-excel", 
                        "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet", 
                        "text/csv"]:
        raise ValueError("Invalid file type")
    return True

def clean_column_name(name):
    """Ensure column names are URL and Arrow safe"""
    name = str(name)
    # Replace special chars (keeping underscores)
    name = re.sub(r'[^a-zA-Z0-9_]', '_', name)
    # Remove leading/trailing underscores/numbers
    name = name.strip('_').strip('0123456789')
    # Ensure it starts with letter
    if not name or not name[0].isalpha():
        name = f"col_{name}" if name else "column"
    return name[:64]  # Limit length

# =============== STREAMLIT APP ===============
st.set_page_config(
    page_title="Survey Analyzer",
    layout="wide",
    page_icon="📊"
)

def main():
    st.title("📊 Survey Data Analyzer")
    
    # Initialize session state
    if 'df' not in st.session_state:
        st.session_state.df = None
        st.session_state.clean_cols = None
    
    # File upload with enhanced validation
    uploaded_file = st.file_uploader(
        "Upload Survey Data (Excel/CSV)", 
        type=["xlsx", "csv"],
        accept_multiple_files=False
    )
    
    if uploaded_file:
        try:
            validate_upload(uploaded_file)
            
            with st.spinner("Processing survey data..."):
                if uploaded_file.name.endswith('.csv'):
                    df = pd.read_csv(uploaded_file)
                else:
                    df = pd.read_excel(
                        uploaded_file,
                        engine='openpyxl',
                        header=[0, 1, 2]  # Handle multi-header
                    )
                    # Flatten multi-index columns
                    df.columns = [
                        clean_column_name('_'.join(
                            filter(None, 
                                map(str, col))
                        )) 
                        for col in df.columns.values
                    ]
                
                # Clean data
                df = df.replace(r'^\s*$', np.nan, regex=True)
                df = df.dropna(axis=1, how='all')
                
                # Convert numeric columns
                for col in df.columns:
                    if not is_numeric_dtype(df[col]):
                        try:
                            df[col] = pd.to_numeric(
                                df[col].astype(str).str.replace('[^0-9.-]', ''),
                                errors='coerce'
                            )
                        except:
                            pass
                
                st.session_state.df = df
                st.session_state.clean_cols = df.columns.tolist()
                st.success("✅ Data loaded successfully!")
                
        except Exception as e:
            st.error(f"❌ Upload failed: {str(e)}")
            st.session_state.df = None
    
    if st.session_state.df is None:
        return st.warning("Please upload valid survey data")
    
    df = st.session_state.df
    clean_cols = st.session_state.clean_cols
    
    # Main tabs
    tab1, tab2, tab3, tab4 = st.tabs([
        "📋 Overview", 
        "📈 Analytics", 
        "💡 Insights", 
        "📤 Export"
    ])
    
    # =============== OVERVIEW TAB ===============
    with tab1:
        st.subheader("Data Overview")
        st.dataframe(df.head(10))
        
        with st.expander("Column Summary"):
            for col in clean_cols:
                st.write(f"**{col}** ({df[col].dtype})")
                if is_numeric_dtype(df[col]):
                    st.write(df[col].describe()[['mean', 'min', 'max']])
                else:
                    st.write(df[col].value_counts().head(5))
    
    # =============== ANALYTICS TAB ===============
    with tab2:
        st.subheader("Data Analytics")
        num_cols = [col for col in clean_cols if is_numeric_dtype(df[col])]
        
        if len(num_cols) >= 2:
            col1, col2 = st.columns(2)
            with col1:
                x_col = st.selectbox("X-axis", num_cols, key='x_axis')
            with col2:
                y_col = st.selectbox("Y-axis", num_cols, key='y_axis')
            
            try:
                chart = alt.Chart(df).mark_circle().encode(
                    x=alt.X(x_col, type='quantitative'),
                    y=alt.Y(y_col, type='quantitative'),
                    tooltip=clean_cols[:5]  # Show first 5 cols
                ).interactive()
                st.altair_chart(chart, use_container_width=True)
            except Exception as e:
                st.error(f"Visualization error: {str(e)}")
        else:
            st.warning("Need 2+ numeric columns for analytics")
    
    # =============== INSIGHTS TAB ===============
    with tab3:
        st.subheader("Data Insights")
        
        insights = []
        for col in clean_cols:
            try:
                if is_numeric_dtype(df[col]) and df[col].notna().any():
                    stats = df[col].describe()
                    insights.append(
                        f"🔢 **{col}**: "
                        f"Avg={stats.get('mean', 0):.2f} "
                        f"(Range: {stats.get('min', 0):.2f}-{stats.get('max', 0):.2f})"
                    )
                elif df[col].notna().any():
                    top_val = df[col].mode()[0] if not df[col].mode().empty else "N/A"
                    freq = df[col].value_counts(normalize=True).iloc[0]
                    insights.append(
                        f"🏷 **{col}**: "
                        f"Most common: '{top_val}' ({freq:.1%})"
                    )
            except:
                pass
        
        for insight in insights[:15]:  # Limit to 15 insights
            st.info(insight)
    
    # =============== EXPORT TAB ===============
    with tab4:
        st.subheader("Export Data")
        
        export_format = st.radio(
            "Format",
            ["CSV", "Excel", "JSON"],
            horizontal=True
        )
        
        try:
            if export_format == "CSV":
                csv = df.to_csv(index=False)
                st.download_button(
                    "Download CSV",
                    data=csv,
                    file_name="survey_data.csv",
                    mime="text/csv"
                )
            elif export_format == "Excel":
                output = BytesIO()
                with pd.ExcelWriter(output, engine='openpyxl') as writer:
                    df.to_excel(writer, index=False)
                st.download_button(
                    "Download Excel",
                    data=output.getvalue(),
                    file_name="survey_data.xlsx",
                    mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
                )
            elif export_format == "JSON":
                st.download_button(
                    "Download JSON",
                    data=df.to_json(orient='records'),
                    file_name="survey_data.json",
                    mime="application/json"
                )
        except Exception as e:
            st.error(f"Export failed: {str(e)}")

if __name__ == "__main__":
    main()
