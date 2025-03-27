
import streamlit as st
import pandas as pd
import os
from openai import OpenAI
import matplotlib.pyplot as plt
from wordcloud import WordCloud
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.decomposition import NMF

st.set_page_config(page_title="Text Analytics", layout="wide")
st.title("📝 Text Analytics Module – Sentiment & Topic Modeling")

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

uploaded_file = st.file_uploader("Upload your dataset with open-ended text", type=["csv", "xlsx"])
method = st.selectbox("Choose Topic Modeling Method", ["GPT Summary", "TF-IDF + NMF Topics"])
text_col = st.text_input("Column name containing text responses")

if uploaded_file and text_col and st.button("Analyze Text"):
    try:
        df = pd.read_csv(uploaded_file) if uploaded_file.name.endswith(".csv") else pd.read_excel(uploaded_file)
        if text_col not in df.columns:
            st.error("❌ Column not found.")
        else:
            responses = df[text_col].dropna().astype(str).tolist()
            full_text = "\n".join(responses[:100])  # Limit for speed
            st.success(f"Loaded {len(responses)} responses.")

            if method == "GPT Summary":
                with st.spinner("Using GPT to summarize themes..."):
                    system_prompt = f"You are a text analysis assistant. Analyze the following open-ended survey responses and summarize key topics, common themes, and emotional sentiment."
                    response = client.chat.completions.create(
                        model="gpt-3.5-turbo",
                        messages=[
                            {"role": "system", "content": system_prompt},
                            {"role": "user", "content": full_text}
                        ]
                    )
                    st.subheader("📚 GPT Topic Summary")
                    st.markdown(response.choices[0].message.content)

            elif method == "TF-IDF + NMF Topics":
                st.subheader("🧠 TF-IDF Topic Modeling (NMF)")
                tfidf = TfidfVectorizer(stop_words="english", max_features=500)
                tfidf_matrix = tfidf.fit_transform(responses)
                nmf = NMF(n_components=5, random_state=42)
                W = nmf.fit_transform(tfidf_matrix)
                H = nmf.components_
                feature_names = tfidf.get_feature_names_out()

                for topic_idx, topic in enumerate(H):
                    st.markdown(f"**Topic {topic_idx+1}:** " + ", ".join([feature_names[i] for i in topic.argsort()[:-6:-1]]))

                st.subheader("☁️ Word Cloud")
                wordcloud = WordCloud(width=800, height=300, background_color="white").generate(full_text)
                fig, ax = plt.subplots(figsize=(10, 3))
                ax.imshow(wordcloud, interpolation="bilinear")
                ax.axis("off")
                st.pyplot(fig)

    except Exception as e:
        st.error(f"Error: {e}")
