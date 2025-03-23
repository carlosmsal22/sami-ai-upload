import streamlit as st
import openai
import pandas as pd
import io

st.set_page_config(page_title="SAMI AI – Excel Analyzer", layout="wide")
st.title("SAMI AI – Advanced Analytical Tool")

openai.api_key = st.secrets["OPENAI_API_KEY"]

uploaded_file = st.file_uploader("Upload an Excel or CSV file", type=["xlsx", "csv"])
user_prompt = st.text_area("Ask a question about your uploaded file or type any data-related query:")

def parse_file(file):
    if file.name.endswith(".csv"):
        return pd.read_csv(file)
    elif file.name.endswith(".xlsx"):
        return pd.read_excel(file)
    else:
        return None

if st.button("Analyze"):
    if uploaded_file:
        try:
            df = parse_file(uploaded_file)
            data_sample = df.head(3).to_csv(index=False)
            file_info = f"The uploaded file contains {df.shape[0]} rows and {df.shape[1]} columns."
        except Exception as e:
            st.error(f"Error reading file: {e}")
            st.stop()
    else:
        data_sample = ""
        file_info = "No file uploaded."

    system_prompt = f"You are SAMI AI, an advanced analytics assistant. {file_info} The first few rows of the file look like this:
{data_sample}"

    try:
        with st.spinner("Generating insights..."):
            response = openai.ChatCompletion.create(
                model="gpt-4",
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_prompt}
                ]
            )
            st.markdown(response['choices'][0]['message']['content'])
    except Exception as e:
        st.error(f"API error: {e}")
