
import streamlit as st
import pandas as pd
import os
from openai import OpenAI

st.set_page_config(page_title="Persona Generator", layout="wide")
st.title("👤 AI-Based Persona Generator")

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

uploaded_file = st.file_uploader("Upload segmentation or open-ended survey data", type=["csv", "xlsx"])
text_col = st.text_input("Enter column name with segments or open-ended responses")

persona_prompt_template = """
You are a persona-building assistant.

Based on the following customer responses or segment labels, generate 2-3 distinct buyer personas.

Each persona should include:
- Name
- Brief description
- Demographics (if inferable)
- Motivations
- Frustrations/Pain Points
- Preferred communication channels

Use only the content provided and do not invent unrelated attributes.

Customer input:
{responses}
"""

if uploaded_file and text_col and st.button("Generate Personas"):
    try:
        df = pd.read_csv(uploaded_file) if uploaded_file.name.endswith(".csv") else pd.read_excel(uploaded_file)
        if text_col not in df.columns:
            st.error("❌ Column not found.")
        else:
            entries = df[text_col].dropna().astype(str).tolist()
            combined_text = "\n".join(entries[:100])  # Limit to 100 for performance
            with st.spinner("Generating personas..."):
                final_prompt = persona_prompt_template.format(responses=combined_text)
                response = client.chat.completions.create(
                    model="gpt-3.5-turbo",
                    messages=[
                        {"role": "system", "content": "You are a helpful market research analyst."},
                        {"role": "user", "content": final_prompt}
                    ]
                )
                st.subheader("🎯 Generated Personas")
                st.markdown(response.choices[0].message.content)

    except Exception as e:
        st.error(f"Error: {e}")
