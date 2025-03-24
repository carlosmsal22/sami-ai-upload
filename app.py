import streamlit as st
import os
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.feature_extraction.text import TfidfVectorizer
from openai import OpenAI

st.set_page_config(page_title="SAMI AI – Excel Analyzer", layout="wide")
st.sidebar.image("https://nextaigeninsights.com/wp-content/uploads/2023/10/INSIGHTS-AI-LOGO-White-Transparent.png", use_column_width=True)
st.sidebar.title("💡 Prompt Templates")
st.sidebar.markdown("""
Try these to get started:
- 🔍 Find the top 5 categories by revenue
- 📊 Summarize data trends by region
- ⚖️ Compare performance across time
- 🧠 Show any outliers or unusual values
- 📈 Suggest possible correlations
""")

st.title("SAMI AI – Advanced Analytical Tool")

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

uploaded_file = st.file_uploader("Upload an Excel or CSV file", type=["xlsx", "csv"])
user_prompt = st.text_area("Ask a question about your uploaded file or type any data-related query:")

def parse_file(file):
    if file.name.endswith(".csv"):
        return pd.read_csv(file)
    elif file.name.endswith(".xlsx"):
        return pd.read_excel(file)
    return None

def show_summary_stats(df):
    st.subheader("📊 Summary Statistics")
    numeric_df = df.select_dtypes(include="number")
    if not numeric_df.empty:
        summary = numeric_df.describe().transpose()
        st.dataframe(summary)
        return summary
    else:
        st.warning("No numeric data found.")
        return pd.DataFrame()

def show_tfidf_analysis(df):
    st.subheader("🧠 Text to Numerical Conversion (TF-IDF)")
    text_cols = df.select_dtypes(include='object').columns.tolist()
    if not text_cols:
        st.warning("No text columns found for TF-IDF conversion.")
        return
    selected_col = st.selectbox("Select a text column to convert:", text_cols)
    if selected_col:
        try:
            vectorizer = TfidfVectorizer(max_features=20)
            tfidf_matrix = vectorizer.fit_transform(df[selected_col].fillna("").astype(str))
            tfidf_df = pd.DataFrame(tfidf_matrix.toarray(), columns=vectorizer.get_feature_names_out())
            st.dataframe(tfidf_df)
        except Exception as e:
            st.error(f"TF-IDF error: {e}")

def generate_basic_chart(df):
    numeric_cols = df.select_dtypes(include="number").columns.tolist()
    if len(numeric_cols) >= 2:
        st.subheader("📈 Auto-Generated Chart")
        fig, ax = plt.subplots()
        df[numeric_cols[:2]].plot(kind='bar', ax=ax)
        st.pyplot(fig)

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
        file_info = "No file uploaded."
        df = pd.DataFrame()
        data_sample = ""

    show_tfidf_analysis(df)
    summary_stats = show_summary_stats(df)

    if any(kw in user_prompt.lower() for kw in ["chart", "plot", "compare", "trend", "graph"]):
        generate_basic_chart(df)

    if not df.empty:
        try:
            with st.spinner("Generating GPT insights..."):
                gpt_input = f"You are SAMI AI, an advanced data analyst. The file info: {file_info}\n"
                if not summary_stats.empty:
                    gpt_input += f"Here are summary statistics:\n{summary_stats.to_csv()}\n"
                gpt_input += f"User's prompt: {user_prompt}"

                response = client.chat.completions.create(
                    model="gpt-3.5-turbo",
                    messages=[
                        {"role": "system", "content": gpt_input},
                        {"role": "user", "content": user_prompt}
                    ]
                )
                st.subheader("🧠 GPT Insight")
                st.markdown(response.choices[0].message.content)
        except Exception as e:
            st.error(f"API error: {e}")
