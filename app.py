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

def summarize_data(df):
    st.subheader("📈 Summary Statistics")
    summary = df.describe(include='all').transpose()
    st.dataframe(summary)
    return summary.to_string()

def show_grouped_insights(df):
    st.subheader("📊 Grouped Insights")
    cat_cols = df.select_dtypes(include='object').columns.tolist()
    num_cols = df.select_dtypes(include='number').columns.tolist()

    if not cat_cols or not num_cols:
        st.info("Grouped insights require at least one categorical and one numeric column.")
        return None, None, None

    cat_col = st.selectbox("Group by (categorical column):", cat_cols, key="cat_col")
    num_col = st.selectbox("Aggregate (numeric column):", num_cols, key="num_col")
    agg_func = st.selectbox("Aggregation method:", ["mean", "sum", "count"], key="agg_func")

    if st.button("Generate Grouped Insights"):
        grouped = df.groupby(cat_col)[num_col].agg(agg_func).reset_index()
        st.dataframe(grouped)

        st.subheader("📈 Chart")
        fig, ax = plt.subplots()
        grouped.plot(x=cat_col, y=num_col, kind="bar", ax=ax, legend=False)
        plt.ylabel(f"{agg_func} of {num_col}")
        st.pyplot(fig)

        return grouped.to_string(index=False), cat_col, num_col
    return None, None, None

if st.button("Analyze"):
    if uploaded_file:
        try:
            df = parse_file(uploaded_file)
            file_info = f"The uploaded file contains {df.shape[0]} rows and {df.shape[1]} columns."
        except Exception as e:
            st.error(f"Error reading file: {e}")
            st.stop()
    else:
        file_info = "No file uploaded."
        df = None

    # Show TF-IDF block
    show_tfidf_analysis(df)

    # Show summary block
    summary_text = summarize_data(df) if df is not None else ""

    # Smart chart from prompt
    keywords = ['chart', 'graph', 'visual', 'compare', 'trend']
    if df is not None and any(kw in user_prompt.lower() for kw in keywords):
        try:
            generate_basic_chart(df)
        except Exception as e:
            st.warning("Chart generation failed. Try refining your data.")

    # Grouped analysis block
    if df is not None:
        grouped_str, cat_col, num_col = show_grouped_insights(df)
    else:
        grouped_str, cat_col, num_col = None, None, None

    # Send summary + grouped results to GPT
    if df is not None:
        system_parts = [
            f"You are SAMI AI, an advanced analytics assistant.",
            file_info,
            f"Here are summary statistics for the file:\n{summary_text}",
        ]
        if grouped_str:
            system_parts.append(f"Here is a grouped {cat_col} vs {num_col} insight:
{grouped_str}")
        system_prompt = "\n\n".join(system_parts)

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
