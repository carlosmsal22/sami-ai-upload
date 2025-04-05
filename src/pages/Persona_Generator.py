import streamlit as st
import pandas as pd
import os
from openai import OpenAI

st.set_page_config(page_title="👤 AI-Based Persona Generator", layout="wide")
st.title("👤 AI-Based Persona Generator")

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# Sidebar UI
with st.sidebar:
    st.header("📥 Upload Data")
    uploaded_file = st.file_uploader("Upload CSV or Excel file", type=["csv", "xlsx"])
    text_col = st.text_input("📝 Column with segment labels or open-ended responses")

# Prompt template
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

# Processing
if uploaded_file and text_col:
    try:
        # Load data
        df = pd.read_excel(uploaded_file) if uploaded_file.name.endswith("xlsx") else pd.read_csv(uploaded_file)
        st.success(f"✅ Loaded {df.shape[0]} rows, {df.shape[1]} columns")
        st.write("🔍 Data Preview:", df[[text_col]].dropna().head())

        if text_col not in df.columns:
            st.error("❌ Column not found. Please verify the column name.")
        elif st.button("🚀 Generate Personas"):
            entries = df[text_col].dropna().astype(str).tolist()
            if not entries:
                st.warning("⚠️ No valid responses found in the selected column.")
            else:
                combined_text = "\n".join(entries[:100])  # Limiting to 100 rows
                final_prompt = persona_prompt_template.format(responses=combined_text)

                with st.spinner("Generating personas..."):
                    response = client.chat.completions.create(
                        model="gpt-3.5-turbo",
                        messages=[
                            {"role": "system", "content": "You are a helpful market research analyst."},
                            {"role": "user", "content": final_prompt}
                        ]
                    )
                    result = response.choices[0].message.content
                    st.subheader("🎯 Generated Personas")
                    st.markdown(result)

    except Exception as e:
        st.error(f"❌ Error: {e}")

else:
    st.info("📌 Please upload a file and specify a text column to proceed.")
