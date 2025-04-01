import streamlit as st  
import pandas as pd  
import plotly.express as px  
from utils.parsers import parse_crosstab_file  
from utils.gpt_helpers import summarize_comparisons  

st.set_page_config(page_title="📊 Cross-Tabs Analyzer – Step 2", layout="wide")  
st.title("📊 Cross-Tabs Group Comparison Visualizer")  

uploaded_file = st.file_uploader("Upload a cross-tab Excel file with grouped segments", type=["xlsx", "xls"])  

if uploaded_file:  
    try:  
        df = parse_crosstab_file(uploaded_file)  
        st.subheader("📋 Data Preview")  
        st.dataframe(df.head(20))  

        question_col = st.selectbox("Select Question Column", df.columns)  
        group_col = st.selectbox("Select Grouping Column", df.columns[::-1])  

        st.subheader("📊 Group Comparison Chart")  
        try:  
            fig = px.bar(df, x=group_col, y=question_col, color=group_col, barmode="group")  
            st.plotly_chart(fig, use_container_width=True)  
        except Exception as e:  
            st.error(f"Error generating chart: {e}")  

        if st.button("🧠 GPT Insight Summary"):  
            st.subheader("🧠 GPT Summary")  
            try:  
                gpt_summary = summarize_comparisons(df, group_col, question_col)  
                st.markdown(gpt_summary)  
            except Exception as e:  
                st.error(f"Error during GPT summary: {e}")  

    except Exception as e:  
        st.error(f"❌ File parsing failed: {e}")
