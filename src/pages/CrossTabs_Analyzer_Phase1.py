# =============== IMPORTS ===============
import streamlit as st
import pandas as pd
import numpy as np
from io import BytesIO
import matplotlib.pyplot as plt
import altair as alt

# =============== DATA CLEANING ===============
def clean_data(df):
    """Handle all data cleaning and type conversion"""
    # Clean column names
    if isinstance(df.columns, pd.MultiIndex):
        df.columns = ['_'.join(filter(None, map(str, col))).strip() 
                     for col in df.columns.values]
    else:
        df.columns = [str(col).strip() for col in df.columns]
    
    # Replace empty strings with NaN
    df = df.replace(r'^\s*$', np.nan, regex=True)
    
    # Convert numeric columns
    for col in df.columns:
        # Skip if already numeric
        if pd.api.types.is_numeric_dtype(df[col]):
            continue
            
        # Try converting to numeric
        try:
            # Handle percentage strings
            if df[col].astype(str).str.contains('%').any():
                df[col] = pd.to_numeric(
                    df[col].astype(str).str.replace('%', ''),
                    errors='coerce'
                ) / 100
            # Handle regular numbers
            else:
                df[col] = pd.to_numeric(
                    df[col].astype(str).str.replace(',', ''),
                    errors='coerce'
                )
        except:
            pass
    
    # Drop completely empty columns
    df = df.dropna(axis=1, how='all')
    
    return df

# =============== STREAMLIT APP ===============
st.set_page_config(
    page_title="Survey Data Analyzer",
    layout="wide",
    page_icon="📊"
)

def main():
    st.title("📊 Survey Data Analyzer")
    
    # File upload with enhanced cleaning
    uploaded_file = st.file_uploader("Upload Survey Data", type=["xlsx", "csv"])
    if uploaded_file:
        with st.spinner("Processing survey data..."):
            try:
                if uploaded_file.name.endswith('.csv'):
                    df = pd.read_csv(uploaded_file)
                else:
                    df = pd.read_excel(
                        uploaded_file,
                        engine='openpyxl',
                        header=[0, 1, 2]  # Handle multi-header surveys
                    )
                
                df = clean_data(df)
                st.session_state.df = df
                st.success("✅ Survey data loaded successfully!")
                
                # Debug view
                with st.expander("View cleaned data"):
                    st.write(df.head(3))
                    st.write("Column types:", df.dtypes)
                    
            except Exception as e:
                st.error(f"🚨 Error loading survey data: {str(e)}")
                st.session_state.df = None
    
    if 'df' not in st.session_state or st.session_state.df is None:
        return st.warning("Please upload survey data file to begin")
    
    df = st.session_state.df
    
    # Main tabs
    tab1, tab2, tab3, tab4 = st.tabs([
        "📋 Overview", 
        "📈 Analytics", 
        "💡 Insights", 
        "📤 Export"
    ])
    
    # =============== OVERVIEW TAB ===============
    with tab1:
        st.subheader("Survey Data Overview")
        st.dataframe(df, height=400)
        
        # Show column summaries
        with st.expander("Column Details"):
            for col in df.columns:
                st.write(f"**{col}** ({df[col].dtype})")
                if pd.api.types.is_numeric_dtype(df[col]):
                    st.write(df[col].describe()[['mean', 'min', 'max']])
                else:
                    st.write(df[col].value_counts().head(5))
    
    # =============== ANALYTICS TAB ===============
    with tab2:
        st.subheader("Survey Analytics")
        num_cols = df.select_dtypes(include=np.number).columns.tolist()
        
        if len(num_cols) >= 2:
            col1, col2 = st.columns(2)
            with col1:
                x_col = st.selectbox("X-axis (Question)", num_cols)
            with col2:
                y_col = st.selectbox("Y-axis (Question)", num_cols)
            
            # Interactive scatter plot
            chart = alt.Chart(df).mark_circle(size=60).encode(
                x=x_col,
                y=y_col,
                tooltip=list(df.columns)
            ).interactive()
            st.altair_chart(chart, use_container_width=True)
            
            # Correlation heatmap
            st.subheader("Question Correlations")
            corr = df[num_cols].corr()
            st.dataframe(corr.style.background_gradient(cmap='coolwarm'))
        else:
            st.warning("Need at least 2 numeric questions for analytics")
            
            # Show conversion candidates
            st.info("Potential questions to convert to numeric:")
            candidates = [
                col for col in df.columns 
                if df[col].astype(str).str.replace('.','',1).str.isdigit().any()
            ]
            
            if candidates:
                for col in candidates:
                    st.write(f"- {col}")
                if st.button("Convert these questions"):
                    df[candidates] = df[candidates].apply(pd.to_numeric, errors='coerce')
                    st.session_state.df = df
                    st.rerun()
            else:
                st.write("No obvious numeric questions found in text responses")
    
    # =============== INSIGHTS TAB ===============
    with tab3:
        st.subheader("Survey Insights")
        
        insights = []
        for col in df.columns:
            try:
                if pd.api.types.is_numeric_dtype(df[col]):
                    # Skip non-informative numeric columns
                    if df[col].nunique() < 2:
                        continue
                        
                    stats = df[col].describe()
                    insights.append(
                        f"🔢 **{col.replace('_', ' ')}**: "
                        f"Average {stats['mean']:.1f} "
                        f"(Range: {stats['min']:.1f}-{stats['max']:.1f})"
                    )
                else:
                    # Skip empty columns
                    if df[col].isna().all():
                        continue
                        
                    mode = df[col].mode()
                    top_val = mode[0] if not mode.empty else "N/A"
                    freq = df[col].value_counts(normalize=True).iloc[0] if len(df[col].dropna()) > 0 else 0
                    insights.append(
                        f"🏷 **{col.replace('_', ' ')}**: "
                        f"Most common response '{top_val}' ({freq:.1%})"
                    )
            except:
                pass
        
        if insights:
            st.info("Key findings from survey responses:")
            for insight in insights[:10]:  # Show top 10 insights
                st.write(insight)
        else:
            st.warning("No meaningful insights could be generated")
    
    # =============== EXPORT TAB ===============
    with tab4:
        st.subheader("Export Survey Data")
        export_format = st.radio(
            "Select format",
            ["CSV", "Excel", "JSON"],
            horizontal=True
        )
        
        if export_format == "CSV":
            st.download_button(
                "Download CSV",
                data=df.to_csv(index=False),
                file_name="survey_results.csv",
                mime="text/csv"
            )
        elif export_format == "Excel":
            output = BytesIO()
            with pd.ExcelWriter(output, engine='openpyxl') as writer:
                df.to_excel(writer, index=False)
            st.download_button(
                "Download Excel",
                data=output.getvalue(),
                file_name="survey_results.xlsx",
                mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
            )
        elif export_format == "JSON":
            st.download_button(
                "Download JSON",
                data=df.to_json(orient='records'),
                file_name="survey_results.json",
                mime="application/json"
            )

if __name__ == "__main__":
    main()
