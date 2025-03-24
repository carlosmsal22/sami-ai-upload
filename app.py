import streamlit as st
import os
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.feature_extraction.text import TfidfVectorizer
from openai import OpenAI

# ----------------------------
# Page config & branding
# ----------------------------
st.set_page_config(page_title="SAMI AI – Excel Analyzer", layout="wide")

# Sidebar: Branding + Prompt Templates
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

# ----------------------------
# Main interface
# ----------------------------
st.title("SAMI AI – Advanced Analytical Tool")

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

uploaded_file = st.file_uploader("Upload an Excel or CSV file", type=["xlsx", "csv"])
user_prompt = st.text_area("Ask a question about your uploaded file or type any data-related query:")

def parse_file(file):
    if file.name.endswith(".csv"):
        return pd.read_csv(file)
    elif file.name.endswith(".xlsx"):
        return pd.read_excel(file)
    else:
        return None

def generate_basic_chart(df):
    numeric_cols = df.select_dtypes(include="number").columns.tolist()
    if len(numeric_cols) >= 2:
        st.subheader("📊 Auto-Generated Chart")
        st.markdown("This chart compares the first two numeric columns.")
        fig, ax = plt.subplots()
        df[numeric_cols[:2]].plot(kind='bar', ax=ax)
        st.pyplot(fig)

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
            st.error(f"TF-IDF processing error: {e}")

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

    # Show TF-IDF block
    show_tfidf_analysis(df)

    # Generate chart if prompt is related to visualization
    keywords = ['chart', 'graph', 'visual', 'compare', 'trend']
    if any(kw in user_prompt.lower() for kw in keywords):
        try:
            generate_basic_chart(df)
        except Exception as e:
            st.warning("Chart generation failed. Try refining your data.")

    system_prompt = f"You are SAMI AI, an advanced analytics assistant. {file_info} The first few rows of the file look like this:\n{data_sample}"

    try:
        with st.spinner("Generating insights..."):
            response = client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_prompt}
                ]
            )
            st.markdown(response.choices[0].message.content)
    except Exception as e:
        st.error(f"API error: {e}")
