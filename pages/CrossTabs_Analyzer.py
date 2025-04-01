import streamlit as st  
import pandas as pd  
from utils.parsers import parse_crosstab_file  
from utils.gpt_helpers import summarize_gpt_slide_text  

st.set_page_config(page_title="📊 Cross-Tabs Analyzer", layout="wide")  
st.title("📊 Cross-Tabs Reader + GPT Insight Summarizer")  

uploaded_file = st.file_uploader("Upload a cross-tabulated Excel file", type=["xlsx", "xls"])  

if uploaded_file:  
    try:  
        st.info("Parsing file and detecting headers...")  
        df = parse_crosstab_file(uploaded_file)  
        st.subheader("🔍 Preview")  
        st.dataframe(df.head(20))  

        if st.button("🧠 Generate GPT Summary"):  
            st.subheader("🧠 GPT Insights Summary")  
            try:  
                gpt_summary = summarize_gpt_slide_text(df.head(30).to_string(index=False))  
                st.success("Summary complete!")  
                st.markdown(gpt_summary)  
            except Exception as e:  
                st.error(f"❌ Error with GPT: {e}")  

    except Exception as e:  
        st.error(f"❌ Error parsing file: {e}")
